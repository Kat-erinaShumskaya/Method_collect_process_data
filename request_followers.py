# 5) Написать запрос к базе, который вернет список подписчиков только указанного пользователя
import pymongo
from pymongo import MongoClient
from pprint import pprint

client = MongoClient('127.0.0.1', 27017)
# main_username = input('Введите имя пользователя: ')
main_username = 'ai_machine_learning'
db = client['instagram21_1351']
instagram = db.instagram

# for doc in instagram.find({'$and': [{'main_username': main_username, 'friend_type': 'followers'}]}):
#      pprint(doc)
for doc in instagram.find({'main_username': main_username, 'friend_type': 'followers'}):
     pprint(doc)

