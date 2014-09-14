from flask import make_response
from flask import jsonify
from flask import Blueprint
from flask import request
from pymongo import MongoClient
from lib.algorithms import proximate


client = MongoClient()
db = client.newspindb
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
	srcs = request.args.get('sources')
	print "SRCS:",srcs
	type_of_analysis = request.args.get('type')
	print "TYPE:",type_of_analysis
	input1 = request.args.get('input1')
	input2 = request.args.get('input2')
	if srcs:
		selected_sources = []
		for src in srcs:
			selected = processed.find({'media_source':src})
			selected_sources.append(selected)
	else:
		return jsonify({'ERROR':'NO DATA REQUESTED'})

	if not selected_sources:
		return jsonify({'ERROR':'NO DATA REQUESTED'})
	
	if type_of_query == 'freq':
		
		# results = [s['common_words'] for s in selected_sources
		# for each data source, grab text, analyze
		return jsonify({'ERROR':'NOT YET IMPLEMENTED'})	
	elif type_of_query == 'sentiment':
		pass
	elif type_of_query == 'readability':
		#average the readability over each source's respective articles
		for source in selected selected_sources:
			avg = 0
			for article in source:
				avg += article['readability_score']
			

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
