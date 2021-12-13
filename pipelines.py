# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


class JobparserPipeline:

    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongobase = client.vacancy_test13_1314


    def process_item(self, item, spider):
        if spider.name == 'hhru':
            # item['min'], item['max'], item['cur'], item['nalog'] = self.process_salary_hh(item['salary'])
            item['min'], item['max'], item['cur'] = self.process_salary_hh(item['salary'])
            del item['salary']
        if spider.name == 'sj':
            item['min'], item['max'], item['cur'] = self.process_salary_sj(item['salary'])
            del item['salary']
        collection = self.mongobase[spider.name]
        collection.insert_one(item)
        return item

    def process_salary_hh(self, salary):
        if len(salary) == 7:
            min_s = int(salary[1].replace('\xa0', ''))
            max_s = int(salary[3].replace('\xa0', ''))
            cur = salary[5]
            # nalog = salary[6]
        elif len(salary) == 5:
            if 'от' in salary[0]:
                min_s = int(salary[1].replace('\xa0', ''))
                max_s = None
            elif 'до' in salary[0]:
                min_s = None
                max_s = int(salary[1].replace('\xa0', ''))
            else:
                min_s = None
                max_s = None
                cur = None
                # nalog = None
            cur = salary[3]
            # nalog = salary[4]
        elif len(salary) == 1:
            min_s = None
            max_s = None
            cur = None
            # nalog = None
        else:
            min_s = None
            max_s = None
            cur = None
            # nalog = None
        return min_s, max_s, cur#, nalog


    def process_salary_sj(self, salary):
        if len(salary) == 8:
            min_s = int(salary[0].replace('\xa0', ''))
            max_s = int(salary[4].replace('\xa0', ''))
            cur = salary[6]
        elif len(salary) == 4:
            cur = salary[2][-4:]
            salary[2] = salary[2][:-4]
            if 'от' in salary[0]:
                min_s = int(salary[2].replace('\xa0', ''))
                max_s = None
            elif 'до' in salary[0]:
                min_s = None
                max_s = int(salary[2].replace('\xa0', ''))
            else:
                min_s = None
                max_s = None
                cur = None
        else:
            min_s = None
            max_s = None
            cur = None
        return min_s, max_s, cur
