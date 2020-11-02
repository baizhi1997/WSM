import jieba

from flask import Flask,request,jsonify
import json
from flask_cors import *
from pymongo import MongoClient
from functools import cmp_to_key

conn = MongoClient("127.0.0.1",27017)
db=conn.sinadb


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

word = "发生火灾"

# #import stop words
# words = ["上海今天堵车了吗","购物网站打折吧","今年毕业情况如何"]

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


txt  = searchWord(word)
for item in txt:
	for info in db.Information.find({"_id":item["user_id"]}):
		item['user_id'] = info['nick_name']
		break
print(txt)