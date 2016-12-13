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
  cat("PRECISION",precision,"\n")
  cat("RECALL",recall,"\n")
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


#softmax regression.
library(nnet)
model=multinom(RATING~.,data, MaxNWts = 8540)
#predict the test data.
p1=predict(model,test, probability = TRUE)
predicted=as.numeric(p1)
evaluation(predicted,actual)


#Naive Bayes
require(klaR)
modelNaive=naiveBayes(as.factor(RATING)~.,data=data)
pNaive=predict(modelNaive,test)
pNaive=as.numeric(pNaive)
tab=table(pNaive,actual)
print(tab)
evaluation(pNaive,actual)



#CHI-SQUARED TEST for feature selection.
library(FSelector)#For method
weights<- chi.squared(RATING~., data[1:10000,])
# Print the results
#There are 118 different variables which appears to be dependent variables. 
length(weights$attr_importance[weights$attr_importance>0])
# Select top 118 variables
subset<- cutoff.k(weights, 118)
print(subset)


require(nnet)
#Using new formula
f<- as.simple.formula(subset, "RATING")
modelChiSquared=multinom(formula=f,data, MaxNWts = 8540)
#predict the test data.
p.ChiSquared=predict(modelChiSquared,test, probability = TRUE)
p.ChiSquared=as.numeric(p.ChiSquared)
evaluation(p.ChiSquared,actual)
table(p.ChiSquared,actual)

#Naive Bayes
require(klaR)
f=as.simple.formula(subset,"as.factor(RATING)")
modelNaive.ChiSquared=naiveBayes(formula=f,data=data)
pNaive.ChiSquared=predict(modelNaive.ChiSquared,test)
pNaive.ChiSquared=as.numeric(pNaive.ChiSquared)
evaluation(pNaive.ChiSquared,actual)
table(pNaive.ChiSquared,actual)