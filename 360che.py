#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import pymongo
import re
from utils import getNextValue
from selenium import webdriver
from bs4 import BeautifulSoup

current_version = 2

client = pymongo.MongoClient('mongodb://localhost:27017/')

catcher_db = client['truck_catcher_db']
id_collect = catcher_db['id_collect']
truck_model = catcher_db["truck_model"]
# truck_model = catcher_db["truck_model_new"]
truck_model_detail = catcher_db["truck_model_detail"]
engine_model = catcher_db["engine_model"]
engine_model_detail = catcher_db["engine_model_detail_new"]

truck_parts_db = client['truck_parts_db']
eurocvbay_parts = truck_parts_db['eurocvbay_parts']
air_filter_detail = truck_parts_db["air_filter_detail"]

filter_model = truck_parts_db["filter_model"]
filter_model_detail = truck_parts_db["filter_model_detail"]


def get_format_product(url):
    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    driver = webdriver.Chrome(chrome_options=option)
    driver.get(url)
    html_str = BeautifulSoup(driver.page_source, 'html.parser')
    products = []
    product_list_ul = html_str.findAll(attrs={"class": "products-list"})[0]
    products_li = product_list_ul.findAll("li")
    for product_li in products_li:
        product = {}
        product_name_a = product_li.find("h5").find("a")
        product_index_href = product_name_a.attrs["href"]
        product_index_name = product_name_a.text
        product_span = product_li.findAll(
            attrs={"class": "content"})[0].find("span")
        product_items = product_span.findAll("p")
        for product_item in product_items:
            item_type = product_item.find("span")
            product[item_type.next_element.strip(
            )] = item_type.next_sibling.strip()
        product['product_index_href'] = product_index_href
        product['product_index_name'] = product_index_name
        product['_id'] = getNextValue('product_model')
        product['version'] = current_version
        products.append(product)
    return products