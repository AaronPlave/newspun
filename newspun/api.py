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
		CNN = 0
		HuffPost = 0
		BBC = 0
		FOX = 0
		for article in selected_sources[CNN]:
			CNN += article["word_count"][input1]
		for each in selected_sources[HuffPost]:
			HuffPost += article["word_count"][input1]
		for each in selected_sources[BBC]:
			BBC += article["word_count"][input1]
		for each in selected_sources[FOX]:
			FOX += article["word_count"][input1]
		return jsonify(CNN, HuffPost, BBC, FOX)

	elif type_of_analysis == 'common_words':
		# results = [s['common_words'] for s in selected_sources
		# for each data source, grab text, analyze
		CNN = []
		HuffPost = []
		BBC = []
		FOX = []
		for article in selected_sources[CNN]:
			CNN.append(article["common_words"])
		for each in selected_sources[HuffPost]:
			HuffPost.append(article["common_words"])
		for each in selected_sources[BBC]:
			BBC.append(article["common_words"])
		for each in selected_sources[FOX]:
			FOX.append(article["common_words"])
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
		return jsonify(CNN, HuffPost, BBC, FOX)

	elif type_of_analysis == 'sentiment':
		CNN = 0
		HuffPost = 0
		BBC = 0
		FOX = 0
		countC = 0
		countH = 0
		countB = 0
		countF = 0
		for article in selected_sources[CNN]:
			CNN += article["sentiment"]
			countC += 1
		for each in selected_sources[HuffPost]:
			HuffPost += article["sentiment"]
			countH += 1
		for each in selected_sources[BBC]:
			BBC += article["sentiment"]
			countB += 1
		for each in selected_sources[FOX]:
			FOX += article["sentiment"]
			countF += 1
		return jsonify((CNN/countC), (HuffPost/countH), (BBC/countB), (FOX/countF))

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

	elif type_of_query == 'proximity':
		CNN = 0
		HuffPost = 0
		BBC = 0
		FOX = 0
		for each in selected_sources[CNN]:
			CNN += proximity(text)
		for each in selected_sources[HuffPost]:
			HuffPost += words[input1]
		for each in selected_sources[BBC]:
			BBC += words[input1]
		for each in selected_sources[FOX]:
			FOX += words[input1]
		return jsonify(CNN, HuffPost, BBC, FOX)
		pass

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
