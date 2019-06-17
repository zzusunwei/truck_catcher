#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import pymongo
import re
from utils import get_next_id
from utils import get_html
from selenium import webdriver
from bs4 import BeautifulSoup

current_version = 2

client = pymongo.MongoClient('mongodb://localhost:27017/')
truck_parts_db = client['truck_parts_db']
filter_model = truck_parts_db["filter_model"]
filter_model_detail = truck_parts_db["filter_model_detail"]
truck_model = truck_parts_db["truck_model"]
truck_model_detail = truck_parts_db["truck_model_detail"]
engine_model = truck_parts_db["engine_model"]
engine_model_detail = truck_parts_db["engine_model_detail"]


def get_format_product(url, product_model):
    html_str = get_html(url)
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
        product['_id'] = get_next_id(product_model)
        product['version'] = current_version
        products.append(product)
    return products


def get_format_product_detail(parent_collection, detail_collection, version):
    models_josn = truck_parts_db[parent_collection].find({
        "version": version
    }, {
        "_id": 1,
        "product_index_href": 1,
        "version": 1
    }).distinct('product_index_href')

    for model in models_josn:
        model_index_url = model
        # ["product_index_href"]
        model_param_url = model_index_url.replace("index", "param")
        url = "https://product.360che.com" + model_param_url
        print(url)
        html = get_html(url)
        product_detail_container = html.find(attrs={"class": "parameter-detail"})
        product_detail_num = sum(1 for _ in product_detail_container.find(
            "tr",
            attrs={
                "id": "fixed_top"
            },
        ).findAll("th"))
        product_details = {}
        for i in range(1, product_detail_num):
            product_details[i] = {}
        rows = product_detail_container.findAll("tr")
        for row_data in rows:
            if row_data.get('id', "") == "fixed_top":
                for i in range(1, product_detail_num):
                    cell_model_name = row_data.findAll("th")[i].find(
                        'a').string
                    product_details[i]["cell_model_name"] = cell_model_name
            if row_data.get('class', "") == ["param-row"]:
                row_id = row_data.findAll("td")[0].text
                for i in range(1, product_detail_num):
                    value_content_td = row_data.findAll("td")
                    if value_content_td and len(value_content_td) > i:
                        value_content = value_content_td[i]
                        if value_content:
                            value = value_content.find('div').text
                            product_details[i][row_id] = value.strip()
        for product_details in product_details.values():
            product_details["_id"] = get_next_id('filter_model_detail')
            product_details["parent_id"] = model
            product_details["version"] = version
            truck_parts_db[detail_collection].insert(product_details)

        query = {"product_index_href": model}
        newvalues = {"$set": {"version": version + 1}}
        update_ret = truck_parts_db[parent_collection].update_many(query, newvalues)
        print(update_ret.modified_count)


def init_parts():
    # urls = [
    #     "https://product.360che.com/price/c3_s113_b0_s0.html",
    #     "https://product.360che.com/price/c3_s113_b0_s0_c2.html",
    #     "https://product.360che.com/price/c3_s113_b0_s0_c3.html",
    #     "https://product.360che.com/price/c3_s113_b0_s0_c4.html",
    #     "https://product.360che.com/price/c3_s113_b0_s0_c5.html",
    #     "https://product.360che.com/price/c3_s113_b0_s0_c6.html",
    #     "https://product.360che.com/price/c3_s113_b0_s0_c7.html",
    #     "https://product.360che.com/price/c3_s114_b0_s0.html",
    #     "https://product.360che.com/price/c3_s114_b0_s0_c2.html",
    #     "https://product.360che.com/price/c3_s114_b0_s0_c3.html",
    #     "https://product.360che.com/price/c3_s115_b0_s0.html",
    #     "https://product.360che.com/price/c3_s115_b0_s0_c2.html",
    #     "https://product.360che.com/price/c3_s115_b0_s0_c3.html"
    # ]
    # for url in urls:
    #     products = get_format_product(url)
    #     filter_model.insert_many(products) 


if __name__ == "__main__":
    # init_truck_model()
    # i = 265
    # while i < 399:
    #     i += 1
    #     print(i)
    #     base_url = "https://product.360che.com/price/c3_s61_b0_s0_c" + str(
    #         i) + ".html"
    #     init_engine(base_url)
    # init_truck_model_detail()
    # init_engine_detail()
    # models_josn = engine_model.find({"version": 1}, {"_id": 1, "product_index_href": 1, "version":1}).distinct('product_index_href')
    # print(models_josn)

    # rets = engine_model.find({"product_index_href": "/m39/9781_param.html"})
    # for ret in rets:
    #     print(ret)

    # init_url = "http://www.eurocvbay.com/h-pd-256.html"
    # eurocvbay_parts_init(init_url)

    # for i in range(10):
    #     gethtml("https://www.baidu.com/")
    # init_air_filter_detail()

    # urls = [
    #     "https://product.360che.com/price/c3_s113_b0_s0.html",
    #     "https://product.360che.com/price/c3_s113_b0_s0_c2.html",
    #     "https://product.360che.com/price/c3_s113_b0_s0_c3.html",
    #     "https://product.360che.com/price/c3_s113_b0_s0_c4.html",
    #     "https://product.360che.com/price/c3_s113_b0_s0_c5.html",
    #     "https://product.360che.com/price/c3_s113_b0_s0_c6.html",
    #     "https://product.360che.com/price/c3_s113_b0_s0_c7.html",
    #     "https://product.360che.com/price/c3_s114_b0_s0.html",
    #     "https://product.360che.com/price/c3_s114_b0_s0_c2.html",
    #     "https://product.360che.com/price/c3_s114_b0_s0_c3.html",
    #     "https://product.360che.com/price/c3_s115_b0_s0.html",
    #     "https://product.360che.com/price/c3_s115_b0_s0_c2.html",
    #     "https://product.360che.com/price/c3_s115_b0_s0_c3.html"
    # ]
    # for url in urls:
    #     init_filter(url)

    # init_filter_detail()