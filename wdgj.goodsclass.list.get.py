import json

import requests
import time
import hashlib

# content = {'ckey': "<trade_order_info><trade_order></trade_order></trade_order_info>"}
AppSecret = '6f93ledk8c5b6noa620f46c5de2i5gfe'
pageno = 1
total_products = []
while True:
    data = {'Appkey': '55057521',
            'Accesstoken': '1f16c156608b43feb4dec5ad75fbbcca',
            'Format': 'json',
            'Versions': '1.1',
            'Method': "wdgj.goodsclass.list.get",
            'Pageno': pageno,
            'Pagesize': '100',
            'ckey': '<trade_order_info><trade_order></trade_order></trade_order_info>',
            'Timestamp': int(time.time())}

    # for ckey in content:
    #     data[ckey] = content[ckey]
    sorted_key_list = []
    for item in data:
        sorted_key_list.append(data[item])
    sorted_key_list = sorted(sorted_key_list, key=str)
    sign = '{}'.format(AppSecret)
    for key in sorted_key_list:
        sign = '{}{}'.format(sign, key)
    sign = '{}{}'.format(sign, AppSecret)
    hl = hashlib.md5()
    hl.update(sign.encode(encoding='utf-8'))
    sign = hl.hexdigest()

    data["sign"] = str(sign)
    print("Start page " + str(pageno))
    r = requests.post("http://api.wdgj.com/wdgjcloud/api", data=data)
    if "datalist" not in r.json():
        print(f"Total products founded {len(total_products)}")
        with open('wdgj.goodsclass.list.get.json', 'w') as file:
            json.dump(total_products, file)
        break
    else:
        pageno += 1
        response_dict = json.loads(r.text)
        filtered_prod = [item for item in response_dict['datalist']
                         # if (item['stock'] != '0.0000' and ('机械表' in item['goodsname'] or '石英表' in item['goodsname'] or '表带' in item['goodsname']))
                         ]
        # hi guys, the api works now, but i have a question, there are some kind of filters that can allow me to get only the watches? for now i am filtering by finding in "goodsname": '机械表', '石英表' or '表带', but with stock >0 i get more that 500 products, is it normal? i noticed also that the stock is doubled as compared the qty that you send in the xlsx file, example the reference 'YA157404' has stock 6 from the api but you put 3 in the xlsx file, why this? can you resolve my doubts?
        # 表带 cinghia
        # 机械表 orologio meccanico
        # 石英表 Orologi al quarzo
        total_products += filtered_prod
        # filtered_prod = [item for item in response_dict['datalist']]
        # total_products += filtered_prod
        print(
            f"End page {str(pageno)}, status code:{r.status_code}, products founded in this page:{len(filtered_prod)}, total founded:{len(total_products)}")
