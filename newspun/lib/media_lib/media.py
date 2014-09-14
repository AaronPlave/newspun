from flask import jsonify
from pymongo import MongoClient
import feedparser
import re
import time
import datetime
import requests
from BeautifulSoup import BeautifulSoup

client = MongoClient()
db = client.newspundb
raw_text = db.text

default_categories = ['Economics','Entertainment','Food',
		'Politics','Religion','Science','Sports','Style',
		'Technology','Travel','World'
]

sources = ['HuffingtonPost','CNN','FOXNews','BBC']


def add_to_db(obj_to_insert,id_value):
	if db.text.find({'id':id_value}).count() == 0:
		db.text.insert(obj_to_insert)


#TODO: Figure out time system and last_update
class Media():
	def __init__(self):
		self.sources = sources

	def update_all(self):
		"""
		Updates all news sources and adds them to the db
		"""
		for source in self.sources:
			self.update_source(source)

	def update_source(self,source):
		if source == "HuffingtonPost":
			huff = HuffingtonPost(default_categories)
			huff.fetch_articles()

			# update the last update time
			last_update = time.time()

		elif source == "CNN":
			cnn = CNN(default_categories)
			cnn.fetch_articles()

			# update the last update time
			last_update = time.time()

		elif source == "FOXNews":
			fox = FOXNews(default_categories)
			fox.fetch_articles()

			# update the last update time
			last_update = time.time()

		elif source == "BBC":
			bbc = BBC(default_categories)
			bbc.fetch_articles()

			# update the last update time
			last_update = time.time()
		else:
			print "Source:",source,"does not match any of the sources."

TAG_RE = re.compile(r'<[^>]+>')
def remove_tags(text):
	return TAG_RE.sub('', text)


#below are specific source classes. Each will be slightly different depending on
#whether or not the source has usable API vs RSS.

class HuffingtonPost():
	def __init__(self,default_categories):
		self.name = "HuffingtonPost"
		self.default_categories = default_categories
		self.articles=[]
		self.categories = {
			'Economics':"http://www.huffingtonpost.com/feeds/verticals/business/news.xml",
			'Entertainment':"http://www.huffingtonpost.com/feeds/verticals/entertainment/news.xml",
			"Food":"http://www.huffingtonpost.com/feeds/verticals/food/news.xml",
			"Politics":"http://www.huffingtonpost.com/feeds/verticals/politics/news.xml",
			"Religion":"http://www.huffingtonpost.com/feeds/verticals/religion/news.xml",
			"Science":"http://www.huffingtonpost.com/feeds/verticals/science/news.xml",
			"Sports":"http://www.huffingtonpost.com/feeds/verticals/sports/news.xml",
			"Style":"http://www.huffingtonpost.com/feeds/verticals/style/news.xml",
			"Technology":"http://www.huffingtonpost.com/feeds/verticals/technology/news.xml",
			"Travel":"http://www.huffingtonpost.com/feeds/verticals/travel/news.xml",
			"World":"http://www.huffingtonpost.com/feeds/verticals/world/news.xml"
		}

	def fetch_articles(self):
		"""
		Fetches articles from each item in each RSS feed in 'categories'
		"""
		#fetch from each category
		for category in default_categories:
			#check if HuffPost has this category
			if not category in self.categories:
				print "Huff post does not have cat:",category
				continue
			fparser = feedparser.parse(self.categories[category])
			if not fparser.status == 200:
				print "Unable to init feedparser on:",category
				continue
			items = fparser['items']
			print "Processing HuffingtonPost-- Category:",category," article count:",len(items)
			for item in items:
				pub_date = datetime.datetime.strptime(item.published,'%a, %d %b %Y %H:%M:%S -0400')
				raw_text = item['summary_detail'].value
				scrubbed_text  = remove_tags(raw_text)
				a = {
				  'id':item.id,
				  'title':item.title,
				  'author':item.author,
				  'category':category,
				  'date_published':pub_date,
				  'text':scrubbed_text,
				  'source_url':item.id,
				  'media_source':"HuffingtonPost"
				  }

				add_to_db(a,item.id)
				# if not db.text.find({'id':item.id}):
				# 	db.text.insert(a)

