import re
import json
json_data = open('../wordlist/words.json').read()
lib = json.loads(json_data)
class scored_words:
  def __init___(self,score,comparitave,words):
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
          if lib[each] and lib[each] < 0:
            tally = add_append(each,lib[each],tally,leng)
      else:
          if lib[each] and lib[each] > 0:
            tally = add_append(each,lib[each],tally,leng)

    return tally
def add_append(t,score,tally,l):
  tally.score = score - hits
  tally.comparitave = score/l
  tally.words = words.append(t)
  return tally

def analyze_get_score(phrase,need_score):
  tally = scored_words(0,0,[])
  tally = change_score(tally,phrase,True)
  tally = change_score(tally,phase,False)
  if(need_score):
    return tally.score
  else:
    return tally.comparitave
print(analyze_get_score('i hate this shit',False))
