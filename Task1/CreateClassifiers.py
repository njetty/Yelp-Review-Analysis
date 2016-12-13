#This file creates the classifiers and makes predictions
#Authors: Naveen Jetty & Pradeep Ravilla

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import MultinomialNB 
from sklearn.multiclass import OneVsRestClassifier 
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn import cross_validation
from sklearn import metrics

import pickle
from pprint import pprint
from time import time
import os,sys

class Business:
    def __init__(self, business_id, stars, name, categories):
        self.id = business_id
        self.stars = stars
        self.name = name
        self.categories = categories
        self.cleanReviews = [] #List of list of tokenized words
        self.cleanTips = []

def createCorpus(businessDict):
    corpus = []
    target = []
    startTime = time()
    print "Started creating corpus ..." 
    for key, value in businessDict.iteritems():
        currentObj = value
        #Combining all reviews in one big string
        tipsAndReviews = ""
        tipsAll = ""
        for tip in currentObj.cleanTips:
            tipsAll += tip+" "
        reviewsAll = ""
        for review in currentObj.cleanReviews:
            reviewsAll += review+" "
        corpus.append(tipsAll+" "+reviewsAll)
        target.append(currentObj.categories)
    
    print "Corpus created in "+str(time() - startTime)
    return (corpus, target)

def main():
    xExists = os.path.exists("input/Dataset/XAll.processed")
    yExists = os.path.exists("input/Dataset/YAll.processed")
    if not xExists and not yExists:
        startTime= time()
        businessDict = {}
        with open("input/Dataset/businessDict.pickle") as f:
            businessDict = pickle.load(f)
            print "Reading pickle completed in "+str(time() - startTime)
        XAndY = createCorpus(businessDict)
        X = XAndY[0]
        y = XAndY[1]
        
        print "Size of X : " + str(len(X))
        print "Size of y : " + str(len(y))
        
        vectorizer = TfidfVectorizer(stop_words="english", min_df=0.0009)
        XAll = vectorizer.fit_transform(X)
        mlb = MultiLabelBinarizer()
        yAll = mlb.fit_transform(y)
        
        with open("input/Dataset/XAll.processed", 'wb') as f:
            pickle.dump(XAll, f)
        
        with open("input/Dataset/YAll.processed", 'wb') as f:
            pickle.dump(yAll, f)
        print "Data Pickled "
    else:
        print "Loading XAll and YAll from pickled data"
        
        with open("input/Dataset/XAll.processed") as f:
            XAll = pickle.load(f)

        with open("input/Dataset/YAll.processed") as f:
            yAll = pickle.load(f)
    
    xTrain, xTest, yTrain, yTest = cross_validation.train_test_split(XAll, yAll, test_size=0.2)
##### SVC 
    classifierTime = time()
    print "Training Classifier"
    svc80Exists = os.path.exists("input/Dataset/svc80.classifier")
    if not svc80Exists:
        svcClassifier = OneVsRestClassifier(LinearSVC()).fit(xTrain, yTrain)
        print "Training classifier took : "+str(time()- classifierTime)
        with open("input/Dataset/svc80.classifier", 'w') as f:
            pickle.dump(svcClassifier, f)
        print "Classifier dumped on disk"
    else:
        print "Loading SVC 80 Classifier from pickle"
        with open("input/Dataset/svc80.classifier") as f:
            svcClassifier = pickle.load(f)

    print "Predicting ... "
    predicted = svcClassifier.predict(xTest)
    with open("input/Dataset/Task1/Results/svc20Test.ReviewsTips", 'w') as f:
        f.write(metrics.classification_report(yTest, predicted, target_names=mlb.classes_))

    
    xTrain, xTest, yTrain, yTest = cross_validation.train_test_split(XAll, yAll, test_size=0.4)
##### SVC 
    classifierTime = time()
    print "Training Classifier"
    svc60Exists = os.path.exists("input/Dataset/svc60.classifier")
    if not svc60Exists:
        svcClassifier = OneVsRestClassifier(LinearSVC()).fit(xTrain, yTrain)
        print "Training classifier took : "+str(time()- classifierTime)
        with open("input/Dataset/svc60.classifier", 'w') as f:
            pickle.dump(svcClassifier, f)
        print "Classifier dumped on disk"    
    else:
        print "Loading SVC 60 from pickle"
        with open("input/Dataset/svc60.classfier") as f:
            svcClassifier = pickle.load(f)

    print "Predicting ... "
    predicted = svcClassifier.predict(xTest)
    with open("input/Dataset/Task1/Results/svc40Test.ReviewsTips", 'w') as f:
        f.write(metrics.classification_report(yTest, predicted, target_names=mlb.classes_))

    
    xTrain, xTest, yTrain, yTest = cross_validation.train_test_split(XAll, yAll, test_size=0.4)

##### MultinomialNB 
    classifierTime = time()
    print "Training Classifier"
    svcNB60Exists = os.path.exists("input/Dataset/MultinomialNB60.classifier")
    if not svcNB60Exists:
        svcClassifier = OneVsRestClassifier(MultinomialNB()).fit(xTrain, yTrain)
        print "Training classifier took : "+str(time()- classifierTime)
        with open("input/Dataset/MultinomialNB60.classifier", 'w') as f:
            pickle.dump(svcClassifier, f)
        print "Classifier dumped on disk"    
    else:
        print "Loading Multinomial NB60 from pickle"
        with open("input/Dataset/MultinomialNB60.classifier") as f:
            svcClassifier = pickle.load(f)

    print "Predicting ... "
    predicted = svcClassifier.predict(xTest)
    with open("input/Dataset/Task1/Results/MNB40Test.ReviewsTips", 'w') as f:
        f.write(metrics.classification_report(yTest, predicted, target_names=mlb.classes_))
    
    
    xTrain, xTest, yTrain, yTest = cross_validation.train_test_split(XAll, yAll, test_size=0.2)

##### MultinomialNB 
    classifierTime = time()
    print "Training Classifier"
    if not os.path.exists("input/Dataset/MultinomialNB80.classifier"):
        svcClassifier = OneVsRestClassifier(MultinomialNB()).fit(xTrain, yTrain)
        print "Training classifier took : "+str(time()- classifierTime)
        with open("input/Dataset/MultinomialNB80.classifier", 'w') as f:
            pickle.dump(svcClassifier, f)
        print "Classifier dumped on disk"
    else:
        print "Loading Multinomial NB80 from pickle"
        with open("input/Dataset/MultinomialNB80.classifier") as f:
            svcClassifier = pickle.load(f)
            
    print "Predicting ... "
    predicted = svcClassifier.predict(xTest)
    with open("input/Dataset/Task1/Results/MNB20Test.ReviewsTips", 'w') as f:
        f.write(metrics.classification_report(yTest, predicted, target_names=mlb.classes_))
       
    
if __name__ == "__main__": main()
