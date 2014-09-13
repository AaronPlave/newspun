import feedparser
import re
import time
import datetime

default_categories = ['Economics','Entertainment','Food',
		'Politics','Religion','Science','Sports','Style',
		'Technology','Travel','World'
]

class Media():
	def __init__(self,sources,last_update,categories):
		self.sources = ['HuffingtonPost']
		self.last_update = last_update

	def update_all():
		"""
		Updates all news sources and adds them to the db
		"""
		for source in self.sources:
			update_source(source)


	def update_source(source):
		if source == "HuffingtonPost":
			huff = HuffingtonPost()
			huff.fetch_articles()
			
			# update the last update time  
			self.last_update = time.time()

			# create the MediaSource Object
			ms = MediaSource(
					name="HuffingtonPost",
					articles=huff.articles,
					categories=huff.categories.keys()
				)
			insert_ms(ms)

	def insert_ms(ms):
		#INSERT DB HERE TYLER!!!!!!!!!!!!!!!!!!!!
		# db.text....upsert(ms)
		pass




#define article class
class Article():
	"""
	Article docstring fill in later.
	@Id is some unique identifier for the article
	@Text is main text of article
	@Source_url is the origin of the article
	"""
	def __init__(self,id,title,author,category,date_published,text,source_url):
		self.id = id
		self.title = title
		self.author = author
		self.date_published = date_published
		self.text = text
		self.source_url = source_url

#define source class
class MediaSource():
	"""
	MediaSource docstring fill in later.
	@Name is a string identifier for the source, e.g. 'CNN' or 'MSNBC'
	@Articles is a list of article objects associated with this media source
	@Categories is a list of categories available for this media source
	"""
	def __init__(self,name,articles,categories,last_updated):
		self.name = name
		self.articles = articles
		self.last_updated = last_updated


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
			for item in items:
				# parse date
				print "Processing",item.title
				pub_date = datetime.datetime.strptime(item.published,'%a, %d %b %Y %H:%M:%S -0400')
				raw_text = item['summary_detail'].value
				scrubbed_text  = remove_tags(raw_text)
				article = Article(
					id=item.id,
					title=item.title,
					author=item.author,
					category=category,
					date_published=pub_date,
					text=scrubbed_text,
					source_url=item.id
				)
				self.articles.append(article)

			#try to avoid rate limit...
			time.sleep(.25)

		# return self.articles


 