class CNN():
	def __init__(self,default_categories):
		self.name = "CNN"
		self.default_categories = default_categories
		self.articles=[]
		self.categories = {
			'Economics':"http://rss.cnn.com/rss/money_latest.rss",
			'Entertainment':"http://rss.cnn.com/rss/cnn_showbiz.rss",
			"Politics":"http://rss.cnn.com/rss/cnn_allpolitics.rss",
			"Technology":"http://rss.cnn.com/rss/cnn_tech.rss",
			"Travel":"http://rss.cnn.com/rss/cnn_travel.rss",
			"World":"http://rss.cnn.com/rss/cnn_world.rss"
		}

	def fetch_articles(self):
		"""
		Fetches articles from each item in each RSS feed in 'categories'
		"""
		#fetch from each category
		for category in default_categories:
			if not category in self.categories:
				print "CNN does not have cat:",category
				continue
			print self.categories[category]
			response = requests.get(self.categories[category])
			if not response.status_code == 200:
				print "Unable to reach CNN feed:",category
				continue
			soup = BeautifulSoup(response.content)
			items = soup.findAll("item")
			print "Processing CNN-- Category:",category," article count:",len(items)
			for item in items:
				try:
					title = item.findAll("title")[0].text
					pub_date = item.findAll("pubdate")[0].text
					#now follow the link inside of this
					#to get the full text

					#Hope this is unique... think it is!
					item_id = title
					link = item.findAll('feedburner:origlink')[0].text

					#get actual story
					response2 = requests.get(link)
					if not response.status_code == 200:
						print "Unable to reach CNN feed-article:",link
						continue

					#get the story!
					soup2 = BeautifulSoup(response2.content)

					#decide what id to pull from. First approach is
					#to just try both..
					raw_text_1 = soup2.findAll(id='storytext')
					raw_text_2 = soup2.findAll('div',{'class':"cnn_strycntntlft"})
					raw_text = ""
					if raw_text_1:
						raw_text = raw_text_1
					elif raw_text_2:
						raw_text = raw_text_2
					else:
						print "Unable to find text of article:",title
						continue

					scrubbed_text = remove_tags(str(raw_text))
					author = soup2.findAll('meta',{'name':'author'})[0].text
					a = {
					  'id':item_id,
					  'title':title,
					  'author':author,
					  'category':category,
					  'date_published':pub_date,
					  'text':scrubbed_text,
					  'source_url':link,
					  'media_source':"CNN"
					}
					add_to_db(a,item_id)
					# if not db.text.find({'id':item.id}):
					# 	db.text.insert(a)
				except:
					print "Unable to process CNN article:",item.findAll("title")[0].text




