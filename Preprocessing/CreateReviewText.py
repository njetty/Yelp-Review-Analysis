from __future__ import print_function
import pymongo
from pymongo import MongoClient
import os
import sys
import errno
from Multithreading import submit_and_monitor_thread
import codecs
import csv
import unicodedata
import re

CURRENT_WORKING_DIRECTORY = os.getcwd()

def cleanup():
	#This should contain the logic to cleanup before exiting the process
	os.chdir(CURRENT_WORKING_DIRECTORY)

def error_exit():
	cleanup()
	print("Terminating the process due to an error",file=sys.stderr)
	exit(0)

def graceful_exit():
	cleanup()
	print("All processes completed normally, Terminating the process")
	exit(0)

def call(*argv, **kwargs):
	def call_fn(fn):
		return fn(*argv, **kwargs)
	return call_fn

@call()
def db():
	max_sev_sel_Delay = 0.1
	print("Establishing connection to MongoDB Server ...",end=" ")
	try:
		uri = "mongodb://silo.soic.indiana.edu:31786"
		client = MongoClient(uri,serverSelectionTimeoutMS=max_sev_sel_Delay)
		client.server_info()
		db = client.yelp
		print("done")
		return db
	except pymongo.errors.ServerSelectionTimeoutError as e:
		print("error")
		error_exit()

@call()
def output_path() -> str:
	def validate(pathname: str) -> bool:
		try:
			if os.path.exists(pathname):
				return True
			elif os.access(os.path.dirname(pathname),os.W_OK):
				return True
			else:
				return False
		except:
			return False
			
	if len(sys.argv) < 2 or not validate(sys.argv[1]):
		print("The output path is not specified or does not exist")
		error_exit()
	else:
		return sys.argv[1]

@call(db,output_path)
def get_review_text(db,output_path):
	os.chdir(output_path)
	business_collection = db.business
	reviews_collection = db.reviews
	res_count, rev_count = 0, 0
	for business in business_collection.find({"categories":{"$in": ["Restaurants"]}},{"business_id":1,"categories":1}):
		for reviews in reviews_collection.find({"business_id":business['business_id']},{"text":1,"business_id":1,"stars":1}):
			rev_count += 1
		res_count += 1
	print(res_count, "restaurants found")
	print(rev_count, "reviews found")

graceful_exit()