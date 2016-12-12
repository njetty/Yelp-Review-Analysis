#TO PERFORM MODEL EVALUATION
evaluation<-function(pred,actual){
  library(caret)
  library(e1071)
  conf=table(pred,actual)
  f.conf=confusionMatrix(conf)
  print(f.conf)
  
  ##OR
  accuracy=sum(diag(conf))/sum(conf)
  cat("ACCURACY\n",accuracy,"\n")
  precision=diag(conf)/rowSums(conf)
  cat("PRECISION\n",precision,"\n")
  recall=diag(conf)/colSums(conf)
  cat("RECALL\n",recall,"\n")
}


#Read the csv file here, give your own path.
data=read.csv(file="../input.csv")
#randomsampling 1 lakh data points
data=data[sample(nrow(data),100000),]
print(colnames(data))
#random sample of 40k test data.
test=data[sample(nrow(data),40000),]
#storing the test ratings to find our accuracies.
actual=test$stars.y
#deleting test ratings from the test data.
test$stars=NULL


#softmax regression.
library(nnet)
model=multinom(stars.y~., data = data, MaxNWts = 8540)
#predict the test data.
p1=predict(model,test, probability = TRUE)
p1=as.numeric(p1)
x=evaluation(p1,actual)


#Naive Bayes
require(klaR)
modelNaive=naiveBayes(as.factor(stars.y)~.,data=data)
pNaive=predict(modelNaive,test)
pNaive=as.numeric(pNaive)
x=evaluation(pNaive,actual)