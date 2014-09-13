from flask import Flask
from flask import render_template
from lib.word.wordfreq import frequency
from lib.media_lib import media
app = Flask(__name__)

# Initialize blueprints
app.register_blueprint(frequency,url_prefix='/frequency')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
