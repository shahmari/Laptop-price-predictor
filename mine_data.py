import re

keys = [
    'وزن',
    'اندازه صفحه نمایش',
    'دقت صفحه نمایش',
    'سازنده پردازنده گرافیکی',
    'حافظه اختصاصی پردازنده گرافیکی',
    'نوع حافظه داخلی',
    'نوع حافظه RAM',
    'ظرفیت حافظه RAM',
    'سری پردازنده',
    'حافظه Cache',
    'سیستم عامل',
    'توضیحات باتری',
    'صفحه نمایش لمسی',
    'پورت Thunderbolt',
    'پورت USB 4.0',
    'پورت USB Type-C',
    'کیبورد با نور پس زمینه',
    'حسگر اثر انگشت',
    'درایو نوری'
]

def miner(raw_inp):
    outdict = {}
    outdict['Price'] = int(raw_inp['price'])
    for key in keys:
        if key == 'وزن':
            outdict['Mass'] = float(re.findall(r'(.+?) کیلوگرم', raw_inp[key])[0])

        if key == 'اندازه صفحه نمایش':
            outdict['Panal size'] = float(re.findall(r'(.+?) اینچ', raw_inp[key])[0])

        if key == 'دقت صفحه نمایش':
            find = re.findall(
                r'(\d.+\d)\s', raw_inp[key])[0].replace(' ', '').split('x')
            outdict['Panal resolution'] = int(find[0]) * int(find[1])

        if key == 'سازنده پردازنده گرافیکی':
            outdict['GPU brand'] = raw_inp[key].replace(" ","")

        if key == 'حافظه اختصاصی پردازنده گرافیکی':
            null = 'بدون حافظه\u200cی گرافیکی مجزا '
            find = raw_inp[key].replace('GB ', '000')
            find = find.replace('MB ', '')
            find = find.replace(null, '0')
            outdict['GPU capacity'] = int(find)

        if key == 'نوع حافظه داخلی':
            if key in raw_inp.keys():
                stg_type = ['SSD ', 'eMMC ', 'حافظه\u200cهای هیبریدی ', 'هارد دیسک ']
                find = raw_inp[key].replace(stg_type[2], '1')
                find = find.replace(stg_type[3], '2')
                find = find.replace(stg_type[0], '3')
                find = find.replace(stg_type[1], '4')
                outdict['Disk type'] = int(find)
            else:
                outdict['Disk type'] = 1

        if key == 'نوع حافظه RAM':
            if '3' in raw_inp[key]:
                find = 3
            else:
                find = 4
            outdict['RAM type'] = find
            
        if key == 'ظرفیت حافظه RAM':
            find = raw_inp[key].replace(' گیگابایت ', '')
            outdict['RAM capacity'] = int(find)
            
        if key == 'سری پردازنده':
            outdict['CPU serie'] = raw_inp[key][:-1]

        if key == 'حافظه Cache':
            if key in raw_inp.keys():
                find = raw_inp[key].replace(' مگابایت ', '')
                outdict['Cache capacity'] = int(find)
            elif raw_inp['price'] < 10000000:
                outdict['Cache capacity'] = 1
            else:
                outdict['Cache capacity'] = 5

        if key == 'توضیحات باتری':
            if key in raw_inp.keys():
                find = re.sub(r'[^\d\.\s]', "", raw_inp[key])
                find = re.findall(r'\s(\d[\d\.]+)\s', find)
                if find != []:
                    if float(find[0]) > 100:
                        find[0] = 30.0
                    outdict['Battery'] = float(find[0])
                else:
                    outdict['Battery'] = 35.0
            else:
                outdict['Battery'] = 35.5
                
        if key == 'سیستم عامل':
            if key in raw_inp.keys():
                freeos = ['ندارد ', 'بدون ویندوز ', 'بدون سیستم\u200cعامل ',
                          'Ubuntu Linux ', 'FreeDOS ', 'Boot-Up DOS ']
                if raw_inp[key] in freeos:
                    find = 0
                else:
                    find = 1
                outdict['OS'] = find
            else:
                outdict['OS'] = 0

        if key == 'صفحه نمایش لمسی':
            if key in raw_inp.keys():
                resp = ['بله ', 'خیر ']
                find = raw_inp[key].replace(resp[0], '1').replace(resp[1], '0')
                outdict['Touch'] = int(find)
            else:
                outdict['Touch'] = 0

        if key == 'پورت Thunderbolt':
            if key in raw_inp.keys():
                resp = ['ندارد ', 'دارد ']
                find = raw_inp[key].replace(resp[0], '0').replace(resp[1], '1')
                outdict['Thunderbolt'] = int(find)
            else:
                outdict['Thunderbolt'] = 0

        if key == 'پورت USB 4.0':
            if key in raw_inp.keys():
                resp = ['ندارد ', 'دارد ']
                find = raw_inp[key].replace(resp[0], '0').replace(resp[1], '1')
                outdict['USB4'] = int(find)
            else:
                outdict['USB4'] = 0
        
        if key == 'پورت USB Type-C':
            if key in raw_inp.keys():
                resp = ['ندارد ', 'دارد ']
                find = raw_inp[key].replace(resp[0], '0').replace(resp[1], '1')
                outdict['Type-c'] = int(find)
            else:
                outdict['Type-c'] = 0

        if key == 'کیبورد با نور پس زمینه':
            if key in raw_inp.keys():
                resp = ['ندارد ', 'دارد ']
                find = raw_inp[key].replace(resp[0], '0').replace(resp[1], '1')
                outdict['Keyboard light'] = int(find)
            else:
                outdict['Keyboard light'] = 0

        if key == 'حسگر اثر انگشت':
            if key in raw_inp.keys():
                resp = ['ندارد ', 'دارد ']
                find = raw_inp[key].replace(resp[0], '0').replace(resp[1], '1')
                outdict['Fingerprint'] = int(find)
            else:
                outdict['Fingerprint'] = 0

        if key == 'درایو نوری':
            if key in raw_inp.keys():
                resp = ['DVD-RW ', 'بدون درایو نوری ']
                find = raw_inp[key].replace(resp[0], '1').replace(resp[1], '0')
                outdict['DVD'] = int(find)
            else:
                outdict['DVD'] = 0
    return outdict
