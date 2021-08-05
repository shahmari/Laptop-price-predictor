from get_propertiese import get_laptop_url as glu
from requests import get
from bs4 import BeautifulSoup
from json import dump
from csv import writer, QUOTE_MINIMAL

baseurl = 'https://www.digikala.com'
url = 'https://www.digikala.com/search/category-notebook-netbook-ultrabook/?has_selling_stock=1&pageno={}&sortby=4'
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
string = ''
for i in data:
    for key in i.keys():
        string += key
        string += ' , '
    string += '\n'
    for val in i.values():
        string += val
        string += ' , '
    string += '\n'

with open("output.txt", "w", encoding='utf-8') as txtfile:
    txtfile.write(string)

with open('output.json', 'w', encoding='utf-8') as jsonfile:
    dump(data, jsonfile)

with open('output.csv', 'w',  encoding='utf-8') as csvfile:
    spamwriter = writer(csvfile, delimiter=',',
                        quotechar='\n', quoting= QUOTE_MINIMAL)
    for i in data:
        spamwriter.writerow(i.keys())
        spamwriter.writerow(i.values())

with open('output.tsv', 'w',  encoding='utf-8') as tsvfile:
    spamwriter = writer(tsvfile, delimiter='\t', quotechar='"')
    for i in data:
        spamwriter.writerow(i.keys())
        spamwriter.writerow(i.values())
