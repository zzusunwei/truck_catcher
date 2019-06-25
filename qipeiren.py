import pymongo
from utils import get_next_id
from utils import get_html
client = pymongo.MongoClient('mongodb://localhost:27017/')
truck_parts_qipeiren_db = client['truck_parts_qipeiren_db']

product_coll = truck_parts_qipeiren_db["product_coll"]


def get_filter_detail(url):
    html = get_html(url)
    product_lis = html.findAll(name="li",
                               attrs={
                                   "class": "list-item",
                                   "issbpitem": "true"
                               })
    for product_li in product_lis:
        product_url = product_li.find("a").attrs.get("href", "")
        product_page = get_html(product_url)
        product = {}
        desc = product_page.find("h1").text
        product["desc"] = desc
        detail_info = product_page.find(name="div",
                                        attrs={"class": "info-typedesc"})
        if not detail_info:
            continue
        lis = detail_info.find(name="div", attrs={
            "class": "basic-info"
        }).findAll("li")
        for li in lis:
            if not li.find("span"):
                continue
            key = li.find("span").text
            value = li.text
            product[key] = value
        adaptations = product_page.findAll(name="div",
                                           attrs={"class": "adaptation"})
        for adp in adaptations:
            adp_type = adp.find("div").text
            adp_prods_li = adp.findAll("li")
            adp_prods = []
            if not adp_prods_li:
                continue
            for li in adp_prods_li:
                if not li.text:
                    continue
                adp_prods.append(li.text.strip())
            product[adp_type] = adp_prods
        product_coll.insert(product)


if __name__ == "__main__":
    for i in range(1, 100):
        get_filter_detail("http://www.qipeiren.com/c/101095P" + str(i) + "/")
