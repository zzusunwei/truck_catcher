#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import pymongo
from utils import get_next_id
current_version = 1
client = pymongo.MongoClient('mongodb://localhost:27017/')
truck_parts_cn357_db = client['truck_parts_cn357_db']
truck_parts_che360_db = client['truck_parts_db']
truck_parts_qipeiren_db = client['truck_parts_qipeiren_db']

target_truck_parts_db = client['target_truck_parts_db']

che360_filter_model_detail = truck_parts_che360_db["filter_model_detail"]
che360_engine_model_detail = truck_parts_che360_db["engine_model_detail"]
che360_truck_model_detail = truck_parts_che360_db["truck_model_detail"]

che360_air_filter_detail = truck_parts_che360_db["air_filter_detail"]
che360_filter_detail = truck_parts_che360_db["filter_detail"]
che360_eurocvbay_parts_clean = truck_parts_che360_db["eurocvbay_parts_clean"]

cn357_filter_model_detail = truck_parts_cn357_db["cn357_filter_model_detail"]
cn357_truck_model_detail = truck_parts_cn357_db["cn357_truck_model_detail"]

filter_model_detail = target_truck_parts_db["filter_model_detail"]
engine_model_detail = target_truck_parts_db["engine_model_detail"]
truck_model_detail = target_truck_parts_db["truck_model_detail"]

qipeiren_product_coll = truck_parts_qipeiren_db['qipeiren_product_coll']


def cn357_filter_clean():
    has_next = True
    for i in range(0, 100000):
        page_size = 10
        coll = cn357_filter_model_detail.find({}).sort(
            '_id', pymongo.ASCENDING).skip(i * page_size).limit(page_size)
        if not has_next:
            return
        has_next = False
        for data in coll:
            has_next = True
            filter = {}
            filter["brand"] = data.get("品牌：", "").split("：")[1]
            models_str = data.get("型号：", "").split("：")[1]
            models = models_str.split("/")
            for model in models:
                filter["model"] = model
                filter["_id"] = get_next_id("filter_model_detail")
                print(filter)
                filter_model_detail.insert_one(filter)


def cn357_truck_clean():
    has_next = True
    for i in range(0, 10000):
        page_size = 10
        coll = cn357_truck_model_detail.find({}).sort(
            '_id', pymongo.ASCENDING).skip(i * page_size).limit(page_size)
        if not has_next:
            return
        has_next = False
        for data in coll:
            has_next = True
            truck = {}
            truck["desc"] = data.get("product", "")
            truck["announcement_model"] = data.get("整车公告：", "")
            truck["brand"] = data.get("品牌：", "")
            truck["series"] = data.get("车系：", "")
            truck["purpose"] = data.get("用途：", "")
            truck["drive_model"] = data.get("驱动方式：", "")
            truck["tonnage_level"] = data.get("吨位级别：", "")
            truck["manufacturer"] = data.get("生产厂家：", "")
            truck["origin"] = data.get("整车产地：", "")
            truck["weight"] = data.get("整车重量：", "")
            truck["length"] = data.get("整车长度：", "")
            truck["width"] = data.get("整车宽度：", "")
            truck["height"] = data.get("整车高度：", "")
            truck["member"] = data.get("准乘人数：", "")
            truck["engine_model"] = data.get("发动机型号：", "")
            truck["engine_type"] = data.get("发动机形式：", "")
            truck["max_power"] = data.get("最大功率：", "")
            truck["max_hp"] = data.get("最大马力：", "")
            truck["cc"] = data.get("排量：", "")
            truck["fuel_type"] = data.get("燃油种类：", "")
            truck["transmission_model"] = data.get("变速箱型号：", "")
            truck["forward_gears_num"] = data.get("前进档位数：", "")
            truck["reverse_gears_num"] = data.get("倒档档位数：", "")
            truck["chassis_models"] = data.get("底盘型号：", "")
            truck["plate_spring_num"] = data.get("板簧片数：", "")
            truck["tyre_num"] = data.get("轮胎数量：", "")
            truck["tyre_type"] = data.get("轮胎规格：", "")
            truck["_id"] = get_next_id("truck_model_detail")
            print(truck)
            print()
            truck_model_detail.insert_one(truck)


