import re
import json
json_data = open('words.json').read()
lib = json.loads(json_data)

class scored_words():
  def __init__(self,score,comparitave,words = []):
    self.score = score
    self.comparitave = comparitave
    self.words = words

def change_score(tally,phrase,is_neg):
    no_punctuation = re.sub('/[^a-zA-Z]+/g', " ",phrase)
    no_punctuation = re.sub('/ {2, }/', ' ',no_punctuation)
    tokens = no_punctuation.split(" ")
    leng = len(tokens)
    for each in tokens:
      if(is_neg):
          if lib.get(each) and lib.get(each) < 0:
            tally = add_append(each,lib.get(each),tally,leng)
      else:
          if lib.get(each) and lib.get(each) > 0:
            tally = add_append(each,lib.get(each),tally,leng)

    return tally

def add_append(t,hits,tally,l):
  tally.score = tally.score - hits
  tally.comparitave = tally.score/l
  if tally.words:
    tally.words.append(t)
  else:
    tally.words = [t]
  return tally

def analyze_get_score(phrase,need_score):
  tally = scored_words(0,0,[])
  tally = change_score(tally,phrase,True)
  tally = change_score(tally,phrase,False)
  if(need_score):
    return tally.score
  else:
    return tally.comparitave

