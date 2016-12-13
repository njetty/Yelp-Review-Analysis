#Author: Pradeep Ravilla

from pymongo import MongoClient
from collections import defaultdict
connection = MongoClient("mongodb://silo.soic.indiana.edu:31786")
db = connection.yelp.business
categories = defaultdict()
businesses = defaultdict()

cursor = db.find()
index = 0
count = cursor.count()
while index != count:
	doc = cursor[index]
	businesses[doc['business_id']] = doc['categories']
print len(businesses), count

cursor.close()

db = connection.yelp.reviews
cursor = db.find()
index = 0
count = cursor.count()
while index != count:
	doc = cursor[index]
	cur_cat = businesses[doc['business_id']]
	for cat in cur_cat:
		categories[cat] += 1
cursor.close()

with open("business_categories.pickle",'w') as picklefile:
	pickle.dump(businesses,picklefile)

with open("category_review_counts.pickle",'w') as picklefile:
	pickle.dump(categories,picklefile)
