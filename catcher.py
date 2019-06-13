#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import pymongo
import re
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
air_filter_detail = catcher_db["air_filter_detail"]

truck_parts_db = client['truck_parts_db']
eurocvbay_parts = truck_parts_db['eurocvbay_parts']


def gethtml(url):
    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    driver = webdriver.Chrome(chrome_options=option)
    driver.get(url)
    html_str = driver.page_source
    return BeautifulSoup(html_str, 'html.parser')


def getNextValue(collect_name):
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


def init_truck_model():
    # base_url = [
    #     "http://www.360che.com/zhongkache/", "http://www.360che.com/zixieche/",
    #     "http://www.360che.com/qianyinche/", "http://www.360che.com/qingka/"
    # ]
    base_url = ["http://www.360che.com/qingka/"]
    for url in base_url:
        html = gethtml(url)
        truck_container = html.findAll(attrs={"class": "xll_center2_a1_y"})
        for brand_truck in truck_container:
            brand_name_container = brand_truck.find(
                attrs={"class": "xll_center2_a1_y1"})
            brand_name = brand_name_container.find('a').string

            model_list_container = brand_truck.find(
                attrs={'class': 'xll_center2_a1_y2'})
            for model_container in model_list_container:
                model = model_container.findChildren()
                model_name_a = model[0].find('a')
                model_name = model_name_a.string
                model_url = model_name_a.attrs["href"]
                model_json = {
                    "brand_name": brand_name,
                    "model_name": model_name,
                    "model_index_url": model_url,
                    "version": current_version
                }
                truck_model.insert(model_json)


def init_truck_model_detail():
    models_josn = truck_model.find({"version": current_version}, {
        "_id": 0,
        "id": 1,
        "brand_name": 1,
        "model_name": 1,
        "model_index_url": 1,
        "version": 1
    })

    for model in models_josn:
        db_ver = model.get("version", 1)
        if int(db_ver) > current_version:
            continue
        model_index_url = model["model_index_url"]
        model_param_url = model_index_url.replace("index", "param")
        html = gethtml(model_param_url)
        truck_model_container = html.find(attrs={"class": "parameter-detail"})
        cell_truck_model_num = sum(1 for _ in truck_model_container.find(
            "tr",
            attrs={
                "id": "fixed_top"
            },
        ).findAll("th"))
        cell_truck_models = {}
        for i in range(1, cell_truck_model_num):
            cell_truck_models[i] = {}
        rows = truck_model_container.findAll("tr")
        for row_data in rows:
            if row_data.get('id', "") == "fixed_top":
                for i in range(1, cell_truck_model_num):
                    cell_model_name = row_data.findAll("th")[i].find(
                        'a').string
                    cell_truck_models[i]["cell_model_name"] = cell_model_name
            if row_data.get('class', "") == ["param-row"]:
                row_id = row_data.findAll("td")[0].text
                for i in range(1, cell_truck_model_num):
                    value_content_td = row_data.findAll("td")
                    if value_content_td and len(value_content_td) > i:
                        value_content = value_content_td[i]
                        if value_content:
                            value = value_content.find('div').text
                            cell_truck_models[i][row_id] = value.strip()
        for cell_truck_model in cell_truck_models.values():
            cell_truck_model["_id"] = getNextValue('truck_model_detail')
            cell_truck_model["parent_id"] = model["model_index_url"]
            cell_truck_model["brand_name"] = model["brand_name"]
            cell_truck_model["model_name"] = model["model_name"]
            truck_model_detail.insert(cell_truck_model)
        truck_model.find_and_modify({"id": model.get("id", 1)},
                                    {"$inc": {
                                        "version": current_version + 1
                                    }})


