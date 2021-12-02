# 1. Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и реализовать функцию,
# которая будет добавлять только новые вакансии/продукты в вашу базу.
# 2. Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой
# больше введённой суммы (необходимо анализировать оба поля зарплаты). Для тех, кто выполнил задание
# с Росконтролем - напишите запрос для поиска продуктов с рейтингом не ниже введенного или качеством
# не ниже введенного (то есть цифра вводится одна, а запрос проверяет оба поля)

import pymongo
from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup
from pprint import pprint
from pymongo.errors import *
import requests
from bs4 import BeautifulSoup
import re


def search_vacancy(comp_sum):
    for product in products.find({'$or': [{'minimal_compensation': {'$gte': comp_sum}},
                                          {'maximal_compensation': {'$gte': comp_sum}}]}):
        pprint(product)


client = MongoClient('127.0.0.1', 27017)

db = client['database_products']
products = db.products
products.create_index([('name_of_vacancy', pymongo.TEXT)], name='search_index', unique=True)

url = 'https://spb.hh.ru'

search_item = 'Data Science'

params = {
    'area': 2,
    'fromSearchLine': 'true',
    'text': search_item,
    'page': 0
}

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/94.0.4606.85 YaBrowser/21.11.2.773 Yowser/2.5 Safari/537.36'}

response = requests.get(url + '/search/vacancy/', params=params, headers=headers)

dom = BeautifulSoup(response.text, 'html.parser')

pages = dom.find_all('div', {'class', 'pager'})

number_pages = 0
for p in pages:
    tmp = p.find_all('a')
    for t in tmp:
        if t.text.isdigit():
            number_pages = int(t.text)

vacancy_list = []

for i in range(number_pages + 1):
    response = requests.get(url + '/search/vacancy/', params=params, headers=headers)

    dom = BeautifulSoup(response.text, 'html.parser')

    vacancies = dom.find_all('div', {'class', 'vacancy-serp-item'})
    for vacancy in vacancies:
        vacancy_data = {}
        tag_a = vacancy.find('a')
        name_of_vacancy = tag_a.text
        link = tag_a.get('href')
        try:
            block_with_compensation = vacancy.find('div', {'class', 'vacancy-serp-item__sidebar'}).text
            list_of_compensations = block_with_compensation.split(' ')
            match list_of_compensations:
                case (min_comp, _, max_comp, currency):
                    min_comp, max_comp, currency = \
                        int(min_comp.replace(u"\u202f", '')), \
                        int(max_comp.replace(u"\u202f", '')), \
                        currency
                case (pref, comp, currency) if pref == 'от':
                    min_comp, max_comp, currency = int(comp.replace(u"\u202f", '')), None, currency
                case (pref, comp, currency) if pref == 'до':
                    min_comp, max_comp, currency = None, int(comp.replace(u"\u202f", '')), currency

        except:
            min_comp = None
            max_comp = None
            currency = None
        block_with_hr_information = vacancy.find('div', {'class', 'vacancy-serp-item__meta-info-company'})
        hr_link = url + block_with_hr_information.find('a', {'class', 'bloko-link'})['href']

        vacancy_data['name_of_vacancy'] = name_of_vacancy
        vacancy_data['vacancy_link'] = link
        vacancy_data['minimal_compensation'] = min_comp
        vacancy_data['maximal_compensation'] = max_comp
        vacancy_data['compensation_currency'] = currency
        vacancy_data['hr_link'] = hr_link

        try:
            products.insert_one(vacancy_data)
        except DuplicateKeyError as e:
            print(e)
            print(vacancy_data['name_of_vacancy'])
        # vacancy_list.append(vacancy_data)

    params['page'] += 1

search_vacancy(int(input('Введите минимальную сумму оплаты: ')))
