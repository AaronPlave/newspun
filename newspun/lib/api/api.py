from flask import make_response
from flask import jsonify
from flask import Blueprint
from flask import request
from pymongo import MongoClient

client = MongoClient()
db = client.newspindb
processed = db.processed

api = Blueprint('api',__name__,template_folder = 'templates')
#joomy passes the source, topics, type
@analyze.route('')
def index():
	#sources will be a list of source IDs.
	if request.form.get('sources'):
		if not request.form.get('category'):
      		processed.find({'source':request.form.get('source')})
    	else:
      		processed.find({'source':request.form.get('source')})

