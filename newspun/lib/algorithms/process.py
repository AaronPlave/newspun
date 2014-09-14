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
    raw_text.remove(each)

def process(collection_item):
  text = collection_item['text']
  words = wordfreq.all_word_count(text)
  common_words = wordfreq.most_common_words(text)
  readability = GunningFog.count(text)
  types = tokenize_title(title)
  sentiment = sentiment_analysis.analyze_get_score(text,False)
  collection_item["word_count"] = words
  collection_item["common_words"] = common_words
  collection_item["readability_score"] = readabilitiy
  collection_item['sentiment'] = sentiment
  collection_item['tags'] = types
  processed.insert(collection_item)
