# Написать приложение, которое собирает основные новости с сайта на выбор news.mail.ru,
# lenta.ru, yandex-новости. Для парсинга использовать XPath. Структура данных должна содержать:
# название источника;
# наименование новости;
# ссылку на новость;
# дата публикации.
# Сложить собранные новости в БД


import pymongo
from pymongo import MongoClient
from pymongo.errors import *
from pprint import pprint
import requests
from lxml import html

client = MongoClient('127.0.0.1', 27017)

db = client['database_news']
news = db.news

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/94.0.4606.85 YaBrowser/21.11.2.773 Yowser/2.5 Safari/537.36'}

response = requests.get('https://lenta.ru/', headers=header)

dom = html.fromstring(response.text)
items = dom.xpath("//div[@class='item']")

for item in items:
    news_dict = {}

    name_news = item.xpath("./a/text()")[0]
    name_news = name_news.replace('\xa0', ' ')
    link = 'https://lenta.ru' + item.xpath(".//a/@href")[0]

    try:
        response1 = requests.get(link, headers=header)
        dom1 = html.fromstring(response1.text)
        date = dom1.xpath("//time[@class ='g-date']/@datetime")
    except:
        date = None

    news_dict['source'] = 'https://lenta.ru'
    news_dict['name_news'] = name_news
    news_dict['link'] = link
    news_dict['date'] = date
    print(news_dict)
    news.insert_one(news_dict)