def init_engine(url):
    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    driver = webdriver.Chrome(chrome_options=option)
    driver.get(url)
    html_str = BeautifulSoup(driver.page_source, 'html.parser')
    product_list_ul = html_str.findAll(attrs={"class": "products-list"})[0]
    products_li = product_list_ul.findAll("li")
    for product_li in products_li:
        engine = {}
        product_name_a = product_li.find("h5").find("a")
        product_index_href = product_name_a.attrs["href"]
        product_index_name = product_name_a.text
        product_span = product_li.findAll(
            attrs={"class": "content"})[0].find("span")
        product_items = product_span.findAll("p")
        for product_item in product_items:
            item_type = product_item.find("span")
            engine[item_type.next_element.strip(
            )] = item_type.next_sibling.strip()
        engine['product_index_href'] = product_index_href
        engine['product_index_name'] = product_index_name
        engine['_id'] = getNextValue('engine_model')
        engine['version'] = current_version
        engine_model.insert(engine)

    # links = html_str.findAll(attrs={"class": "pages-wd"})
    # link = links[0].attrs["href"]
    # init_engine('https://product.360che.com' + link)


def init_engine_detail():
    models_josn = engine_model.find({
        "version": 2
    }, {
        "_id": 1,
        "product_index_href": 1,
        "version": 1
    }).distinct('product_index_href')

    for model in models_josn:
        # db_ver = model.get("version", 1)
        # if int(db_ver) > current_version:
        #     continue
        model_index_url = model
        # ["product_index_href"]
        model_param_url = model_index_url.replace("index", "param")
        url = "https://product.360che.com" + model_param_url
        print(url)
        html = gethtml(url)
        truck_engin_container = html.find(attrs={"class": "parameter-detail"})
        cell_engin_model_num = sum(1 for _ in truck_engin_container.find(
            "tr",
            attrs={
                "id": "fixed_top"
            },
        ).findAll("th"))
        cell_engin_models = {}
        for i in range(1, cell_engin_model_num):
            cell_engin_models[i] = {}
        rows = truck_engin_container.findAll("tr")
        for row_data in rows:
            if row_data.get('id', "") == "fixed_top":
                for i in range(1, cell_engin_model_num):
                    cell_model_name = row_data.findAll("th")[i].find(
                        'a').string
                    cell_engin_models[i][
                        "cell_model_name"] = cell_model_name
            if row_data.get('class', "") == ["param-row"]:
                row_id = row_data.findAll("td")[0].text
                for i in range(1, cell_engin_model_num):
                    value_content_td = row_data.findAll("td")
                    if value_content_td and len(value_content_td) > i:
                        value_content = value_content_td[i]
                        if value_content:
                            value = value_content.find('div').text
                            cell_engin_models[i][row_id] = value.strip()
        for cell_engin_model in cell_engin_models.values():
            cell_engin_model["_id"] = getNextValue('engine_model_detail')
            cell_engin_model["parent_id"] = model
            cell_engin_model["version"] = current_version
            engine_model_detail.insert(cell_engin_model)

        query = {"product_index_href": model}
        newvalues = {"$set": {"version": current_version + 1}}
        update_ret = engine_model.update_many(query, newvalues)
        print(update_ret.modified_count)


def init_air_filter_detail():

    urls = [
        "https://product.360che.com/m67/16962_param.html",
        "https://product.360che.com/m66/16560_param.html",
        "https://product.360che.com/m76/19099_param.html"
    ]
    for url in urls:
        print(url)
        html = gethtml(url)
        truck_engin_container = html.find(attrs={"class": "parameter-detail"})
        cell_engin_model_num = sum(1 for _ in truck_engin_container.find(
            "tr",
            attrs={
                "id": "fixed_top"
            },
        ).findAll("th"))
        cell_engin_models = [{}] * cell_engin_model_num
        rows = truck_engin_container.findAll("tr")
        for row_data in rows:
            if row_data.get('id', "") == "fixed_top":
                for i in range(1, cell_engin_model_num):
                    cell_model_name = row_data.findAll("th")[i].find(
                        'a').string
                    cell_engin_models[i]["cell_model_name"] = cell_model_name
            if row_data.get('class', "") == ["param-row"]:
                row_id = row_data.findAll("td")[0].text
                for i in range(1, cell_engin_model_num):
                    value_content_td = row_data.findAll("td")
                    if value_content_td and len(value_content_td) > i:
                        value_content = value_content_td[i]
                        if value_content:
                            value = value_content.find('div').text
                            cell_engin_models[i][row_id] = value.strip()
        for cell_engin_model in cell_engin_models:
            cell_engin_model["_id"] = getNextValue('air_filter_detail')
            cell_engin_model["version"] = current_version
            air_filter_detail.insert(cell_engin_model)


