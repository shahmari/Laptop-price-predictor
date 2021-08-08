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
    'توضیحات باتری',
    'سیستم عامل',
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

        elif key == 'اندازه صفحه نمایش':
            outdict['PanalSize'] = float(re.findall(r'(.+?) اینچ', raw_inp[key])[0])

        elif key == 'دقت صفحه نمایش':
            find = re.findall(
                r'(\d.+\d)\s', raw_inp[key])[0].replace(' ', '').split('x')
            outdict['PanalResolution'] = int(find[0]) * int(find[1])

        elif key == 'سازنده پردازنده گرافیکی':
            find = raw_inp[key].replace(" ", "")
            GPUBrand = ['AMD', 'ATI', 'Apple', 'Intel', 'NVIDIA']
            find = GPUBrand.index(find)
            outdict['GPUBrand'] = find

        elif key == 'حافظه اختصاصی پردازنده گرافیکی':
            null = 'بدون حافظه\u200cی گرافیکی مجزا '
            find = raw_inp[key].replace('GB ', '000')
            find = find.replace('MB ', '')
            find = find.replace(null, '0')
            outdict['GPUCapacity'] = int(find)

        elif key == 'نوع حافظه داخلی':
            if key in raw_inp.keys():
                stg_type = ['SSD ', 'eMMC ', 'حافظه\u200cهای هیبریدی ', 'هارد دیسک ']
                find = stg_type.index(raw_inp[key])
                outdict['DiskType'] = int(find)
            else:
                outdict['DiskType'] = 1

        elif key == 'نوع حافظه RAM':
            if '3' in raw_inp[key]:
                find = 3
            else:
                find = 4
            outdict['RAMType'] = find
            
        elif key == 'ظرفیت حافظه RAM':
            find = raw_inp[key].replace(' گیگابایت ', '')
            outdict['RAMCapacity'] = int(find)
            
        elif key == 'سری پردازنده':
            CPUModel = ['Core i7',
                        'Pentium',
                        'M1',
                        'Ryzen 3',
                        'Bristol Ridge',
                        'A6',
                        'Core i5',
                        'Core i9',
                        'Celeron',
                        'Ryzen 5',
                        'Core i3',
                        'ATHLON',
                        'Ryzen 7',
                        'Quad Core']
            find = raw_inp[key][:-1]
            find = CPUModel.index(find)
            outdict['CPUSerie'] = find

        elif key == 'حافظه Cache':
            if key in raw_inp.keys():
                find = raw_inp[key].replace(' مگابایت ', '')
                outdict['CacheCapacity'] = int(find)
            elif int(raw_inp['price']) < 10000000:
                outdict['CacheCapacity'] = 1
            else:
                outdict['CacheCapacity'] = 5

        elif key == 'توضیحات باتری':
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
                
        elif key == 'سیستم عامل':
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

        elif key == 'صفحه نمایش لمسی':
            if key in raw_inp.keys():
                resp = ['بله ', 'خیر ']
                find = raw_inp[key].replace(resp[0], '1').replace(resp[1], '0')
                outdict['Touch'] = int(find)
            else:
                outdict['Touch'] = 0

        elif key == 'پورت Thunderbolt':
            if key in raw_inp.keys():
                resp = ['ندارد ', 'دارد ']
                find = raw_inp[key].replace(resp[0], '0').replace(resp[1], '1')
                outdict['Thunderbolt'] = int(find)
            else:
                outdict['Thunderbolt'] = 0

        elif key == 'پورت USB 4.0':
            if key in raw_inp.keys():
                resp = ['ندارد ', 'دارد ']
                find = raw_inp[key].replace(resp[0], '0').replace(resp[1], '1')
                outdict['USB4'] = int(find)
            else:
                outdict['USB4'] = 0
        
        elif key == 'پورت USB Type-C':
            if key in raw_inp.keys():
                resp = ['ندارد ', 'دارد ']
                find = raw_inp[key].replace(resp[0], '0').replace(resp[1], '1')
                outdict['TypeC'] = int(find)
            else:
                outdict['TypeC'] = 0

        elif key == 'کیبورد با نور پس زمینه':
            if key in raw_inp.keys():
                resp = ['ندارد ', 'دارد ']
                find = raw_inp[key].replace(resp[0], '0').replace(resp[1], '1')
                outdict['KeyboardLight'] = int(find)
            else:
                outdict['KeyboardLight'] = 0

        elif key == 'حسگر اثر انگشت':
            if key in raw_inp.keys():
                resp = ['ندارد ', 'دارد ']
                find = raw_inp[key].replace(resp[0], '0').replace(resp[1], '1')
                outdict['Fingerprint'] = int(find)
            else:
                outdict['Fingerprint'] = 0

        elif key == 'درایو نوری':
            if key in raw_inp.keys():
                resp = ['DVD-RW ', 'بدون درایو نوری ']
                find = raw_inp[key].replace(resp[0], '1').replace(resp[1], '0')
                outdict['DVD'] = int(find)
            else:
                outdict['DVD'] = 0
    return outdict
