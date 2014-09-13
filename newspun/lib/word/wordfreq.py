import re
from flask import jsonify
from nltk.corpus import stopwords
from nltk import FreqDist
from nltk.tokenize.punkt import PunktWordTokenizer

def add_article(text):
  text = re.sub('[.]','',text)
  text = PunktWordTokenizer().tokenize(text)
  freq = FreqDist(text)
  for f in stopwords.words('english'):
    if f in freq:
      del freq[f]
  return freq
def all_word_count(text):
  return jsonify(add_article(text))

def most_common(text):
  jsonify(add_article(text).most_common(10))
