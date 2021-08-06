import re

def miner(raw_inp):
    keys = []
    for key in keys:
        outdict = {}
        if key == 'وزن':
            outdict['mass'] = float(re.findall(r'(.+?) کیلوگرم', raw_inp[key])[0])
        if key == 'اندازه صفحه نمایش':
            outdict['panal size'] = float(re.findall(r'(.+?) اینچ', raw_inp[key])[0])
        if key == 'دقت صفحه نمایش':
            find = re.findall(
                r'(\d.+\d)\s', raw_inp[key])[0].replace(' ', '').split('x')
            outdict['panal resolution'] = int(find[0]) * int(find[1])
        if key == 'سازنده پردازنده گرافیکی':
            outdict['GPU company'] = raw_inp[key].replace(" ","")
        if key == 'حافظه اختصاصی پردازنده گرافیکی':
            null = 'بدون حافظه\u200cی گرافیکی مجزا '
            find = raw_inp[key].replace('GB ', '000')
            find = find.replace('MB ', '')
            find = find.replace(null, '0')
            outdict['GPU memory'] = int(find)
        if key == 'نوع حافظه داخلی':
            stg_type = ['SSD ', 'eMMC ', 'حافظه\u200cهای هیبریدی ', 'هارد دیسک ']
            find = raw_inp[key].replace(stg_type[2], '1')
            find = find.replace(stg_type[3], '2')
            find = find.replace(stg_type[0], '3')
            find = find.replace(stg_type[1], '4')
            outdict['Memory type'] = int(find)
    return outdict
