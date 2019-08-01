# __author__ = "xyt"
'''

主程序模组，处理所有用户交互相关事宜。

'''
import os
import sys
import time
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
atm_dir= os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)
sys.path.append(atm_dir)


from core import auth
from core import db_handler
from conf import settings
from core import accounts

from core import transaction
# from core.auth import login_required

user_data = {
    'account_id':None,
    'is_authenticated':False,
    'user_type':None,
    'shopping_cart':[],
    'account_data':None
}

def account_info(user_data):
    '''
    打印用户的账户信息，包括用户账号，是否认证成功，数据库信息。
    传入参数：
        acc_data:户的user_data,即用户当前的状态信息以及数据库信息。
    返回值：
        用户信息提示语。
    '''
    acc_info=''' --------- ACCOUNT INFO --------
            ID:          {}
            用户类型 :     {}
            enroll_date：{}
            expire_date：{}
            status：     {}
            '''.format(user_data['account_data']['id'],user_data['account_data']['user_type'],user_data['account_data']['enroll_date'],\
                   user_data['account_data']['expire_date'],user_data['account_data']['status'])

    print(acc_info)
    wait=input("press any key to continue..")

def buy_products(user_data):
    '''
    打印商品列表，提示用户选择商品，把商品加入购物车中。
    '''
    data = db_handler.file_db_handle("select * from product")
    while True:
        print("####以下为商品列表#####")
        print("项目\t商品名称\t\t单价")
        for index, item in enumerate(data):
            print("{}   {}\t{}".format(index,item[0],item[1]))
        user_choice = input("which product do you want?\n(press 'q' to quit)")
        if user_choice.isdigit():
            user_choice = int(user_choice)
            if user_choice < len(data) and user_choice >= 0:
                user_data['shopping_cart'].append(data[user_choice])
                print("{} has added to your cart...".format(data[user_choice]))
        elif user_choice == 'q':
             print('Back to Main Menu!')
             break
        else:
            print("Invalid input")



def check_cart(user_data):
    '''
    显示当前购物车中的商品，可以删除商品。
    '''
    cart_data=user_data['shopping_cart']
    while True:
        print("----当前购物车有以下商品----")
        print("项目\t商品名称\t\t单价")
        for index, item in enumerate(cart_data):
            print("{}   {}\t{}".format(index, item[0], item[1]))
        user_choice = input("which product do you want to delete?\n(press 'q' to quit)")
        if user_choice.isdigit():
            user_choice = int(user_choice)
            if user_choice < len(cart_data) and user_choice >= 0:
                print("{} had moved from your cart...".format(cart_data[user_choice]))
                cart_data.pop(user_choice)

        elif user_choice == 'q':
             print('Back to Main Menu!')
             user_data['shopping_cart']=cart_data
             break
        else:
            print("Invalid input")


    pass


def pay_bill(user_data):
    cart_data = user_data['shopping_cart']
    print("----正在进行账单结算----")
    print("----当前购物车有以下商品----")
    print("项目\t商品名称\t\t单价")
    sum=0
    for index, item in enumerate(cart_data):
        print("{}   {}\t{}".format(index, item[0], item[1]))
        sum+=float(item[1])
    print("总金额为：{}".format(sum))
    user_choice = input("请按任意键确认,按q键返回。。")
    if user_choice=='q':
        pass
    else:
        atm_account_data = accounts.load_atm_balance(user_data['account_id'])

        if atm_account_data:
            password = input("\033[32;1m请输入你的ATM信用卡密码:\033[0m").strip()#用户的密码
            if atm_account_data['password'] == password:
                exp_time_stamp = time.mktime(time.strptime(atm_account_data['expire_date'], "%Y-%m-%d"))
                if time.time() > exp_time_stamp:
                    print(
                        "\033[31;1mYour ATM Account [%s] has expired,please contact the bank to get a new card!\033[0m" % user_data['account_id'])
                else:  # 通过了信用卡密码认证。

                    wait_input=input("你的信用卡余额为：【{}】,本次交易金额为：【{}】,确认付款？".format(atm_account_data['balance'],sum))
                    print("开始交易。")
                    new_atm_account_data = transaction.make_transaction(atm_account_data, 'consume', sum)
                    if new_atm_account_data:
                        user_data['account_data']=new_atm_account_data
                        user_data['shopping_cart']=[]
                        print('''\033[42;1m你已经消费：%s，当前余额为:%s\033[0m''' %(sum,new_atm_account_data['balance']))

            else:
                print("你的信用卡账户或者密码有误！")

        else:
            print("你的ATM账户不存在，无法进行付款操作。")


def show_old_order(user_data):
    pass



def logout(user_data):
    exit("BoodBye!")





def shopping_menu(user_data):
    menu = u'''
       ======= 欢迎光临 =========
       ------- 又一个购物商场 ---------
       #############################
       \033[32;1m1.  账户信息
       2.  购物
       3.  查询&修改购物车
       4.  结账
       5.  查看历史订单
       6.  退出
       \033[0m'''

    menu_dic = {
        '1': account_info,
        '2': buy_products,
        '3': check_cart,
        '4': pay_bill,
        '5': show_old_order,
        '6': logout,
    }
    exit_flag = False
    while not exit_flag:
        print(menu)
        user_option = input(">>:").strip()
        if user_option in menu_dic:
            menu_dic[user_option](user_data)
        else:
            print("\033[31;1mOption does not exist!\033[0m")



def admin_menu(user_data):
    i=input("欢迎进入管理员菜单。")
    pass







def run():
    '''
    用途:
        此函数为程序入口，处理用户交互事宜。
    this function will be called right a way when the program started, here handles the user interaction stuff
    auth.acc_login(user_data),
    传入参数：
        user_data，用户状态信息的临时字典文件，有3个键，分别是用户账户id，认证状态信息，json文件内容。
    创建的参数：
        acc_data,如果通过的认证，就把用户的账号数据库json文件赋值给acc_data
    具体操作：
        调用auth.acc_login登陆函数，并且把user_data传入。acc_login处理用户登陆相关的操作。如果处理成功，
        就会返回登陆后的用户的json文件内容，并赋值给acc_data。
        此时的用户必定已经通过的认证，并且登陆状态为已经登陆。于是更新user_data['account_data']，把json内容赋值给
        临时状态文件。
        然后调用interactive交互函数，并传入user_data用户信息临时变量。

    '''

    acc_data = auth.acc_login(user_data)

    if user_data['is_authenticated']:
        user_data['account_data'] = acc_data
    if user_data['user_type']==1: #管理员
        admin_menu(user_data)
    elif user_data['user_type']==0:#普通用户
        shopping_menu(user_data)