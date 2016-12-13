#Author: Pradeep Ravilla
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

def gettopBusiness(businessDict,topCategories):
	topCategoryBusinessDict = {}
	for key, value in businessDict.iteritems():
		currentObj = value
		if any(x in topCategories for x in value.categories):
			topCategoryBusinessDict[key] = value
	return topCategoryBusinessDict


def main():
	startTime = time()
	businessDict = {}
	with open("input/Dataset/businessDict.pickle") as f:
		businessDict = pickle.load(f)
		print "Reading pickle completed in "+str(time() - startTime)
	topCategories = []
	with open("top40Categorieslist.pickle") as f:
		topCategories = pickle.load(f)
		print "Reading top categories from pickle completed"
	topCategoryBusinessDict = gettopBusiness(businessDict,topCategories)

	with open("business_with_only_top_cat.pickle",'w') as f:
		pickle.dump(topCategoryBusinessDict,f)

