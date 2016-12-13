#Author: Pradeep Ravilla
from pprint import pprint
from time import time
import sys
from collections import defaultdict

categories = defaultdict(int)
with open("categorycount.pickle") as picklefile:
	categories = pickle.load(picklefile)

sortedList = sorted(categories.items(), key = lambda x:x[1], reverse=True)

for cat in sortedList:
	print cat
