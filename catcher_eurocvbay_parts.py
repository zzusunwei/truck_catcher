import pymongo
from selenium import webdriver
from bs4 import BeautifulSoup

current_version = 1

client = pymongo.MongoClient('mongodb://localhost:27017/')

catcher_db = client['truck_catcher_db']
id_collect = catcher_db['id_collect']
# truck_model = catcher_db["truck_model"]
truck_model = catcher_db["truck_model_new"]
truck_model_detail = catcher_db["truck_model_detail"]
engine_model = catcher_db["engine_model"]
engine_model_detail = catcher_db["engine_model_detail_new"]


def init_engine(url):
    driver = webdriver.Chrome()
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
        engine['_id'] = get_next_id('engine_model')
        engine['version'] = current_version
        engine_model.insert(engine)
    # links = html_str.findAll(attrs={"class": "pages-wd"})
    # link = links[0].attrs["href"]
    # init_engine('https://product.360che.com' + link)


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