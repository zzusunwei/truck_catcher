#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import pymongo
from utils import get_next_id
from utils import get_html
current_version = 1
client = pymongo.MongoClient('mongodb://localhost:27017/')
truck_parts_cn357_db = client['truck_parts_cn357_db']
filter_model = truck_parts_cn357_db["filter_model"]
filter_model_detail = truck_parts_cn357_db["filter_model_detail"]
truck_model = truck_parts_cn357_db["truck_model"]
truck_model_detail = truck_parts_cn357_db["truck_model_detail"]
engine_model = truck_parts_cn357_db["engine_model"]
engine_model_detail = truck_parts_cn357_db["engine_model_detail"]


def get_format_product(url, product_model):
    html_str = get_html(url)
    products = []
    products_container = html_str.findAll(attrs={"class": "mProList"})
    products_div = products_container.findAll(attrs={"class": "l"})
    for product_div in products_div:
        product = {}
        product_name_a = product_div.find("a")
        product_index_href = product_name_a.attrs["href"]
        product_index_name = product_name_a.text
        product_descs_lis = product_div.findAll("li")
        for product_descs_li in product_descs_lis:
            key = product_descs_li.find("i").text
            value = product_descs_li.find("span").text
            product[key.strip()] = value.strip()
        product['product_index_href'] = product_index_href
        product['product_index_name'] = product_index_name
        product['_id'] = get_next_id(product_model)
        product['version'] = current_version
        products.append(product)
    return products


def get_format_product_detail(parent_collection, detail_collection, version):
    models_josn = truck_parts_cn357_db[parent_collection].find(
        {
            "version": version
        }, {
            "_id": 1,
            "product_index_href": 1,
            "version": 1
        }).distinct('product_index_href')

    for model in models_josn:
        url = "https://www.cn357.com/" + model + "_2-1"
        print(url)
        html = get_html(url)
        product = {}
        product_name = html.find(attrs={"class": "mTab wp"}).find("h2").text
        product["product"] = product_name

        uls = html.findAll(name="ul", attrs={"class": "table"})
        for ul in uls:
            key = ul.find("i").text
            value = ul.find("span").text
            product[key] = value
        truck_parts_cn357_db[detail_collection].insert(product)

        query = {"product_index_href": model}
        newvalues = {"$set": {"version": version + 1}}
        update_ret = truck_parts_cn357_db[parent_collection].update_many(
            query, newvalues)
        print(update_ret.modified_count)


def get_filter_parts(url, collection_name):
    print("filter_parts: " + url)
    html = get_html(url)
    filters_continer = html.findAll(name="div", attrs={"class": "cellPic"})
    for filter_continer in filters_continer:
        url = "https://www.cn357.com" + filter_continer.find("a").attrs["href"]
        print("filter_part: " + url)
        filter_html = get_html(url)
        filter_desc = filter_html.find(name="ul", attrs={"class": "parameter clear"})
        filter = {}
        for filter_desc_item in filter_desc:
            key = filter_desc_item.find("span").text
            value = filter_desc_item.text
            filter[key] = value
        collection_name.insert_one(filter)


if __name__ == "__main__":
    for i in range(1, 256):
        if i < 198:
            get_format_product("https://www.cn357.com/product_list1-" + str(i),
                               "truck_model")
        if i < 150:
            get_format_product(
                "https://www.cn357.com/product_list2-1" + str(i),
                "truck_model")
        if i < 256:
            get_format_product("https://www.cn357.com/product_list3-" + str(i),
                               "truck_model")
        if i < 175:
            get_format_product("https://www.cn357.com/product_list4-" + str(i),
                               "truck_model")
    # https://www.cn357.com/qipei_list134
    # https://www.cn357.com/qipei_list133