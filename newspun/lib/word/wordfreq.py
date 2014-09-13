from flask import Blueprint
from flask import jsonify
from nltk.corpus import stopwords
from nltk import FreqDist
from nltk.tokenize.punkt import PunktWordTokenizer
from pymongo import MongoClient
import re

client = MongoClient()
db = client.newspindb
raw_text = db.text
frequencies = db.frequencies

frequency = Blueprint('frequency',__name__,template_folder = 'templates')
def add_article(text):
  text = re.sub('[.]','',text)
  text = PunktWordTokenizer().tokenize(text)
  freq = FreqDist(text)
  for f in stopwords.words('english'):
    if f in freq:
      del freq[f]
  freq_to_db = {
      'all_word_count' : freq,
      'most_common_five' : freq.most_common(5)
      }
  frequencies.insert(freq_to_db)
  return freq

@frequency.route('',methods = ['POST'])
def all_word_count(text):
  return jsonify(add_article(text))

@frequency.route('')
def most_common(limit = 10):
  jsonify(add_article(text).most_common(limit))