class BBC():
	def __init__(self,default_categories):
		self.name = "BBC"
		self.default_categories = default_categories
		self.articles=[]
		self.categories = {
			'Economics':"http://feeds.bbci.co.uk/news/business/economy/rss.xml",
			'Entertainment':"http://feeds.bbci.co.uk/news/entertainment_and_arts/rss.xml",
			"Politics":"http://feeds.bbci.co.uk/news/politics/rss.xml",
			"Science":"http://www.bbc.co.uk/science/0/rss.xml",
			"Technology":"http://feeds.bbci.co.uk/news/technology/rss.xml",
			"World":"http://feeds.bbci.co.uk/news/rss.xml"
		}

	def fetch_articles(self):
		"""
		Fetches articles from each item in each RSS feed in 'categories'
		"""
		#fetch from each category
		for category in default_categories:
			if not category in self.categories:
				print "BBC does not have cat:",category
				continue
			response = requests.get(self.categories[category])
			if not response.status_code == 200:
				print "Unable to reach BBC feed:",category
				continue
			soup = BeautifulSoup(response.content)
			items = soup.findAll("item")
			print "Processing BBC-- Category:",category," article count:",len(items)
			for item in items:
				try:
					title = item.findAll("title")[0].text
					print "PROCESSING: TITLE=",title
					pub_date = item.findAll("pubdate")[0].text
					#now follow the link inside of this
					#to get the full text

					#Hope this is unique... think it is!
					item_id = title
					link = item.findAll('guid')[0].text

					#NOTE: BBC Articles do not list authors!

					#get actual story
					response2 = requests.get(link)
					if not response.status_code == 200:
						print "Unable to reach BBC feed-article:",link
						continue

					#get the story!
					soup2 = BeautifulSoup(response2.content)

					#decide what id to pull from. First approach is
					#to just try both..
					raw_text_1 = soup2.findAll('div',{'class':'story-body'})
					# raw_text_2 = soup2.findAll('div',{'class':"cnn_strycntntlft"})
					raw_text = ""
					if raw_text_1:
						raw_text = raw_text_1
					# elif raw_text_2:
						# raw_text = raw_text_2
					else:
						print "Unable to find text of article:",title
						continue

					scrubbed_text = remove_tags(str(raw_text))
					a = {
					  'id':item_id,
					  'title':title,
					  'author':None,
					  'category':category,
					  'date_published':pub_date,
					  'text':scrubbed_text,
					  'source_url':link,
					  'media_source':"BBC"
					}
					add_to_db(a,item_id)
					# if not db.text.find({'id':item.id}):
					# 	db.text.insert(a)

				except:
					print "Unable to process BBC article:",item.findAll("title")[0].text

class FOXNews():
	def __init__(self,default_categories):
		self.name = "FOXNews"
		self.default_categories = default_categories
		self.articles = []
		self.categories = {
			'Economics':"http://feeds.foxnews.com/foxnews/business",
			'Entertainment':"http://feeds.foxnews.com/foxnews/entertainment",
			'Politics':"http://feeds.foxnews.com/foxnews/politics",
			'Science':"http://feeds.foxnews.com/foxnews/scitech",
			'Technology':"http://feeds.foxnews.com/foxnews/scitech",
			'World':"http://feeds.foxnews.com/foxnews/world"
		}

	def fetch_articles(self):
		"""
		Fetches articles from each item in each RSS feed in 'categories'
		"""
		#fetch from each category
		for category in default_categories:
			if not category in self.categories:
				print "FOXNews does not have cat:", category
				continue
			response = requests.get(self.categories[category])
			if not response.status_code == 200:
				print "Unable to reach FOXNews feed:", category
				continue
			soup = BeautifulSoup(response.content)
			items = soup.findAll("item")
			print "Processing FOXNews-- Category:",category," article count:",len(items)
			for item in items:
				try:
					title = item.findAll("title")[0].text
					pub_date = item.findAll("pubdate")[0].text
					#now follow the link inside of this
					#to get the full text

					#Hope this is unique... think it is!
					item_id = title
					link = item.findAll('feedburner:origlink')[0].text

					#get actual story
					response2 = requests.get(link)
					if not response.status_code == 200:
						print "Unable to reach FOXNews feed-article:",link
						continue

					#get the story!
					soup2 = BeautifulSoup(response2.content)

					raw_text = soup2.findAll('div',{'itemprop':"articleBody"})
					if not raw_text:
						print "Unable to find text of article:",title
					scrubbed_text = remove_tags(str(raw_text))
					author = None
					a = {
					  'id':item_id,
					  'title':title,
					  'author':author,
					  'category':category,
					  'date_published':pub_date,
					  'text':scrubbed_text,
					  'source_url':link,
					  'media_source':"FOXNews"
					}
					add_to_db(a,item_id)
				except:
					print "Unable to process FOXNews article:",item.findAll("title")[0].text

