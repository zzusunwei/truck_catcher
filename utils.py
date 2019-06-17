#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import pymongo
from selenium import webdriver
from bs4 import BeautifulSoup

client = pymongo.MongoClient('mongodb://localhost:27017/')
catcher_db = client['truck_catcher_db']
id_collect = catcher_db['id_collect']


def get_html(url):
    print(url)
    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    driver = webdriver.Chrome(chrome_options=option)
    driver.implicitly_wait(60)
    driver.get(url)
    html_str = driver.page_source
    return BeautifulSoup(html_str, 'html.parser')


def get_next_id(collect_name):
    ret = id_collect.find_and_modify({"_id": collect_name},
                                     {"$inc": {
                                         "sequence_value": 1
                                     }},
                                     safe=True,
                                     new=True)
    if ret:
        return ret.get("sequence_value", "default")
    id_collect.insert_one(({'_id': collect_name, 'sequence_value': 0}))
    return 0
