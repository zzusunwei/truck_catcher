#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import pymongo
from utils import get_next_id
from utils import get_html
current_version = 1
client = pymongo.MongoClient('mongodb://localhost:27017/')
truck_parts_cn357_db = client['truck_parts_cn357_db']
filter_model = truck_parts_cn357_db["cn357_filter_model"]
filter_model_detail = truck_parts_cn357_db["cn357_filter_model_detail"]
truck_model = truck_parts_cn357_db["cn357_truck_model"]
truck_model_detail = truck_parts_cn357_db["cn357_truck_model_detail"]
engine_model = truck_parts_cn357_db["cn357_engine_model"]
engine_model_detail = truck_parts_cn357_db["cn357_engine_model_detail"]
error_collection = truck_parts_cn357_db["error_coll"]


def get_format_product(url, product_model):
    try:
        html_str = get_html(url)
        products = []
        products_container = html_str.find(attrs={"class": "mProList"})
        if products_container:
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
    except BaseException as e:
        print('错误：', e)
        except_handler(url, product_model)
        return []


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
        try:
            url = "https://www.cn357.com" + model + "_2-1"
            print(url)
            html = get_html(url)
            product = {}
            product_name = html.find(attrs={
                "class": "mTab wp"
            }).find("h2").text
            product["product"] = product_name

            uls = html.findAll(name="ul", attrs={"class": "table"})
            for ul in uls:
                lis = ul.findAll(name="li")
                for li in lis:
                    key = li.find("i").text
                    value = li.find("span").text
                    product[key] = value
            truck_parts_cn357_db[detail_collection].insert(product)

            query = {"product_index_href": model}
            newvalues = {"$set": {"version": version + 1}}
            update_ret = truck_parts_cn357_db[parent_collection].update_many(
                query, newvalues)
            print(update_ret.modified_count)
        except BaseException as e:
            print('错误：', e)
            except_handler(url, detail_collection)


def get_filter_parts(url, collection_name):
    print("filter_parts: " + url)
    try:
        html = get_html(url)
        if not html:
            return
        filters_continer = html.findAll(name="div", attrs={"class": "cellPic"})
        for filter_continer in filters_continer:
            detail_url = "https://www.cn357.com" + filter_continer.find(
                "a").attrs["href"]
            filter = get_filter_parts_details(detail_url, collection_name)
            truck_parts_cn357_db[collection_name].insert_one(filter)
    except BaseException as e:
        print('错误：', e)
        except_handler(url, collection_name)


def get_filter_parts_details(url, collection_name):
    filter_html = get_html(url)
    filter_desc = filter_html.find(attrs={"class": "shopBaoJia"})
    if not filter_desc:
        container = filter_html.find(attrs={"class": "shopDiv1 pt10 pb10 cf"})
        if not container:
            return
        filter_desc = container.find(attrs={"class": "fr"})
    filter = {}
    if not filter_desc:
        except_handler(url, collection_name)
        return
    filter_desc_items = filter_desc.find("ul").findAll("li")
    if not filter_desc_items:
        return
    for filter_desc_item in filter_desc_items:
        key_container = filter_desc_item.find("span")
        if not key_container:
            key_container = filter_desc_item.find("i")
        key = key_container.text
        value = filter_desc_item.text
        filter[key] = value
    return filter


def error_handler():
    models = error_collection.find({"version": {
        "$lt": 2
    }}, {
        "_id": 1,
        "url": 1,
        "collection": 1,
        "version": 1
    })

    for model in models:
        url = model.get("url")

        coll = model.get("collection")
        if coll == "truck_model":
            pass
        elif coll == "cn357_truck_model_detail":
            pass
        elif coll == "cn357_filter_model_detail":
            ret = get_filter_parts_details(url, coll)
            if not ret:
                continue
            truck_parts_cn357_db[coll].insert_one(ret)
            query = {"url": model.get("url")}
            newvalues = {"$set": {"version": 2}}
            update_ret = error_collection.update_many(query, newvalues)
            print(update_ret)


if __name__ == "__main__":
    # for i in range(36, 256):
    #     products_a = []
    #     if i < 198:
    #         products = get_format_product(
    #             "https://www.cn357.com/product_list1-" + str(i), "truck_model")
    #         if products:
    #             products_a.extend(products)
    #     if i < 150:
    #         products = get_format_product(
    #             "https://www.cn357.com/product_list2-" + str(i), "truck_model")
    #         if products:
    #             products_a.extend(products)
    #     if i < 256:
    #         if products:
    #             products_a.extend(products)
    #         products = get_format_product(
    #             "https://www.cn357.com/product_list3-" + str(i), "truck_model")
    #     if i < 175:
    #         if products:
    #             products_a.extend(products)
    #         products = get_format_product(
    #             "https://www.cn357.com/product_list4-" + str(i), "truck_model")
    #     if products:
    #         truck_model.insert_many(products)
    # get_format_product_detail("cn357_truck_model", "cn357_truck_model_detail",
    #                           current_version)

    # https://www.cn357.com/qipei_list134
    # https://www.cn357.com/qipei_list133
    # filters = [
    #     "https://www.cn357.com/qipei_list133",
    #     "https://www.cn357.com/qipei_list134"
    # ]
    # for i in range(11, 19):
    #     if i < 18:
    #         get_filter_parts(
    #             "https://www.cn357.com/qipei_list133_0_0_0_0_" + str(i),
    #             "cn357_filter_model_detail")
    #     if i < 11:
    #         get_filter_parts(
    #             "https://www.cn357.com/qipei_list134_0_0_0_0_" + str(i),
    #             "cn357_filter_model_detail")
    error_handler()
