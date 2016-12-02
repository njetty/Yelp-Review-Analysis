import pymongo
from pymongo import MongoClient
import os
import sys
import errno

ERROR_INVALID_NAME = 123

def call(*argv, **kwargs):
	def call_fn(fn):
		return fn(*argv, **kwargs)
	return call_fn

@call()
def db():
	max_sev_sel_Delay = 0.1
	try:
		client = MongoClient(serverSelectionTimeoutMS=max_sev_sel_Delay)
		client.server_info()
		print("Connection to Mongo Established")
		db = client.yelp
		return db
	except pymongo.errors.ServerSelectionTimeoutError as e:
		print("Could not establish connection to Mongo, terminating the process")
		sys.exit(0)

@call()
def output_path():
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
		print("Exiting the program")
		sys.exit(0)
	else:
		return sys.argv[1]


def get_business(db):
	collection = db.business
	count = 0
	for business in collection.find():
		count+=1
	return count

if not sys.argv[1]:
	wrk_directory = os.getcwd()
else:
	wrk_directory = sys.argv[1]


print(get_business(db))