from flask import Flask
from flask import render_template
import json
from lib.process import process
from lib.media_lib import media

app = Flask(__name__)

# Initialize blueprints
app.register_blueprint(process,url_prefix = '/process')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sources')
def sources():
	    return json.dumps(media.sources)


if __name__ == '__main__':
    app.run()
