#商品列表数据库文件的模板。仅用于单独创建一个初始的json格式的文件数据库。
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from conf import settings

import json

'''
product_dic,商品数据库文件的示例。用于测试。

'''

# product_dic = [
# ['Iphone',5800],
# ['Ipad',1800],
# ['P30',9800],
# ['Mac Pro',12000],
# ['Starbuck Latte',31],
# ['Python book', 81],
# ['Bike', 800],
# ['iwatch',10600],
# ]


# account_dic = {
#     'id': 'Jerry',
#     'password': 'abc',
#     'user_type': 0,# 0 = 普通购物者, 1 = 商家
#     'enroll_date': '2016-01-02',
#     'expire_date': '2021-01-01',
#     'status': 0 # 0 = normal, 1 = locked, 2 = disabled
# }
# account_dic2 = {
#     'id': 'Admin',
#     'password': 'abc',
#     'user_type': 1,# 0 = 普通购物者, 1 = 商家
#     'enroll_date': '2016-01-02',
#     'expire_date': '2021-01-01',
#     'status': 0 # 0 = normal, 1 = locked, 2 = disabled
# }
old_order_list=[
['2019-06-18','Iphone',5800],
['2019-06-19','Bike',800],
]






# json_file_addr="{}\{}\{}.json".format(settings.DATABASE['path'],settings.DATABASE['name'],settings.DATABASE['db_table'])
# account_file_addr="{}\{}\{}.json".format(settings.ACCOUNT_BASE['path'],settings.ACCOUNT_BASE['name'],account_dic2['id'])
order_file_addr="{}\{}\{}.json".format(settings.OLD_ORDER_BASE['path'],settings.OLD_ORDER_BASE['name'],'Jerry')


print(order_file_addr)


def make_account():
    '''
    初始化用户数据库，
    返回：在accounts目录下的json文件。
    '''
    with open(order_file_addr, 'w') as f:
        a=json.dump( old_order_list,f)


def read_account():
    '''
    读取用户账户信息。
    返回json文件的内容。
    :return:
    '''
    with open(order_file_addr, 'r') as f:
        print(json.load(f))

# def check_accounts_exist():
#     print(os.path.isfile(json_file_addr))
#     return

make_account()
read_account()
