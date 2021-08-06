from re import findall
from requests import get
from bs4 import BeautifulSoup

# getting laptop informations from url
def get_laptop_info(url):
	laptop = get(url)
	soup = BeautifulSoup(laptop.text, 'html.parser')
	res = soup.find('article', class_="c-params__border-bottom")
	if res == None:
		return None
	vals = res.find_all("div", class_="c-params__list-value")
	keys = res.find_all("div", class_="c-params__list-key")
	name = findall(r'\n\s*([\w\s].*?)\n', soup.find('h1',class_="c-product__title").text)[0]
	ret = {}
	ret['name'] = name
	ret['price'] = soup.find('meta', {"name": "twitter:data1"})['content']
	for i in range(len(keys)):
	    if '\n' in keys[i].text:
	        ret[findall(r'\n\s*([\w\s].*?)\n', keys[i].text)[0]] = findall(r'\n\s*([\w\s].*?)\n', vals[i].text)[0]
	    else:
	        ret[keys[i].text] = findall(r'\n\s*([\w\s].*?)\n', vals[i].text)[0]
	return ret

# finding laptop urls and getting their data
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
            data.append(get_laptop_info(link))
        pnum += 1
    return data

# saving data
def save_text(data):
    string = ''
    for i in data:
        for key in i.keys():
            string += key
            string += '\t'
        string += '\n'
        for val in i.values():
            string += val
            string += '\t'
        string += '\n'
    with open("output.txt", "w", encoding='utf-8') as txtfile:
        txtfile.write(string)