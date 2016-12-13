#Author Naveen Jetty
# Get the categories from the businessDict.pickle file
import pickle
from pprint import pprint
from time import time
import sys
from collections import defaultdict

class Business:
	def __init__(self, business_id, stars, name, categories):
		self.id = business_id
		self.stars = stars
		self.name = name
		self.categories = categories
		self.cleanReviews = [] #List of list of tokenized words
		self.cleanTips = []

def getCategories(businessDict):
	categories = defaultdict()
	for key, value in businessDict.iteritems():
		currentObj = value
		for category in value.categories:
			categories[category] += len(value.cleanReviews)
	return categories

def main():
	startTime = time()
	businessDict = {}
	with open("input/Dataset/businessDict.pickle") as f:
		businessDict = pickle.load(f)
		print "Reading pickle completed in "+str(time() - startTime)

	categories = getCategories(businessDict)
	with open("categorycount.pickle",'w') as picklefile:
		pickle.dump(categories,picklefile)

	for key, value in categories.iteritems():
		print key+": "+str(value)

main()
