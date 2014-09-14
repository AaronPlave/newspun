from flask import Flask
from flask import render_template
import json
from lib.media_lib import media
from lib.algorithms import process
from uwsgidecorators import *
import time

app = Flask(__name__)

# Initialize blueprints

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

@thread
def update():
	WAIT_TIME = 60
	media_obj = media.Media()
	media_obj.update_source('HuffingtonPost')
	print "Finished updating DB"
	process.analyze_all_items()

	# now wait
	for i in xrange(0, WAIT_TIME):
		time.sleep(0.5)

update()

if __name__ == '__main__':
    app.run()