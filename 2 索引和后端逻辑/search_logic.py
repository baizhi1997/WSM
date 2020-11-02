from pymongo import MongoClient

conn = MongoClient("127.0.0.1",27017)
db=conn.sinadb

tweets = db.Tweets
comments = db.Comments

time = "2019"
order ="-1"

first_page_list = []
index = 1
for indexing in db.tweets_indexing.find({"word":"是"}).sort("created_at") :
	if time in ["2016","2017","2018","2019"]:
		if indexing['created_at'] != time:
			continue
	t_id = indexing['t_id']
	if index <=10:
		first_page_list.append(indexing)
	else:
		break
	index = index +1

	# print(indexing)

for item in first_page_list:
	# print(item)
	for tweet in db.Tweets.find({"_id":item["t_id"]}):
		print(tweet['content'])
		print(tweet['created_at'])

		break

# for indexing in db.tweets_indexing_dict.find():
# 	print(indexing)