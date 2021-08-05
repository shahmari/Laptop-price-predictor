from json import dump
from csv import writer, QUOTE_MINIMAL

def save_text(data):
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
def save_json(data):
    with open('output.json', 'w', encoding='utf-8') as jsonfile:
        dump(data, jsonfile)
def save_csv(data):
    with open('output.csv', 'w',  encoding='utf-8') as csvfile:
        spamwriter = writer(csvfile, delimiter=',',
                            quotechar='\n', quoting= QUOTE_MINIMAL)
        for i in data:
            spamwriter.writerow(i.keys())
            spamwriter.writerow(i.values())
def save_tsv(data):
    with open('output.tsv', 'w',  encoding='utf-8') as tsvfile:
        spamwriter = writer(tsvfile, delimiter='\t', quotechar='"')
        for i in data:
            spamwriter.writerow(i.keys())
            spamwriter.writerow(i.values())