def eurocvbay_parts_init(url):
    print("current url is" + url)
    html = gethtml(url)
    # f = requests.get(url)
    # html = BeautifulSoup(f.content, "html.parser")
    part = {}
    product_name = html.find(attrs={
        "class": "J_productTitle title g_minor"
    }).find("span").text
    detailedDesc_container = html.find(attrs={"id": "detailedDesc"})
    product_detail = detailedDesc_container.find("table")
    replaces = []
    if product_detail:
        trs = product_detail.findAll("tr")
        if len(trs) > 0:
            for index in range(len(trs)):
                if index == 0:
                    continue
                replace = {}
                tds = trs[index]
                if (len(tds) < 4):
                    continue
                replace["brand"] = tds.contents[0].text
                replace["replace_prod_no"] = tds.contents[1].text
                replace["properties"] = tds.contents[2].text
                replace["data"] = tds.contents[3].text
                replaces.insert(index, replace)
    part["product_name"] = product_name
    part["replaces"] = replaces
    part["_id"] = getNextValue("eurocvbay_parts")
    part["url"] = url
    eurocvbay_parts.insert(part)
    page_nav_container = html.findAll(attrs={"class": "pagenation2"})
    for page_nav in page_nav_container:
        tag = page_nav.find_all(text=re.compile('下一个*'))
        if tag:
            page_nav = page_nav.findAll("a")
            url = page_nav[1].attrs["href"]
            eurocvbay_parts_init("http://www.eurocvbay.com/" + url)


def truck_model_detail_debug(model_param_url):
    html = gethtml(model_param_url)
    truck_model_container = html.find(attrs={"class": "parameter-detail"})
    cell_truck_model_num = sum(1 for _ in truck_model_container.find(
        "tr",
        attrs={
            "id": "fixed_top"
        },
    ).findAll("th"))
    cell_truck_models = {}
    for i in range(cell_truck_model_num):
        cell_truck_models[i] = {}
    rows = truck_model_container.findAll("tr")
    for row_data in rows:
        if row_data.get('id', "") == "fixed_top":
            for i in range(1, cell_truck_model_num):
                cell_model_name = row_data.findAll("th")[i].find('a').string
                cell_truck_models[i]["cell_model_name"] = cell_model_name
        if row_data.get('class', "") == ["param-row"]:
            row_id = row_data.findAll("td")[0].text
            for i in range(1, cell_truck_model_num):
                value_content_td = row_data.findAll("td")
                if value_content_td and len(value_content_td) > i:
                    value_content = value_content_td[i]
                    if value_content:
                        value = value_content.find('div').text
                        cell_truck_models[i][row_id] = value.strip()
    for cell_truck_model in cell_truck_models.values():
        cell_truck_model["_id"] = getNextValue('truck_model_detail')
        # truck_model_detail.insert(cell_truck_model)


if __name__ == "__main__":
    # init_truck_model()
    # id_collect.insert_one(({'_id': "truck_model", 'sequence_value': 0}))
    # id_collect.insert_one(({
    #    '_id': "truck_cell_model_detail",
    #    'sequence_value': 0
    # }))
    # id_collect.insert_one(({'_id': "engine_model", 'sequence_value': 0}))
    # i = 265
    # while i < 399:
    #     i += 1
    #     print(i)
    #     base_url = "https://product.360che.com/price/c3_s61_b0_s0_c" + str(
    #         i) + ".html"
    #     init_engine(base_url)
    # id_collect.insert_one(({'_id': "truck_model_detail", 'sequence_value': 0}))
    # init_truck_model_detail()

    init_engine_detail()

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

    # mongoexport -d truck_catcher_db -c truck_model -o truck_model.dat
    # mongoexport -d truck_catcher_db -c truck_model_detail -o truck_model_detail.dat
    # mongoexport -d truck_catcher_db -c air_filter_detail -o air_filter_detail.dat
    # mongoimport -d truck_catcher_db -c truck_model_detail_new truck_model_detail.dat
    # mongoimport -d truck_catcher_db -c filter_detail air_filter_detail.dat
    # truck_model_detail_debug("https://product.360che.com/s0/219_63_param.html")