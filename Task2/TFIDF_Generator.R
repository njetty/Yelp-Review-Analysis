library(mongolite)
library(tm)

#Read reviews data from mongodb
con <- mongo("reviews", url = "mongodb://silo.soic.indiana.edu:31786/yelp")
data <- con$find(fields = '{"_id":0, "text":1, "stars":1, "review_id" : 1}', limit = 500000)
myReader <- readTabular(mapping=list(id="review_id", content="text", data = "stars"))

#Make a corpus object from a text vector
dd <- Corpus(DataframeSource(data), readerControl = list(reader=myReader))

#Clean the text
dd <- tm_map(dd, content_transformer(stripWhitespace))
dd <- tm_map(dd, content_transformer(tolower))
dd <- tm_map(dd, content_transformer(removePunctuation))
dd <- tm_map(dd, removeWords, stopwords("english"))
dd <- tm_map(dd, content_transformer(stemDocument))
dd <- tm_map(dd, content_transformer(removeNumbers))

#Generate DocumentTermMatrix
dtm <- DocumentTermMatrix(dd, control = list(weighting = weightTfIdf))
dtm <- removeSparseTerms(dtm,0.99)
m <- inspect(dtm)
DF <- as.data.frame(m, stringsAsFactors = FALSE)

# Append stars column as classification
DF <- data.frame("review_id"=rownames(DF), DF)
data <- subset(data, select=-c(text))
merged <- merge(DF, data, by = "review_id")
write.csv(merged,"../output.csv")