def che360_truck_clean():
    has_next = True
    for i in range(0, 100000):
        page_size = 10
        coll = che360_truck_model_detail.find({}).sort(
            '_id', pymongo.ASCENDING).skip(i * page_size).limit(page_size)
        if not has_next:
            return
        has_next = False
        for data in coll:
            has_next = True
            truck = {}
            truck["desc"] = data.get("cell_model_name", "")
            truck["announcement_model"] = data.get("公告型号：", "")
            truck["drive_model"] = data.get("驱动形式：", "")
            truck["desc"] = data.get("轴距：", "")
            truck["engine_model"] = data.get("发动机：", "")
            truck["transmission_model"] = data.get("变速箱：", "")
            truck["length"] = data.get("车身长度：", "")
            truck["width"] = data.get("车身宽度：", "")
            truck["height"] = data.get("车身高度：", "")
            truck["weight"] = data.get("整车重量：", "")
            truck["capacity_kg"] = data.get("额定载重：", "")
            truck["tonnage_level"] = data.get("吨位级别：", "")
            truck["engine_brand"] = data.get("发动机品牌：", "")
            truck["cylinders_num"] = data.get("汽缸数：", "")
            truck["fuel_type"] = data.get("燃料种类：", "")
            truck["cc"] = data.get("排量：", "")
            truck["max_hp"] = data.get("最大马力：", "")
            truck["max_power"] = data.get("最大输出功率：", "")
            truck["engine_type"] = data.get("发动机形式：", "")
            truck["transmission_brand"] = data.get("变速箱品牌：", "")
            truck["forward_gears_num"] = data.get("前进挡位：", "")
            truck["reverse_gears_num"] = data.get("倒挡数：", "")
            truck["tyre_type"] = data.get("轮胎规格：", "")
            truck["tyre_num"] = data.get("轮胎数：", "")
            truck["tyre_num"] = data.get("弹簧片数：", "")
            truck["brand"] = data.get("brand_name", "")
            truck["model"] = data.get("model_name", "")
            truck["_id"] = get_next_id("truck_model_detail")
            print(truck)
            print()
            truck_model_detail.insert_one(truck)


def che360_engine_clean():
    has_next = True
    for i in range(0, 100000):
        page_size = 10
        coll = che360_engine_model_detail.find({}).sort(
            '_id', pymongo.ASCENDING).skip(i * page_size).limit(page_size)
        if not has_next:
            return
        has_next = False
        for data in coll:
            has_next = True
            engine = {}
            engine["desc"] = data.get("cell_model_name", "")
            engine["engine_model"] = data.get("发动机：", "")
            engine["series"] = data.get("系列：", "")
            engine["engine_supp"] = data.get("发动机厂商：", "")
            engine["cylinders_num"] = data.get("汽缸数：", "")
            engine["fuel_type"] = data.get("燃料种类：", "")
            engine["cc"] = data.get("排量：", "")
            engine["max_power"] = data.get("最大输出功率：", "")
            engine["max_hp"] = data.get("最大马力：", "")
            engine["engine_type"] = data.get("发动机形式：", "")
            engine["nick_name"] = data.get("nick_name", "")
            engine["_id"] = get_next_id("engine_model_detail")
            print(engine)
            print()
            engine_model_detail.insert_one(engine)


