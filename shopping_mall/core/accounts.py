


from core import db_handler
from conf import settings


def load_atm_balance(account_id):
    '''
    用于查询账户余额信息。
    return account balance and other basic info
    传入参数：
        account_id:用户的卡号
    创建参数：
        db：为该用户卡号的json数据库信息。
    处理动作:
        把file_execute函数重命名为db_api。
        把查询操作语句传递给db_api("select * from accounts where account=%s" % account_id)，
        db_api会返回该用户卡号的json数据库信息。
    返回值：
        db：为该用户卡号的json数据库信息。
    '''
    data = db_handler.file_db_handle("select * from accounts where account=%s in ATM" % account_id)
    return data


def dump_atm_account(account_data):
    '''
    交易操作完成后，把更新后的用户账户json信息写入数据库。
    after updated transaction or account db , dump it back to file db
    传入参数：
        account_data:更新后的用户账户json信息
    创建参数：
        db_api，file_execute函数的重命名。
    执行的操作：
        运行db_api，也就是file_execute函数，并传入参数，数据库操作语句以及更新后的用户账户json信息。


    返回值:

    '''
    data = db_handler.file_db_handle("update from accounts where account=%s in ATM" % account_data['id'],account_data=account_data)



    return True