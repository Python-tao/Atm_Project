# __author__ = "xyt"
'''

主程序模组，处理所有用户交互相关事宜。

'''
import os
import sys
import time
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)


from core import auth
from core import accounts
from core import transaction
from core.auth import login_required


'''
未登陆用户的初始数据，仅保存内存中，用于判断用户登陆状态等。
account_id,用户id信息，此处是指信用卡的账号。
is_authenticated,保存用户是否已经登陆的状态信息。
account_data，用户的账户数据库文件信息。
'''
user_data = {
    'account_id':None,
    'is_authenticated':False,
    'account_data':None
}


def account_info(acc_data):
    '''
    打印用户的账户信息，包括用户账号，是否认证成功，数据库信息。
    传入参数：
        acc_data:户的user_data,即用户当前的状态信息以及数据库信息。
    返回值：
        用户信息提示语。
    '''
    acc_info=''' --------- ACCOUNT INFO --------
            ID:          {}
            Credit :     {}
            Balance:     {}
            enroll_date：{}
            expire_date：{}
            status：     {}
            '''.format(acc_data['account_data']['id'],acc_data['account_data']['credit'], \
                   acc_data['account_data']['balance'],acc_data['account_data']['enroll_date'],\
                   acc_data['account_data']['expire_date'],acc_data['account_data']['status'])

    print(acc_info)
    wait=input("press any key to continue..")

@login_required
def repay(acc_data):    #还款
    '''
    打印当前的余额，并让用户执行还款操作。
    print current balance and let user repay the bill
    传入参数:
        acc_data,就是user_data
    创建变量：
        account_data,用户的json数据库信息。
        current_balance，提示语，提示用户的当前额度以及余额。
        repay_amount，还款金额。
        new_account_data,还款后的用户账户的json信息。

    后续操作:
        accounts.load_current_balance(acc_data['account_id'])
            把用户卡号传递给accounts模块的load_current_balance函数，此函数会返回用户的json数据库信息。
        打印用户的余额信息提示语。
        要求用户输入还款金额，判断用户输入信息的内容正确性。提交给transaction.make_transaction函数处理，
        传递给make_transaction3个参数，用户的json数据库信息,操作类型，还款的金额。
        交易函数处理完后，如果处理正常，就返回交易后的新的json数据库信息。否则返回一个空值。
        判断交易是否成功
            如果成功，提示新的余额的金额。并更新user_data临时文件状态。
            如果失败，提示输入的还款金额，不是一个合法的数字。
    返回值:
        如果处理成功，就返回提示新的余额的金额。
        如果处理失败，提示输入的还款金额不合法。
        如果输入b，就退出循环，结束repay函数。

    '''


    account_data = accounts.load_current_balance(acc_data['account_id'])

    current_balance= ''' ---------ID:%s BALANCE INFO --------
        Credit :    %s
        Balance:    %s''' %(account_data['id'],account_data['credit'],account_data['balance'])
    print(current_balance)
    back_flag = False
    while not back_flag:
        print("Press 'b' back to Main menu.")
        repay_amount = input("\033[33;1mInput repay amount:\033[0m").strip()
        if repay_amount == 'b':
            back_flag = True
            print("Back to menu.")
        elif len(repay_amount) >0 and repay_amount.isdigit():
            new_account_data = transaction.make_transaction(account_data,'repay', repay_amount)
            if new_account_data:
                user_data['account_data'] = new_account_data
                print('''\033[42;1mNew Balance:%s\033[0m''' %(new_account_data['balance']))

        else:
            print('\033[31;1m[%s] is not a valid amount, only accept integer!\033[0m' % repay_amount)

@login_required
def withdraw(acc_data):
    '''
    处理用户提款操作。
    print current balance and let user do the withdraw action
    输入参数：
        acc_data，用户的user_data,即用户当前的状态信息以及数据库信息。

    创建参数：
        account_data，用户账户的json信息
        current_balance，提示语，提示用户的当前额度，以及余额。
        new_account_data，交易后的用户账户的json信息。
        withdraw_amount，用户的提款金额。
        new_account_data，交易后的用户账户的json信息
    后续操作：
        打印户的当前额度，以及余额。
        提示用户输入提款的金额，初步判断输入金额的合法性。
        调用transaction.make_transaction(account_data,'withdraw', withdraw_amount)，处理交易，
        并传入参数，用户账户的json信息，交易的类型，提款金额。
        待make_transaction处理，如果处理正常会返回交易后的用户账户的json信息,如果失败会返回空值。
        判断交易是否成功，如果成功，就提示新的余额的金额，并更新user_data临时文件状态。。如果交易失败，就进行下次循环，要求用户输入提款金额。


    返回值：
        如果交易处理成功，就提示新的余额的金额。
        如果交易失败，就进行下次循环，直到用户输入b，就跳出withdraw函数，返回调用者。


    '''
    account_data = accounts.load_current_balance(acc_data['account_id'])
    current_balance= ''' ---------ID:%s BALANCE INFO --------
        Credit :    %s
        Balance:    %s''' %(account_data['id'],account_data['credit'],account_data['balance'])
    print(current_balance)
    back_flag = False
    while not back_flag:
        print("Press 'b' back to Main menu.")
        withdraw_amount = input("\033[33;1mInput withdraw amount:\033[0m").strip()
        if withdraw_amount == 'b':
            back_flag = True
            print("Back to menu.")
        elif len(withdraw_amount) >0 and withdraw_amount.isdigit():
            new_account_data = transaction.make_transaction(account_data,'withdraw', withdraw_amount)
            if new_account_data:
                user_data['account_data'] = new_account_data
                print('''\033[42;1mNew Balance:%s\033[0m''' %(new_account_data['balance']))

        else:
            print('\033[31;1m[%s] is not a valid amount, only accept integer!\033[0m' % withdraw_amount)



