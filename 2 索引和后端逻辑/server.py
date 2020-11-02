
from flask import Flask,request,jsonify
import json
from flask_cors import *
from pymongo import MongoClient
from functools import cmp_to_key
import jieba

conn = MongoClient("127.0.0.1",27017)
db=conn.sinadb

 
app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False
CORS(app, supports_credentials=True)

 
@app.route('/ping')
def hello_world():
    return 'Hello World!'

def cmp_time(t1,t2):
    t1 = t1['created_at']
    t2 = t2['created_at']
    print(t1)
    print(t2)
    # if t1 == None or t2 == None:
    #     return 0
    year1 = t1[0:4]
    year2 = t2[0:4]
    month1 = t1[5:7]
 
    month2 = t2[5:7]
    day1 = t1[8:10]
    day2 = t2[8:10]
 
    hour1 = t1[11:13]
    hour2 = t2[11:13]
    min1 = t1[14:16]
    min2 = t2[14:16]

    if year1 != year2 :
        return int(year2) - int(year1)
    if month1 != month2 :
        return int(month2) - int(month1)
    if day1 != day2 :
        return int(day2) - int(day1)
    if hour1 != hour2 :
        return int(hour2) - int(hour1)
    if min1 != min2 :
        return int(min2) - int(min1)
    return 0

def content_cmp(c1,c2):
	pass

def comment_cmp(t1,t2):
    t1 = t1['comment_num']
    t2 = t2['comment_num']

    return int(t2)-int(t1)

def search_weibo(word):
	print("weibo")
	index = 1
	first_page_list = []
	for indexing in db.tweets_indexing.find({"word":word+""}).limit(200) :
		
		t_id = indexing['t_id']
		if index <=200:
			first_page_list.append(t_id)
		else:
			break
		index = index +1
	return first_page_list

def search_weibo_content(word):
	print("weibo")
	index = 1
	first_page_list = []
	for indexing in db.tweets_indexing.find({"word":word+""}).limit(200) :
		
		t_id = indexing['t_id']
		if index <=200:
			first_page_list.append(indexing)
		else:
			break
		index = index +1
	return first_page_list


def searchWord(word):
	stopword_file = open("stop_words.txt","r")

	stop_word_list = []


	for line in stopword_file.readlines():
	    stop_word_list.append(line.replace("\n",""))
	stopword_file.close()

	#print(stop_word_list)
	# for word in words:


	results = []
	for result in jieba.cut(word):
	#print(result)
	    if result in stop_word_list:
	        continue
	    results.append(result)
	    # print(result)

	if len(results) == 0:
		return search_weibo_content(results[0])

	final_list = []
	for result in results:
		current = search_weibo(result)
		print(result)
		print(len(current))
		if len(final_list) == 0:
			final_list = current
		else:
			final_list = list(set(final_list).intersection(set(current)))

	final_result = []
	for id_1 in final_list:
		for indexing in db.Tweets.find({"_id":id_1}) :
			final_result.append(indexing)

	return final_result

@app.route('/search_tweets')
def search_tweets():
	word = request.args.get('word')
	time =  request.args.get('time')
	orderby =  request.args.get('order') # time content comment
	region =  request.args.get('region') #1:hashtag 2:weibo 3:comment
	print(word)
	print(region)
	print(time)
	print(orderby)
	result = {}
	result['data'] = []
	first_page_list = []
	index = 1

	if region == "1":
		print("hashtag")
		for indexing in db.tweets_hash_tag.find({"word":word+""}).limit(100) :
			if time in ["2016","2017","2018","2019"]:
				if indexing['created_at'] != time:
					continue
			t_id = indexing['t_id']
			if index <=100:
				first_page_list.append(indexing)
			else:
				break
			index = index +1
	elif region == "2":
		print("weibo")
		first_page_list  = searchWord(word)
		for item in first_page_list:
			for info in db.Information.find({"_id":item["user_id"]}):
				item['user_id'] = info['nick_name']
				break
		# print(txt)
		# for indexing in db.tweets_indexing.find({"word":word+""}).limit(100) :
		# 	if time in ["2016","2017","2018","2019"]:
		# 		if indexing['created_at'] != time:
		# 			continue
		# 	t_id = indexing['t_id']
		# 	if index <=100:
		# 		first_page_list.append(indexing)
		# 	else:
		# 		break
		# 	index = index +1
	elif region == "3":
		print("comments")
		for indexing in db.comments_indexing.find({"word":word+""}).limit(100) :
			if time in ["2016","2017","2018","2019"]:
				if indexing['created_at'] != time:
					continue
			t_id = indexing['t_id']
			if index <=100:
				first_page_list.append(indexing)
			else:
				break
			index = index +1


		# print(indexing)
	# print(first_page_list)
	if region == "3":
		for item in first_page_list:
			# print(item)
			for tweet in db.Comments.find({"_id":item["t_id"]}):
				result['data'].append(tweet)
				tweet['user_id'] = tweet['comment_user_id']
				tweet['weibo_url'] = ""
				tweet['comment_num'] = ""
				tweet['tool'] = ""

				# print(tweet['content'])
				# print(tweet['created_at'])
				break
	elif region == "1":
		for item in first_page_list:
			# print(item)
			for tweet in db.Tweets.find({"_id":item["t_id"]}):
				result['data'].append(tweet)

				  # time content comment
				
				print(tweet['content'])
				print(tweet['created_at'])
				break
		if orderby == "time":
			result['data'].sort(key=cmp_to_key(cmp_time))
		if orderby == "comment":
			result['data'].sort(key=cmp_to_key(comment_cmp))
	else:
		result['data'] = first_page_list
		if orderby == "time":
			result['data'].sort(key=cmp_to_key(cmp_time))
		if orderby == "comment":
			result['data'].sort(key=cmp_to_key(comment_cmp))

			
	return jsonify(result)
 
if __name__ == '__main__':

    app.run(host='0.0.0.0', port=8080,debug=True)
