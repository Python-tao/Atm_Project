#!_*_coding:utf-8_*_
#__author__:"Alex Li"

from conf import settings
from core import accounts
# from core import logger
#transaction logger



def make_transaction(account_data,tran_type,amount,*args,**others):
    '''
    处理用户账户交易的所有操作的函数。
    deal all the user transactions
    传递给make_transaction3个参数：
        :param account_data: user account db，用户的json数据库信息
        :param tran_type: transaction type，交易操作类型
        :param amount: transaction amount，交易操作的金额
        :param others: mainly for logging usage,其它扩展用的参数组。
    创建的变量：
        amount，把传入的交易的金额，变成浮点数并存入变量amount。
        interest，本地交易操作的利息。
        old_balance，账户余额。
        new_balance，交易后的金额数。

    执行的操作：
        首先判断交易类型，是否为全局配置文件中的定义的交易类型的中的一种，分别有还款，提款，转账，消费。
        如果交易类型存在，判断交易操作的方法，
            如果操作的方法为plus，则把交易金额添加入账户余额中。
            如果操作的方法为minus，则从交易金额中，减去交易金额以及利息。
                如果减完后的金额为负数，就返回提示信息：”你当前的额度不足完成本次提款操作，你的余额为***“,退出此函数，并返回一个空值。
            如果交易后的金额正常，就更新用户的json数据库中的余额信息。
            然后通过accounts.dump_account(account_data)函数把更新后的json信息写入到json文件中。
            并返回更新后的用户账户json信息。
        如果交易类型不存在，就返回错误提示。

    返回值：
        如果正常运行，就返回交易后的用户账户json信息。
        否则，返回一个空值。



    '''
    amount = round(float(amount),2)
    if tran_type in  settings.TRANSACTION_TYPE:

        interest =  round(amount * settings.TRANSACTION_TYPE[tran_type]['interest'],2)
        old_balance = account_data['balance']
        if settings.TRANSACTION_TYPE[tran_type]['action'] == 'plus':
            new_balance = round(old_balance + amount + interest,2)
        elif settings.TRANSACTION_TYPE[tran_type]['action'] == 'minus':
            new_balance = round(old_balance - amount - interest,2)
            #check credit
            if  new_balance <0:
                print('''\033[31;1mYour credit [%s] is not enough for this transaction [-%s], your current balance is
                [%s]''' %(account_data['credit'],(amount + interest), old_balance ))
                return None

        account_data['balance'] = new_balance
        accounts.dump_account(account_data) #save the new balance back to file
        # log_obj.info("account:%s   action:%s    amount:%s   interest:%s" %
        #                   (account_data['id'], tran_type, amount,interest) )

        return account_data
    else:
        print("\033[31;1mTransaction type [%s] is not exist!\033[0m" % tran_type)
