from flask import make_response
from flask import jsonify
from flask import Blueprint
from flask import request
from pymongo import MongoClient
from lib.algorithms import proximate
import json

client = MongoClient()
db = client.newspundb
processed = db.processed

api = Blueprint('api',__name__,template_folder='templates')

# common_words   --returns top 10 most common words for srcs
# unique_freq    --returns freq of particular word, avg over all @input1=unique word
# sentiment
# readability
# proximity


def tryDiv(a,b):
	"""
	Divides a/b if possible otherwise returns 0.
	"""
	try:
		return float(a)/b
	except:
		return None

@api.route("")
def index():
	print "REQ",request.args
	srcs_str = request.args.get('sources')
	srcs = srcs_str.split('?')
	print "SRCS:",srcs
	type_of_analysis = request.args.get('type')
	print "TYPE:",type_of_analysis
	input1 = request.args.get('input1')
	input2 = request.args.get('input2')
	selected_sources = {}
	if srcs:
		for src in srcs:
			selected_sources[src] = processed.find({'media_source':src})
	else:
		return jsonify({'ERROR':'NO DATA REQUESTED'})

	if not selected_sources:
		return jsonify({'ERROR':'NO DATA REQUESTED'})

	#algs switches
	if type_of_analysis == 'unique_freq':
		"""
		http://127.0.0.1:5000/api?sources=HuffingtonPost?BBC&type=unique_freq&input1=isis
		"""
		CNN = 0
		HuffPost = 0
		BBC = 0
		FOX = 0

		if 'CNN' not in selected_sources:
			selected_sources['CNN'] = {}
		if 'HuffingtonPost' not in selected_sources:
			selected_sources['HuffingtonPost'] = {}
		if 'BBC' not in selected_sources:
			selected_sources['BBC'] = {}
		if 'FOXNews' not in selected_sources:
			selected_sources['FOXNews'] = {}

		for article in selected_sources['CNN']:
			ad = eval(article["word_count"])
			if ad.get(input1):
				CNN += ad[input1]
		for article in selected_sources['HuffingtonPost']:
			print eval(article["word_count"])
			ad = eval(article["word_count"])
			if ad.get(input1):
				HuffPost += ad[input1]
		for article in selected_sources['BBC']:
			ad = eval(article["word_count"])
			if ad.get(input1):
				BBC += ad[input1]
		for article in selected_sources['FOXNews']:
			ad = eval(article["word_count"])
			if ad.get(input1):
				FOX += ad[input1]

		return jsonify({"CNN":CNN, "HuffingtonPost":HuffPost, "BBC":BBC, "FOXNews":FOX})

	elif type_of_analysis == 'common_words':
		# results = [s['common_words'] for s in selected_sources
		# for each data source, grab text, analyze
		CNN = []
		HuffPost = []
		BBC = []
		FOX = []
		if 'CNN' not in selected_sources:
			selected_sources['CNN'] = {}
		if 'HuffingtonPost' not in selected_sources:
			selected_sources['HuffingtonPost'] = {}
		if 'BBC' not in selected_sources:
			selected_sources['BBC'] = {}
		if 'FOXNews' not in selected_sources:
			selected_sources['FOXNews'] = {}

		for article in selected_sources['CNN']:
			for tup in article["common_words"]:
				if CNN == []:
					CNN += tup
				else:
					for anything in CNN:
						if anything[0] == tup[0]:
							CNN += (tup[0], tup[1] + anything[1])
						else:
							CNN += tup
		for article in selected_sources['HuffingtonPost']:
			for article in selected_sources['HuffingtonPost']:
				for tup in article["common_words"]:
					if HuffPost == []:
						HuffPost += tup
					else:
						for anything in HuffPost:
							if anything[0] == tup[0]:
								HuffPost += (tup[0], tup[1] + anything[1])
							else:
								HuffPost += tup
		for article in selected_sources['BBC']:
			for tup in article["common_words"]:
				if BBC == []:
					BBC += tup
				else:
					for anything in BBC:
						if anything[0] == tup[0]:
							BBC += (tup[0], tup[1] + anything[1])
						else:
							BBC += tup
		for article in selected_sources['FOXNews']:
			for tup in article["common_words"]:
				if FOX == []:
					FOX += tup
				else:
					for anything in FOX:
						if anything[0] == tup[0]:
							FOX += (tup[0], tup[1] + anything[1])
						else:
							FOX += tup
		if len(CNN) > 10:
			CNN = sorted(CNN, key=lambda tup: tup[1])[::1]
			CNN = CNN[:10]
		if len(HuffPost) > 10:
			HuffPost = sorted(HuffPost, key=lambda tup: tup[1])[::1]
			HuffPost = HuffPost[:10]
		if len(BBC) > 10:
			BBC = sorted(BBC, key=lambda tup: tup[1])[::1]
			BBC = BBC[:10]
		if len(FOX) > 10:
			FOX = sorted(FOX, key=lambda tup: tup[1])[::1]
			FOX = FOX[:10]
		return jsonify({"CNN":CNN, "HuffingtonPost":HuffPost, "BBC":BBC, "FOXNews":FOX})

	elif type_of_analysis == 'sentiment':
		CNN = 0
		HuffPost = 0
		BBC = 0
		FOX = 0
		countC = 0
		countH = 0
		countB = 0
		countF = 0

		if 'CNN' not in selected_sources:
			selected_sources['CNN'] = {}
		if 'HuffingtonPost' not in selected_sources:
			selected_sources['HuffingtonPost'] = {}
		if 'BBC' not in selected_sources:
			selected_sources['BBC'] = {}
		if 'FOXNews' not in selected_sources:
			selected_sources['FOXNews'] = {}

		for article in selected_sources['CNN']:
			CNN += article["sentiment"]
			countC += 1
		for article in selected_sources['HuffingtonPost']:
			HuffPost += article["sentiment"]
			countH += 1
		for article in selected_sources['BBC']:
			BBC += article["sentiment"]
			countB += 1
		for article in selected_sources['FOXNews']:
			FOX += article["sentiment"]
			countF += 1

		return jsonify({"CNN":tryDiv(CNN,countC), "HuffingtonPos":tryDiv(HuffPost,countH),
			 "BBC":tryDiv(BBC,countB), "FOXNews":tryDiv(FOX,countF)})

	elif type_of_analysis == 'readability':
		"""
		EXAMPLE
		http://127.0.0.1:5000/api?sources=HuffingtonPost&type=readability
		"""
		print "Computing:",type_of_analysis
		# print "Src",srcs
		print "selected_sources",selected_sources
		#average the readability over each source's respective articles
		calculated_scores = []
		# print "ASD",selected_sources,type(selected_sources),selected_sources[selected_sources.keys()[0]]
		for source in selected_sources.keys():
			total = 0
			# print "SRC",source
			# print "count", selected_sources[source].count()
			if selected_sources[source].count() == 0:
				continue
			for article in selected_sources[source]:
				total += article['readability_score']

			readability_score = float(total) / selected_sources[source].count()
			print "Total",total
			print "Num articles",selected_sources[source].count()
			print "SCORE",readability_score
			score_obj = {
				'source':article['media_source'],
				'readability_score':readability_score
			}
			calculated_scores.append(score_obj)
		print "CALC SCORES:",calculated_scores
		return json.dumps(calculated_scores)

	elif type_of_analysis == 'proximity':
		CNN = 0
		HuffPost = 0
		BBC = 0
		FOX = 0

		if 'CNN' not in selected_sources:
			selected_sources['CNN'] = {}
		if 'HuffingtonPost' not in selected_sources:
			selected_sources['HuffingtonPost'] = {}
		if 'BBC' not in selected_sources:
			selected_sources['BBC'] = {}
		if 'FOXNews' not in selected_sources:
			selected_sources['FOXNews'] = {}

		for article in selected_sources["CNN"]:
			CNN += proximate.proximity(article["text"],input1,input2)
		for each in selected_sources["HuffingtonPost"]:
			HuffPost += proximate.proximity(article["text"],input1,input2)
		for each in selected_sources["BBC"]:
			BBC += proximate.proximity(article["text"],input1,input2)
		for each in selected_sources["FOXNews"]:
			FOX += proximate.proximity(article["text"],input1,input2)
		return jsonify(CNN, HuffPost, BBC, FOX)

	selected.get("type")
	return jsonify({"s":"b"})

#joomy passes the source, topics, type
def handle_request(request):
  # print "GOT REQ;",request
  # src = request.form.get('source')
  # topic = request.form.get('topic')
  # type_of_query = request.form.get('type')
  # if src:
  #   selected = processed.find({'media_source':src})
  # if topic:
  #   selected = selected.find({'tags':topic})
  # if not selected:
  #   return jsonify({'ERROR':'NO DATA REQUESTED'})
  # if type_of_query:
  #   selected.get("type")
  return jsonify({"SUCCESS!":'poodle'})
