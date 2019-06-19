#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import pymongo
import requests
import json

client = pymongo.MongoClient('mongodb://localhost:27017/')
truck_parts_chinacvsp = client['truck_parts_chinacvsp']
chinacvsp_filter_model = truck_parts_chinacvsp["chinacvsp_filter_model"]
chinacvsp_filter_detail_model = truck_parts_chinacvsp[
    "chinacvsp_filter_detail_model"]
error_collection = truck_parts_chinacvsp["error_coll"]


def get_filter_parts():
    try:
        for i in range(1, 25):
            headers = {
                "Accept": "application/json, text/javascript, */*; q=0.01",
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
                "Connection": "keep-alive",
                "Content-Length": "93",
                "Content-Type":
                "application/x-www-form-urlencoded; charset=UTF-8",
                "Cookie":
                'JSESSIONID=E3B996D39E59200396EE2AA2AC0624A3; UM_distinctid=16b6aa6734324a-04c4536198622a-42524a51-1fa400-16b6aa673462d2; CNZZDATA1273685881=901372399-1560862421-%7C1560862421; autologToken=""',
                "Host": "www.chinacvsp.com",
                "Origin": "http://www.chinacvsp.com",
                "Referer":
                "http://www.chinacvsp.com/ec/goods/goods_list.html?catType=pj&catId=10",
                "User-Agent":
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36 OPR/60.0.3255.151",
                "X-Requested-With": "XMLHttpRequest"
            }
            payload = {
                "isBacklog": "",
                "kw": "",
                "sort": "",
                "cat": 10,
                "shopCat": "",
                "catType": "pj",
                "brand": "",
                "page": i,
                "pageSize": 20,
                "shopId": "",
                "propertyId": ""
            }
            url = "http://www.chinacvsp.com/ec/goods/doSearchGoodsByProps.do"
            d = requests.post(url, data=payload, headers=headers)
            if d and d.text and d.text:
                ret = json.loads(d.text)
                row_data = ret.get("data", "").get("rows", "")
                print(row_data)
                chinacvsp_filter_model.insert_many(row_data)
            else:
                except_handler(i, "chinacvsp_filter_model")
                print(i)
                print()
    except BaseException as e:
        print('错误：', e)
        except_handler(url, "chinacvsp_filter_model")


def get_filter_parts_details():
    try:
        models = chinacvsp_filter_model.find({}, {
            "id": 1,
            "partNo": 1,
            "dealerPartNo": 1,
        })

        for model in models:
            id = model.get("id", "")
            headers = {
                "Accept":
                "application/json, text/javascript, */*; q=0.01",
                "Accept-Encoding":
                "gzip, deflate",
                "Accept-Language":
                "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
                "Connection":
                "keep-alive",
                "Content-Length":
                "93",
                "Content-Type":
                "application/x-www-form-urlencoded; charset=UTF-8",
                "Cookie":
                'JSESSIONID=E3B996D39E59200396EE2AA2AC0624A3; UM_distinctid=16b6aa6734324a-04c4536198622a-42524a51-1fa400-16b6aa673462d2; CNZZDATA1273685881=901372399-1560862421-%7C1560862421; autologToken=""',
                "Host":
                "www.chinacvsp.com",
                "Origin":
                "http://www.chinacvsp.com",
                "Referer":
                "http://www.chinacvsp.com/ec/goods/goods_view.html?id=" + id,
                "User-Agent":
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36 OPR/60.0.3255.151",
                "X-Requested-With":
                "XMLHttpRequest"
            }
            payload = {
                "isBacklog": "",
                "kw": "",
                "sort": "",
                "cat": 10,
                "shopCat": "",
                "catType": "pj",
                "brand": "",
                "page": id,
                "pageSize": 20,
                "shopId": "",
                "propertyId": ""
            }
            url = "http://www.chinacvsp.com/ec/goods/goods_view.html?id=" + id
            d = requests.post(url, data=payload, headers=headers)
            if d and d.text:
                ret = json.loads(d.text)
                chinacvsp_filter_detail_model.insert_one(
                    ret.get("data", "").get("goods", ""))

    except BaseException as e:
        print('错误：', e)
        except_handler(url, "chinacvsp_filter_model")


def except_handler(url, target_coll):
    error_collection.insert_one({
        "url": url,
        "collection": target_coll,
        "version": 0
    })


if __name__ == "__main__":
    get_filter_parts_details()
