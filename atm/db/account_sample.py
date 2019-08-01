#用户账户数据库文件的模板。仅用于单独创建一个初始的jso格式的文件数据库。
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from conf import settings

import json

'''
acc_dic,账户数据库文件的示例。用于测试。
'''

acc_dic = {
    'id': 'Jerry',
    'password': 'abc',
    'credit': 15000,
    'balance': 15000,
    'enroll_date': '2016-01-02',
    'expire_date': '2021-01-01',
    'pay_day': 22,
    'status': 0 # 0 = normal, 1 = locked, 2 = disabled
}

json_file_addr="{}\{}\{}.json".format(settings.DATABASE['path'],settings.DATABASE['name'],acc_dic['id'])






def make_account():
    '''
    初始化用户数据库，
    返回：在accounts目录下的json文件。
    '''
    with open(json_file_addr, 'w') as f:
        a=json.dump( acc_dic,f)


def read_account():
    '''
    读取用户账户信息。
    返回json文件的内容。
    :return:
    '''
    with open(json_file_addr, 'r') as f:
        print(json.load(f))

def check_accounts_exist():
    print(os.path.isfile(json_file_addr))
    return
#print(type(acc_dic))
# print(check_accounts_exist)
#
make_account()
read_account()
