from flask import Flask, request
from flask import render_template
from lib.media_lib import media
from lib.algorithms import process
from api import api
from uwsgidecorators import *
import threading
import json
import time

app = Flask(__name__)

# Initialize blueprints
app.register_blueprint(api,url_prefix='/api')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sources')
def sources():
	return json.dumps([
  	{'val': 'Huffington Post'},
  	{'val': 'CNN'}, 
  	{'val':'FOX news'},
  	{'val':'BBC'}])

# @app.route('/api')
# def api():
# 	return api.handle_request(request)
# 	# return api.hello1()

#TODO: Make something on a timer to delete articles
#older than X...


@app.route('/force_populate_database_secret_key')
def force_update():
	t = threading.Thread(target=background_update)
	t.start()

@timer(1800)
def update(args):
	t = threading.Thread(target=background_update)
	t.start()

def background_update():
	media_obj = media.Media()
	media_obj.update_source('HuffingtonPost')
	media_obj.update_source('BBC')
	print "Finished updating DB"
	process.analyze_all_items()
	
if __name__ == '__main__':
    app.run()