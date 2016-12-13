'''
Author: Naveen Jetty
Process: Preprocessing Reviews and Tips and creating input for sklearn classifiers.
Output: Creates a pickle file for a dictionary of Business objects.
'''
import json
from pprint import pprint
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from progressbar import printprogress

import string
import pickle
from time import time,sleep

#Object for storing the business information
class Business:
    def __init__(self, business_id, stars, name, categories):
        self.id = business_id
        self.stars = stars
        self.name = name
        self.categories = categories
        self.cleanReviews = [] #List of list of tokenized words
        self.cleanTips = []


'''Helper functions start'''

#Takes a file path as input and returns a list of all the lines in the file
def readFile(fileAddress):
    t0 = time()
    print "Reading file "+fileAddress
    with open(fileAddress) as f:
        allLines = f.readlines()
        print "Took "+str(time() - t0)+" seconds to read "
    return allLines

#Takes a list of JSON strings, parses them into
# JSON objects and returns the list of parsed JSON objects
def stringToJSONObj(arrayList):
    print "Parsing JSON"
    t0 =time()
    allJSONObj = []
    for row in arrayList:
        #print type(row.decode('utf8'))
        parsedJSON = json.loads(row.decode('utf8')) 
        allJSONObj.append(parsedJSON)
    print "Took "+str(time() - t0)+" seconds to parse JSON"
    return allJSONObj   

# Remove punctuation from a list of tokenized words
# Remove punctuation after counting and extracting sentiment
def removePunctuation(rawTokens):
    exclude = set(string.punctuation)
    cleanTokens = []
    cleanTokens.extend(t for t in rawTokens if t not in exclude)
    return cleanTokens

def removeStopWords(listOfWords):
    temp = [word for word in listOfWords if word not in stopwords.words('english')]
    return temp
        
def countPunctuation(rawTokens):
    print "Can be used to count exclamation marks"
    
def countCapitalizedWords(rawTokens):
    print "Used to count capitalized words"

'''Helper functions section end'''
# Makes use of the helper methods above to transform the raw text to 
# a list of tokens ready to be used as features

def negateWords(s):
    s = s.replace("not ", "not")
    return s

def removeStopwords(wordlist):
    customStopwords = set(stopwords.words('english')) - set(['not'])
    cleanList = [word for word in wordlist if word not in customStopwords]
    return cleanList
    
def removePunctuation(s):
    punct = set(string.punctuation)
    return ''.join(ch for ch in s if ch not in punct)

'''
input: String
output: String
Process: lemmatizes and removes the stopwords from the input
'''
def cleanReview(review):
    lemmatizer = WordNetLemmatizer()
    tokenizer = TweetTokenizer()
    #Skip empty lines
    if review in ['\n', '\r\n']:
        return ""
    line = review.lower() # Task 1
    tokens = tokenizer.tokenize(line) #Task 3
    lemmaTokens = [lemmatizer.lemmatize(token) for token in tokens]  #Task 4
    stopwordsRemoved = removeStopwords(lemmaTokens) #Task 8
    cleanTokens = [removePunctuation(word) for word in stopwordsRemoved]
    s = ""
    for word in cleanTokens:
        s= s+word+" "
    return negateWords(s) #Task 2s

'''
input: String, tokenizer
output: tokenizes the string and removes the stopwords and returns the string
'''
def rawTextToTokens(rawText, tokenizer):
    
    tokenizedText = tokenizer.tokenize(rawText.lower());
    removedStopwords = removeStopWords(tokenizedText)
    #countPunctuations
    cleanText = removePunctuation(removedStopwords)
    return cleanText

def writeDictToFile(DictOfWords):
    with open("output/tempoutput", 'a') as f:
        for key, value in DictOfWords.iteritems():
            print key
            
def main():
    
    startTime = time()
    rawBusiness = stringToJSONObj(readFile("input/Dataset/yelp_academic_dataset_business.json"))
    
    #Create a dictionary of all businesses hashed by ids
    print "Creating Business Objects"
    businessDict = {}
    count = 0
    total = len(rawBusiness)
    for obj in rawBusiness:
        #print obj['business_id']
        businessObj = Business(obj['business_id'], obj['stars'], obj['name'], obj['categories'])
        businessDict[obj['business_id']] = businessObj
        count += 1
        printprogress(count, total, prefix = "Progress:", suffix = "Complete", bar_length = 50)

    
    del rawBusiness #Remove raw business information from memory
    print "done"

    print "Reading Reviews"

    tokenizer = TweetTokenizer()

    reviewErrors = 0
    print "Reading reviews from file ... "
    rawReviews = stringToJSONObj(readFile("input/Dataset/yelp_academic_dataset_review.json"))

    # Insert reviews to their respective Business objects 
    print "Inserting reviews in their respecitive Business Objects"
    count = 0
    total = len(rawReviews)
    for obj in rawReviews:
        businessId = obj['business_id']
        if businessId in businessDict:
            #cleanReviewTokens = rawTextToTokens(obj['text'],tokenizer)
            businessDict[businessId].cleanReviews.append(cleanReview(obj['text']))
        else:
            reviewErrors += 1
        count += 1
        printprogress(count, total, prefix = "Progress:", suffix = "Complete", bar_length = 50)
    print "There were "+str(reviewErrors)+" errors for reviews"        
    del rawReviews # Remove raw review data from memory
    print "Done"

    
    print "Reading Tips"    
    tipsErrors = 0
    rawTips = stringToJSONObj(readFile("input/Dataset/yelp_academic_dataset_tip.json"))
    
    # Insert Tips to their respective Business objects 

    print "Inserting Tips to their respective Business objects"
    count = 0
    total = len(rawTips)
    for obj in rawTips:
        businessId = obj['business_id']
        if businessId in businessDict:
            #cleanTipsTokens = rawTextToTokens(obj['text'],tokenizer)
            businessDict[businessId].cleanTips.append(cleanReview(obj['text']))
        else:
            tipsErrors += 1
        count += 1
        printprogress(count, total, prefix = "Progress:", suffix = "Complete", bar_length = 50)

    print "There were "+str(tipsErrors)+" errors for tips"        
    del rawTips # Remove raw review data from memory
    print "Done"


    print "Dumping objects using pickle"    
    allBusinessIds = businessDict.keys()
    with open("input/Dataset/businessDict.pickle", 'w') as picklefile:    
        pickle.dump(businessDict,picklefile)
    print "Done"

if __name__ == "__main__": 
    main()
