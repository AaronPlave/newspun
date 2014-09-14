from flask import Blueprint
from flask import json
from flask import jsonify
from pymongo import MongoClient
import wordfreq
import GunningFog
import sentiment_analysis

client = MongoClient()
db = client.newspundb
raw_text = db.text
processed = db.processed


def analyze_all_items():
  items = raw_text.find()
  for each in items:
    process(each)
    
  raw_text.drop()
  print "Finished processing DB data"

def process(collection_item):
  text = collection_item['text']
  words = wordfreq.all_word_count(text)
  common_words = wordfreq.most_common_words(text)
  readability = GunningFog.count(text)
  types = wordfreq.tokenize_title(collection_item['title'])
  sentiment = sentiment_analysis.analyze_get_score(text,False)
  collection_item["word_count"] = words
  collection_item["common_words"] = common_words
  collection_item["readability_score"] = readability
  collection_item['sentiment'] = sentiment
  collection_item['tags'] = types
  if processed.find(collection_item).count() == 0:
    processed.insert(collection_item)
  
