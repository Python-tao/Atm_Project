# __author__ = "XYT"
#全局配置文件。
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

'''
DATABASE:数据库相关的配置信息。
    engine:数据库类型
    name:数据库名，此文件数据库下可以有多个目录，分别用于不同的用途，accounts为用户账户相关，还可以放商品列表等等。
    path：数据库目录的绝对路径,Atm_Project\atm/db,此处的路径分隔使用了斜线，python能够正常识别。
    

'''
DATABASE = {
    'engine': 'file_storage', #support mysql,postgresql in the future
    'name':'accounts',
    'path': "%s/db" % BASE_DIR
}


#LOG_LEVEL = logging.INFO   #日志的脚本文件。
#日志类型的的字典文件。
# LOG_TYPES = {
#     'transaction': 'transactions.log',
#     'access': 'test.db',
# }



'''账户交易相关的配置文件。
repay:还款
    action:操作类型，plus表示账户金额增加，
    interest:利息，
withdraw:取款
transfer：转账
consume：用户在商场消费的操作时的配置信息。

'''
TRANSACTION_TYPE = {
    'repay':{'action':'plus', 'interest':0},
    'withdraw':{'action':'minus', 'interest':0.05},
    'transfer':{'action':'minus', 'interest':0.05},
    'consume':{'action':'minus', 'interest':0},

}