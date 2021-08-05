from re import findall
from requests import get
from bs4 import BeautifulSoup
from numpy import ndarray

def get_laptop_url(url):
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