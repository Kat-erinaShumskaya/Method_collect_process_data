# 6) Написать запрос к базе, который вернет список профилей, на кого подписан указанный пользователь
import pymongo
from pymongo import MongoClient
from pprint import pprint

client = MongoClient('127.0.0.1', 27017)
main_username = 'thearchitectsdiaryin'
db = client['instagram21_1351']
instagram = db.instagram

for doc in instagram.find({'main_username': main_username, 'friend_type': 'following'}):
     pprint(doc)