import datetime
import sentiment_analysis
import GunningFog

# sources come in a list, type is a single variable, topic is the tags, category is business, etc.
#def time(sources, topic, types, category, information):
	# 'start' time to base bin separation on
#	now = datetime.datetime.now()
#	bins = {}
#	count = 0
	# set up the action necessary depending on the type
#	if types == proximity:
#		data = proximity(article.text, word1, word2)
#	elif types == freq:
		# incomplete, ask Tyler
#		data = 
#	elif types == sentiment:
		#incomplete, ask Tyler
#		data = analyze_get_score(article.text)
#	elif types == readability:
#		data = count(article.text)
#	else:
#		return "Error: invalid analysis type"
#	for article in information:
#		time = (article.year*8760)+(article.month*720)+(article.day*24)+(article.hour])
#		nowtime = (now.year*8760)+(now.month*720)+(now.day*24)+(now.hour)
#		dif = nowtime - time
#		if dif < 12:
#			bins[1] = data
#		elif dif < 24:
#			bins[2] = data
#		else:

# 'information' is selected sources for a specific source, call more than once if the user 
# specifies more than one source

def sentiment_time(information):
	now = datetime.datetime.now()
	bins = [[],[],[],[],[],[]]
	for article in information:
		# convert time into total number of hours
		time = (article.year*8760)+(article.month*720)+(article.day*24)+(article.hour])
		nowtime = (now.year*8760)+(now.month*720)+(now.day*24)+(now.hour)
		# compute age of article in hours
		dif = nowtime - time
		# separate into bins by half days
		if dif < 12:
			bins[0].append(article["sentiment"])
		elif dif < 24:
			bins[1].append(article["sentiment"])
		elif dif < 36:
			bins[2].append(article["sentiment"])
		elif dif < 48:
			bins[3].append(article["sentiment"])
		elif dif < 60:
			bins[4].append(article["sentiment"])
		else:
			bins[5].append(article["sentiment"])
	datapoints = []
	# make array of averagae sentiment score
	for group in bins:
		total = 0
		count = 0
		for num in group:
			total += num
			count += 1
		datapoints.append(total/count)
	return datapoints

# 'information' is selected sources for a specific source, call more than once if the user 
# specifies more than one source

def readability_time(information):
	now = datetime.datetime.now()
	bins = [[],[],[],[],[],[]]
	for article in information:
		# convert time into total number of hours
		time = (article.year*8760)+(article.month*720)+(article.day*24)+(article.hour])
		nowtime = (now.year*8760)+(now.month*720)+(now.day*24)+(now.hour)
		# compute age of article in hours
		dif = nowtime - time
		# separate into bins by half days
		if dif < 12:
			bins[0].append(article["readability_score"])
		elif dif < 24:
			bins[1].append(article["readability_score"])
		elif dif < 36:
			bins[2].append(article["readability_score"])
		elif dif < 48:
			bins[3].append(article["readability_score"])
		elif dif < 60:
			bins[4].append(article["readability_score"])
		else:
			bins[5].append(article["readability_score"])
	datapoints = []
	# make array of averagae readability score
	for group in bins:
		total = 0
		count = 0
		for num in group:
			total += num
			count += 1
		datapoints.append(total/count)
	return datapoints

# 'information' is selected sources for a specific source, call more than once if the user 
# specifies more than one source

def proximity_time(information, input1, input2):
	now = datetime.datetime.now()
	bins = [[],[],[],[],[],[]]
	for article in information:
		# convert time into total number of hours
		time = (article.year*8760)+(article.month*720)+(article.day*24)+(article.hour])
		nowtime = (now.year*8760)+(now.month*720)+(now.day*24)+(now.hour)
		# compute age of article in hours
		dif = nowtime - time
		# separate into bins by half days
		if dif < 12:
			bins[0].append(proximity(article["text"], input1, input2))
		elif dif < 24:
			bins[1].append(proximity(article["text"], input1, input2))
		elif dif < 36:
			bins[2].append(proximity(article["text"], input1, input2))
		elif dif < 48:
			bins[3].append(proximity(article["text"], input1, input2))
		elif dif < 60:
			bins[4].append(proximity(article["text"], input1, input2))
		else:
			bins[5].append(proximity(article["text"], input1, input2))
	datapoints = []
	# make array of averagae readability score
	for group in bins:
		total = 0
		count = 0
		for num in group:
			total += num
			count += 1
		datapoints.append(total/count)
	return datapoints

