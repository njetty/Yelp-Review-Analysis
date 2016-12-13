#TO PERFORM MODEL EVALUATION
evaluation<-function(pred,actual){
  library(caret)
  library(e1071)
  conf=table(pred,actual)
  f.conf=confusionMatrix(conf)
  #print(f.conf)
  
  ##OR
  accuracy=sum(diag(conf))/sum(conf)
  cat("ACCURACY\n",accuracy,"\n")
  precision=diag(conf)/rowSums(conf)
  #cat("PRECISION\n",precision,"\n")
  recall=diag(conf)/colSums(conf)
  #cat("RECALL\n",recall,"\n")
  cat("MEAN PRECISION",mean(precision),"\n")
  cat("MEAN RECALL",mean(recall),"\n")
}


#Read the csv file here, give your own path.
data=read.csv(file="YelpReview.csv",nrows=200000)
#removing reviewIDs
data$REVIEW_ID=NULL
#randomsampling 1 lakh data points
data=data[sample(nrow(data),100000),]
#random sample of 40k test data.
test=data[sample(nrow(data),40000),]
#storing the test ratings to find our accuracies.
actual=test$RATING
#deleting test ratings from the test data.
test$RATING=NULL


#Information Gain computation
library(FSelector)#For method
weights<- information.gain(RATING~., data[1:10000,])
length(weights$attr_importance[weights$attr_importance>0])
# Select top 100 variables
subset<- cutoff.k(weights, 100)

require(nnet)
#Using new formula
f<- as.simple.formula(subset, "RATING")
modelInfoGain=multinom(formula=f,data, MaxNWts = 8540)
#predict the test data.
p.InfoGain=predict(modelInfoGain,test, probability = TRUE)
p.InfoGain=as.numeric(p.InfoGain)
evaluation(p.InfoGain,actual)


#Naive Bayes
require(klaR)
f=as.simple.formula(subset,"as.factor(RATING)")
modelNaive.InfoGain=naiveBayes(formula=f,data=data)
pNaive.InfoGain=predict(modelNaive.InfoGain,test)
pNaive.InfoGain=as.numeric(pNaive.InfoGain)
evaluation(pNaive.InfoGain,actual)