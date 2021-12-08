# Написать программу, которая собирает входящие письма из своего или тестового почтового ящика
# и сложить данные о письмах в базу данных (от кого, дата отправки, тема письма, текст письма полный)
# Логин тестового ящика: study.ai_172@mail.ru
# Пароль тестового ящика: NextPassword172#

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
import time
from pymongo import MongoClient
from pymongo.errors import *

client = MongoClient('localhost', 27017)

db = client['posts_0812']
posts = db.posts

driver = webdriver.Chrome("./chromedriver.exe")

driver.get("https://mail.ru/")

driver.find_element(By.CLASS_NAME, "email-input").send_keys("study.ai_172")
driver.find_element(By.XPATH, "//button[@data-testid='enter-password']").click()
driver.implicitly_wait(5)

driver.find_element(By.CLASS_NAME, "password-input").send_keys("NextPassword172#")
driver.implicitly_wait(5)

driver.find_element(By.CLASS_NAME, "second-button").click()
driver.implicitly_wait(20)

link_set = set()

last_letter = 0
while True:
    letters = driver.find_elements(By.CLASS_NAME, "js-letter-list-item")

    for letter in letters:
        link = letter.get_attribute('href')
        print(link)
        if 'inbox' in link:
            link_set.add(link)
    if letters[-1] == last_letter:
        break

    last_letter = letters[-1]
    action = ActionChains(driver)
    action.move_to_element(letters[-1])
    action.perform()
    time.sleep(3)


print(letters)
print(link_set)

for i in link_set:
    driver.get(i)
    letters_dict = {}

    elem = driver.find_element(By.CLASS_NAME, 'letter__author')
    letters_dict['author'] = elem.find_element(By.CLASS_NAME, 'letter-contact').text
    letters_dict['date'] = elem.find_element(By.CLASS_NAME, 'letter__date').text
    # letters_dict['date'] = give_me_correct_date(raw_date)

    letters_dict['link'] = i
    letters_dict['thread'] = driver.find_element(By.CLASS_NAME, 'thread__subject').text
    letters_dict['text'] = driver.find_element(By.CLASS_NAME, 'letter__body').text
    posts.insert_one(letters_dict)


