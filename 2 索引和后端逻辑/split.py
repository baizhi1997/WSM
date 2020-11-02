from pymongo import MongoClient
import jieba

def split(str):
	return list(jieba.cut_for_search(str))

conn = MongoClient("127.0.0.1",27017)
db=conn.sinadb

tweets = db.Tweets
comments = db.Comments
# db.tweets_indexing.drop()
# db.tweets_indexing_dict.drop()
# db.comments_indexing.drop()
# db.comments_indexing_dict.drop()


# count = 1
# tweet_dict = dict()
# for  item in tweets.find(no_cursor_timeout = True):
# 	print(count)

# 	# if count < 26761:
# 	# 	count = count +1
# 	# 	continue
# 	count = count +1
# 	# print(item)
# 	_id1 = item['_id']
# 	content = item['content']
# 	created_at = item['created_at'].split("-")[0]
# 	weibo_url = item['weibo_url']
# 	# print(content)
# 	for word in split(content):
# 		if word in [" ","，","《","》","。","#","【","】","！"]:
# 			continue
# 		if word not in tweet_dict.keys():
# 			tweet_dict[word] = []
# 		if len(tweet_dict[word])!=0 and tweet_dict[word][-1]==_id1:
# 			continue
# 		tweet_dict[word].append(_id1)
# 		# tweet_dict.append()
# 		db.tweets_indexing.insert_one({
# 			"t_id":_id1,
# 			"word":word,
# 			"created_at":created_at,
# 			"weibo_url":weibo_url
# 			})


	# if count >30:
	# 	break

# for word in tweet_dict.keys():

# 	db.tweets_indexing_dict.insert_one({
			
# 				"word":word,
# 				'doc_ids':tweet_dict[word]
# 				})
	# break
	# break

# for item in db.tweets_indexing.find():
# 	print(item)


count = 1
tweet_dict = dict()
for  item in comments.find(no_cursor_timeout = True):
	print(count)

	# if count < 26761:
	# 	count = count +1
	# 	continue
	count = count +1
	# print(item)
	_id1 = item['_id']
	content = item['content']
	created_at = item['created_at'].split("-")[0]
	weibo_url = item['weibo_url']
	# print(content)
	for word in split(content):
		if word in [" ","，","《","》","。","#","【","】","！"]:
			continue
		if word not in tweet_dict.keys():
			tweet_dict[word] = []
		if len(tweet_dict[word])!=0 and tweet_dict[word][-1]==_id1:
			continue
		if len(tweet_dict[word])<200:
			tweet_dict[word].append(_id1)
		# tweet_dict.append()
		db.comments_indexing.insert_one({
			"t_id":_id1,
			"word":word,
			"created_at":created_at,
			"weibo_url":weibo_url
			})

	# if count >30:
	# 	break

# for word in tweet_dict.keys():

# 	db.comments_indexing_dict.insert_one({
			
# 				"word":word,
# 				'doc_ids':tweet_dict[word]
# 				})

# def getHashTagContent(str):
#     content = str
#     first_hash_tag = -1
#     second_hash_tag = -1
#     for index,single in zip(range(0,len(content)),content):
#         if single == "#":
#             if first_hash_tag == -1:
#                 first_hash_tag = index
#             else:
#                 second_hash_tag = index
#                 break
#     if first_hash_tag == -1 or second_hash_tag==-1:
#         return ""
#     return content[first_hash_tag+1:second_hash_tag]


# count = 1
# tweet_dict = dict()
# for  item in tweets.find(no_cursor_timeout = True):
# 	print(count)

# 	# if count < 26761:
# 	# 	count = count +1
# 	# 	continue
# 	count = count +1
# 	# print(item)
# 	_id1 = item['_id']
# 	content = item['content']
# 	content = getHashTagContent(content)
# 	if content=="":
# 		continue
# 	created_at = item['created_at'].split("-")[0]
# 	weibo_url = item['weibo_url']
# 	# print(content)
# 	for word in split(content):
# 		if word in [" ","，","《","》","。","#","【","】","！"]:
# 			continue
# 		if word not in tweet_dict.keys():
# 			tweet_dict[word] = []
# 		if len(tweet_dict[word])!=0 and tweet_dict[word][-1]==_id1:
# 			continue
# 		tweet_dict[word].append(_id1)
# 		# tweet_dict.append()
# 		db.tweets_hash_tag.insert_one({
# 			"t_id":_id1,
# 			"word":word,
# 			"created_at":created_at,
# 			"weibo_url":weibo_url
# 			})
