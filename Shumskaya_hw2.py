# Необходимо собрать информацию по продуктам питания с сайта: Список протестированных
# продуктов на сайте Росконтроль.рф Приложение должно анализировать несколько страниц
# сайта (вводим через input или аргументы).
# Получившийся список должен содержать:
#
# Наименование продукта.
# Все параметры (Безопасность, Натуральность, Пищевая ценность, Качество) Не забываем преобразовать
# к цифрам
# Общую оценку
# Сайт, откуда получена информация.
# Общий результат можно вывести с помощью dataFrame через Pandas. Сохраните в json либо csv.

# https://roscontrol.com/category/produkti/molochnie_produkti/siri/?page=2
import pandas as pd
import requests
from bs4 import BeautifulSoup

url = 'https://roscontrol.com/category/produkti/molochnie_produkti/siri/'

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.85 YaBrowser/21.11.2.773 Yowser/2.5 Safari/537.36'}

response = requests.get(url, headers=headers)

products_data = pd.DataFrame(columns=['name', 'safety', 'naturalness', 'nutritional_value', 'quality', 'total_rating'])

for i in range(1, 9):
    response = requests.get(url, params={'page': i}, headers=headers)
    dom = BeautifulSoup(response.text, 'html.parser')

    products = dom.find_all('div', {'class', 'product__item-leftblock group'})

    for product in products:
        product_data = {}

        product_data['name'] = product.find('div', {'class', 'product__item-link'}).contents[0]
        try:
            product_data['total_rating'] = int(product.find('div', {'class': ['rate green rating-value',
                                                'rate violation-value','rate blacklist-value']}).contents[0].strip())
        except:
            product_data['total_rating'] = None

        rating = product.find_all('div', {'class': 'right'})
        if len(rating) > 0:
            product_data['safety'] = int(rating[0].contents[0])
            product_data['naturalness'] = int(rating[1].contents[0])
            product_data['nutritional_value'] = int(rating[2].contents[0])
            product_data['quality'] = int(rating[3].contents[0])
        else:
            product_data['safety'] = None
            product_data['naturalness'] = None
            product_data['nutritional_value'] = None
            product_data['quality'] = None

        products_data.loc[len(products_data)] = product_data

print(products_data)
products_data.to_csv('products_data.csv', index=False)