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
	# if type_of_analysis == 'unique_freq':
	# 	CNN = 0
	# 	HuffPost = 0
	# 	BBC = 0
	# 	FOX = 0
	# 	for each in processed:
	# 		if 'source':source[0]['media_source'] == CNN:
	# 			CNN += words[input1]
	# 		elif 'source':source[0]['media_source'] == HuffingtonPost:
	# 			HuffPost += words[input1]
	# 		elif 'source':source[0]['media_source'] == BBC:
	# 			BBC += words[input1]
	# 		elif 'source':source[0]['media_source'] == FOX:
	# 			FOX += words[input1]
	# 		else:
	# 			print "Invalid Source"
	# 	return jsonify(CNN, HuffPost, BBC, FOX)

	elif type_of_analysis == 'common_words':
		# results = [s['common_words'] for s in selected_sources
		# for each data source, grab text, analyze
		return jsonify({'ERROR':'NOT YET IMPLEMENTED'})		
	elif type_of_analysis == 'sentiment':
		return jsonify({'ERROR':'NOT YET IMPLEMENTED'})	

	elif type_of_analysis == 'readability':
		print "Computing:",type_of_analysis
		# print "Src",srcs
		print "selected_sources",selected_sources
		#average the readability over each source's respective articles
		calculated_scores = []
		# print "ASD",selected_sources,type(selected_sources),selected_sources[selected_sources.keys()[0]]
		for source in selected_sources.keys():
			total = 0
			print "SRC",source
			print "VAL", selected_sources[source].count()
			for article in selected_sources[source]:
				print article
				avg += article['readability_score']

			readability_score = float(total) / source.count() 
			score_obj = {
				'source':source[0]['media_source'],
				'readability_score':readability_score
			}
			calculated_scores.append(score_obj)
		print "CALC SCORES:",calculated_scores
		return jsonify(calculated_scores)

	elif type_of_query == 'proximity':

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
