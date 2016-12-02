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


ERROR_INVALID_NAME = 123
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
		client = MongoClient(serverSelectionTimeoutMS=max_sev_sel_Delay)
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


def get_business(db):
	f = open('businessid.csv','w')
	for business in db.business.find({},{"business_id":1,"_id":0}):
		f.write(business['business_id'] + '\n')
	f.close()

def get_categories(db):
	collection = db.business
	f1 = open("reviews_task1.csv","w")
	f2 = open("reviews_task1_deviated.csv","w")
	count = 0
	for business in collection.find({},{"business_id":1,"categories":1}):
		for reviews in db.reviews.find({"business_id":business['business_id']},{"text":1,"business_id":1}):
			if (len(business['categories']) > 1):
				temp = unicodedata.normalize('NFKD',reviews['text']).encode('ascii','ignore').decode('utf-8')
				review_text = re.sub(r'[^\w -]','',temp)
				business_id = business["business_id"]
				for categories in business["categories"]:
					if((len(business['business_id']) + len(reviews['text'])) != (len(business_id) + len(review_text))):
						f2.write(str(business['business_id'].encode('utf8'))+', "'+str(reviews['text'].encode('utf8'))+'" ,'+str(categories)+'\n')
					f1.write(business_id+','+review_text+','+str(categories)+'\n')
				count += 1
	f1.close()
	f2.close()

if not sys.argv[1]:
	wrk_directory = os.getcwd()
else:
	wrk_directory = sys.argv[1]

# Change the working directory, failure to do so, exits the program
print("Changing the working directory to the specified path ...",end=" ")
try:
	os.chdir(output_path)
	print("done")
except:
	print("error")
	error_exit()

try:
	submit_and_monitor_thread (get_business,(db,))
	submit_and_monitor_thread (get_categories,(db,))
except:
	error_exit()

graceful_exit()