from flask import make_response
from flask import jsonify
from flask import Blueprint
from flask import request
from pymongo import MongoClient

client = MongoClient()
db = client.newspindb
processed = db.processed

api = Blueprint('api',__name__,template_folder = 'templates')

@analyze.route('')
def index():
  if request.form.get('source'):
    if not request.form.get('catagory'):
      processed.find({'source':request.form.get('source')})
    else:
      processed.find({'source':request.form.get('source')})
  if request.form.get('catagory'):