def transfer(acc_data):
    '''
    转账

    输入参数：
        acc_data，用户的user_data,即内存中的用户当前的状态信息以及数据库信息。
    创建变量：
        account_data，用户账户的json数据库信息。
        current_balance，用于余额提示语。
        transfer_amount，转账金额。
        transfer_account，收款人的账户。
        transfer_account_data，收款人的json数据库内容。
        new_account_data，当前用户执行完交易后返回的json数据库内容。
        new_transfer_account_data，收款人行完交易后返回的json数据库内容。

    执行过程：
         提示用户输入收款人的id，调用accounts.load_current_balance，检查该id的json文件是否存在。
         如果不存在，就提示出错。
        提示用户输入转账金额。调用transaction.make_transaction函数，把当前用户的账户余额减去转账金额。
        如果交易成功，就再次调用make_transaction函数，把转账金额转入收款人的账户。
        当以上2步都执行成功，才会完成整个转账操作。
        make_transaction函数传入以下几个参数：
            account_data，交易的用户json文件信息。
            'transfer'，交易类型
            transfer_amount，转账金额。
        make_transaction函数进行处理，可能返回以下值
            如果交易失败，返回 None，
            如果交易成功，返回account_data，此处的account_data为交易后的用户的json库内容。

    返回值：
        返回交易成功后的当前用户的json数据信息，以及收款人的json数据信息。
    '''
    account_data = accounts.load_current_balance(acc_data['account_id'])
    current_balance= ''' ---------ID:%s BALANCE INFO --------
        Credit :    %s
        Balance:    %s''' %(account_data['id'],account_data['credit'],account_data['balance'])
    print(current_balance)
    back_flag = False
    while not back_flag:

        transfer_account = input("\033[33;1mInput Which Account ID transfer to:\033[0m").strip()
        if len(transfer_account) > 0 and transfer_account.isalnum():
            transfer_account_data = accounts.load_current_balance(transfer_account)
            if transfer_account_data==None:
                print("\033[31;1m ID:[{}] doesn't exists !\033[0m".format(transfer_account))
                continue
            elif transfer_account_data:
                print("You are going to transfer to USER:【{}】!".format(transfer_account))
        else:
            print('\033[31;1m[{}] is not a valid Account ID!\033[0m'.format(transfer_account))
            continue
        print("Press 'b' back to Main menu.")
        transfer_amount=input("\033[33;1mInput transfer amount:\033[0m").strip()
        if transfer_amount == 'b':
            back_flag = True
            print("Back to menu.")
        elif len(transfer_amount) > 0 and transfer_amount.isdigit():
            new_account_data = transaction.make_transaction( \
            account_data, 'transfer', transfer_amount)
            if new_account_data:
                new_transfer_account_data = transaction.make_transaction( \
                    transfer_account_data, 'repay', transfer_amount)
                if new_transfer_account_data:
                    print("Amount [{}] has been transfer to ID:[{}]".format(transfer_amount,new_transfer_account_data['id']))
                    print('''\033[42;1mID:【{}】,Your New Balance:{}\033[0m''' .format (new_account_data['id'],new_account_data['balance']))

        else:
            print('\033[31;1m[%s] is not a valid amount, only accept integer!\033[0m' % transfer_amount)















def pay_check(acc_data):
    '''
    账单查询
    :param acc_data:
    :return:
    '''
    pass
def logout(acc_data):
    '''
    退出。

    :param acc_data:
    :return:
    '''

    print("Goodbye!!")
    exit()



def interactive(acc_data):
    '''
    作用：
        与用户进行交互。interact with user
    传入参数：
        acc_data，用户的user_data,即用户当前的状态信息以及数据库信息。
    创建变量：
        menu，显示菜单，前面加u，表示使用unicode编码格式。
        menu_dic,用一个字典变量，把用户的选择与后续操作联系起来，key为用户输入的选择，value为各个函数。
        exit_flag，用户退出操作的标识符。
    后续操作：
        显示菜单，提示用户输入选择项。
        判断用户的选择：
            使用choice in menu_dic,可以判断字典中的键是否存在，如果返回true，表示存在。
        如果是菜单中的某个选择，就运行对应的处理函数，并且把userdata作为参数传给处理函数。
        如果没有该选择，就提示无此操作，并重新显示菜单。
    返回值：
        这是个死循环，没有返回值，只是区分操作类型，并交给后续的处理函数,并且把userdata作为参数传给处理函数。
        处理函数执行完后，就回到当前的循环，继续询问操作。
        如果用户选择了退出，就跳出循环，结束程序。



    :return:
    '''
    menu = u'''
    ------- Sky And Land Bank ---------
    \033[32;1m1.  账户信息
    2.  还款(功能已实现)
    3.  取款(功能已实现)
    4.  转账(功能已实现)
    5.  账单(未实现)
    6.  退出
    \033[0m'''


    menu_dic = {
        '1': account_info,
        '2': repay,
        '3': withdraw,
        '4': transfer,
        '5': pay_check,
        '6': logout,
    }
    exit_flag = False
    while not exit_flag:
        print(menu)
        user_option = input(">>:").strip()
        if user_option in menu_dic:
            menu_dic[user_option](acc_data)

        else:
            print("\033[31;1mOption does not exist!\033[0m")













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



    :return:
    '''
    acc_data = auth.acc_login(user_data)

    if user_data['is_authenticated']:
        user_data['account_data'] = acc_data
        interactive(user_data)