def che360_filter_clean():
    has_next = True
    for i in range(0, 100000):
        page_size = 10
        coll = che360_air_filter_detail.find({}).sort(
            '_id', pymongo.ASCENDING).skip(i * page_size).limit(page_size)
        if not has_next:
            return
        has_next = False
        for data in coll:
            has_next = True
            filter = {}
            filter["_id"] = get_next_id("filter_model_detail")
            filter["desc"] = data.get("cell_model_name", "")
            filter["type"] = data.get("类型：", "")
            filter["model"] = data.get("滤清器型号：", "")
            filter["diameter"] = data.get("直径：", "")
            filter["height"] = data.get("高度：", "")
            filter["weight"] = data.get("重量：", "")
            filter["leakproof_type"] = data.get("密封结构：", "")
            filter["locating_hole_diameter"] = data.get("定位孔直径：", "")
            filter["size_model"] = data.get("尺寸型号：", "")
            filter["market_model"] = data.get("市场型号：", "")
            filter["flux"] = data.get("流量：", "")
            filter["filter_level"] = data.get("过滤级别：", "")
            filter["thread_size"] = data.get("螺纹尺寸：", "")
            filter["adaptable_truck_models"] = data.get("适用车型：", "").split("/")
            filter["adaptable_enign_models"] = data.get("适用机型：", "").split("/")
            filter["adaptable_truck_types"] = data.get("适用车类型：", "").split("/")
            filter["adaptable_engine_types"] = data.get("适用发动机类型：",
                                                        "").split("/")
            filter["alternative_parts_model"] = data.get("可替换滤清器型号：", "")
            filter["nick_name"] = data.get("可替换滤清器零件号：", "")
            print(filter)
            print()
            filter_model_detail.insert_one(filter)


def eurocvbay_parts_clean():
    has_next = True
    for i in range(0, 100000):
        page_size = 10
        coll = che360_eurocvbay_parts_clean.find({}).sort(
            '_id', pymongo.ASCENDING).skip(i * page_size).limit(page_size)
        if not has_next:
            return
        has_next = False
        for data in coll:
            has_next = True
            filter = {}
            filter["_id"] = get_next_id("filter_model_detail")
            filter["desc"] = data.get("product_name", "")
            filter["replaces"] = data.get("replaces", "")
            print(filter)
            print()
            # filter_model_detail.insert_one(filter)


def qipeiren_product_coll_clean():
    has_next = True
    for i in range(0, 100000):
        page_size = 10
        coll = qipeiren_product_coll.find({}).sort(
            '_id', pymongo.ASCENDING).skip(i * page_size).limit(page_size)
        if not has_next:
            return
        has_next = False
        for data in coll:
            has_next = True
            product = {}
            product["id"] = data.get("_id", "")
            product["id"] = data.get("适用范围", "")
            product["id"] = data.get("用途", "")
            product["id"] = data.get("产品认证", "")
            product["id"] = data.get("排量", "")
            product["id"] = data.get("外径", "")
            product["id"] = data.get("型号", "")
            product["id"] = data.get("适配车型", "")
            product["id"] = data.get("容积", "")
            product["id"] = data.get("类别", "")
            product["id"] = data.get("品牌", "")
            product["id"] = data.get("缸径", "")
            product["id"] = data.get("缸数", "")
            product["id"] = data.get("长度", "")
            product["id"] = data.get("排放标准", "")
            product["id"] = data.get("极数", "")
            product["id"] = data.get("最大载荷", "")
            product["id"] = data.get("内径", "")
            product["id"] = data.get("发动机排量", "")
            product["id"] = data.get("外观尺寸", "")
            product["id"] = data.get("汽缸数", "")
            product["id"] = data.get("适配机型", "")
            product["id"] = data.get("材质", "")
            product["id"] = data.get("轮距", "")
            product["height"] = data.get("高度", "")
            product["origin"] = data.get("产地", "")
            product["pressure"] = data.get("压力", "")
            product["color"] = data.get("颜色", "")
            product["type"] = data.get("类型", "")
            product["desc"] = data.get("desc", "")
            product["engine_hp"] = data.get("发动机马力", "")


def get_all_key():
    has_next = True
    keys = set()
    for i in range(0, 100000):
        page_size = 10
        coll = qipeiren_product_coll.find({}).sort('_id', pymongo.ASCENDING).skip(
            i * page_size).limit(page_size)
        if not has_next:
            return keys
        has_next = False
        for data in coll:
            has_next = True
            for key in data.keys():
                keys.add(key)


if __name__ == "__main__":
    # cn357_filter_clean()
    # cn357_truck_clean()
    # che360_truck_clean()
    # che360_engine_clean()
    # che360_filter_clean()
    print(get_all_key())