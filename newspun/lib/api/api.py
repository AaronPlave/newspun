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
  src = request.form.get('source')
  topic = request.form.get('topic')
  type_of_query = request.form.get('type')
  if src:
    selected = processed.find('media_source':src)
  if topic:
    selected = selected.find('tags':topic)
  if not selcted:
    return jsonify({'ERROR':'NO DATA REQUESTED'})
  if type_of_query:
    selected.get("type")
