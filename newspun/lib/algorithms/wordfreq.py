from flask import Blueprint
from flask import jsonify
from nltk.corpus import stopwords
from nltk import FreqDist
from nltk.tokenize.punkt import PunktWordTokenizer
from pymongo import MongoClient
import re
import json

def add_article(text):
  text = re.sub('[-_.,\']','',text).lower()
  text = PunktWordTokenizer().tokenize(text)
  freq = FreqDist(text)
  for f in stopwords.words('english'):
    if f in freq:
      del freq[f]
  return freq

def tokenize_title(text):
  text = re.sub('[.]','',text)
  text = PunktWordTokenizer().tokenize(text)
  for f in stopwords.words('english'):
    if f in text:
      text.remove(f)
  return text


# @frequency.route('',methods = ['POST'])
def all_word_count(text):
  return json.dumps(add_article(text))

# @frequency.route('')
def most_common_words(text,limit = 10):
  articles = add_article(text)
  if limit > len(articles):
    limit = len(articles)-1

  return json.dumps(add_article(text).items()[0:limit])
