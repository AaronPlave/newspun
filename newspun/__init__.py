from flask import Flask
from flask import render_template
import json
from lib.media_lib import media

app = Flask(__name__)

# Initialize blueprints

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sources')
def sources():
  return json.dumps({'val': 'Huffington Post','val': 'CNN', 'val':'FOX news','val':'BBC'})


if __name__ == '__main__':
    app.run()
