from get_propertiese import get_laptop_url as glu
from requests import get
from bs4 import BeautifulSoup

def get_raw_data(url):
    baseurl = 'https://www.digikala.com'
    #url = 'https://www.digikala.com/search/category-notebook-netbook-ultrabook/?has_selling_stock=1&pageno={}&sortby=4'
    pnum = 1
    data = []
    while True:
        page = get(url.format(pnum))
        if page.status_code != 200:
            break
        soup = BeautifulSoup(page.text, 'html.parser')
        urls = soup.find_all(
            'a', class_="c-product-box__img c-promotion-box__image js-url js-product-item js-product-url")
        for i in urls:
            link = baseurl + i['href']
            data.append(glu(link))
        pnum += 1