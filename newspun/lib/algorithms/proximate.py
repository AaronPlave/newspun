# I require a string and two words to locate
# returns the number of sentences with the words in proximity
def proximity(text, word1, word2):
	count = 0
	onealone = 0
	twoalone = 0
	sentences = text.split('.')
	for line in sentences:
		words = line.split(None)
		if word1 in words:
			onealone += 1
		if word2 in words:
			twoalone += 1
		if (word1 in words) and (word2 in words):
			count += 1
	return (onealone, twoalone, count)

# returns information
#def 

# information is an array of articles
# returns a dictionary of 
def prox_time(information, word1, word2):
	bins = {}
	for article in information:
		if not bins[article.date]:
			bins[article.date] = proximity(article.text, word1, word2)
		else:
			bins[article.date] += proximity(article.text, word1, word2)