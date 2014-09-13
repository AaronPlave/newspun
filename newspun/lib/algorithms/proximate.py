# I require a string and two words to locate
def proximity(text, word1, word2):
	count = 0
	sentences = text.split('.')
	for line in sentences:
		words = line.split(None)
		if (word1 in words) and (word2 in words):
			count += 1
	return count