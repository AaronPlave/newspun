from flask import Blueprint
from flask import json
from flask import jsonify
from pymongo import MongoClient
import wordfreq
import GunningFog
import sentament_analysis

client = MongoClient()
db = client.newspundb
raw_text = db.text
processed = db.processed


def analize_all_items():
  items = raw_text.find()
  for each in items:
    process(each)
    raw_text.remove(each)
def process(collection_item):
  text = collection_item['text']
  words = frequency.all_word_count(text)
  common_words = frequency.most_common(text)
  readability = GunningFog.count(text)
  sentament = sentament_analysis.analyze_get_score(text,False)
  collection_item["word_count"] = words
  collection_item["common_words"] = common_words
  collection_item["readability_score"] = readabilitiy
  collection_item['sentament'] = sentament
  processed.insert(collection_item)
