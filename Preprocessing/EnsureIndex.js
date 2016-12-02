use yelp;
db.reviews.ensureIndex({"business_id":1})
db.tip.ensureIndex({"business_id":1})