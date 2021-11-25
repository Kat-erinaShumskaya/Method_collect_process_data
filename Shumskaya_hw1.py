# 1. Посмотреть документацию к API GitHub, разобраться как вывести список
# репозиториев для конкретного пользователя, сохранить JSON-вывод в файле *.json.

import requests
import json

url = 'https://api.github.com'
user='Kat-erinaShumskaya'

rec = requests.get(f'{url}/users/{user}/repos')

for i in rec.json():
    print(i['name'])

with open('data.json', 'w') as f:
    json.dump(rec.json(), f)