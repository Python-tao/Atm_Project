#Author:xyt
'''
handle all the database interactions
'''
import json,time ,os,sys
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(base_dir)
sys.path.append(base_dir)


from  conf import settings



def file_db_handle(conn_params):
    '''
    parse the db file path
    文件数据库的处理函数。
    :param conn_params: the db connection params set in settings，全局配置文件中的数据库信息参数。
    :return:返回一个文件操作的函数的内存地址。
    '''
    #print('file db:',conn_params)   #打印系统数据库参数。
    #db_path ='%s/%s' %(conn_params['path'],conn_params['name'])
    return file_execute     #返回文件操作模块的内存地址。




def file_execute(sql,**kwargs):
    '''
    文件操作模块。或者叫做db_api模块，
    处理数据库查询，更新等操作。并且判断用户账号是否存在是由此部分提供的。

    字符串的split方法：把字符串按照指定关键字分隔成2个元素。

    传入的参数:
        sql:#内部使用的一个数据库交互语句，目的是适配不同的增删改查操作。，比如：‘select * from accounts where account=1234’
        **kwargs: 字典参数组，传入一个字典变量作为参数。
    创建的参数：
        conn_params，再次获取主配置文件中的数据库参数信息，即数据库类型，数据库名，数据库绝对路径。
        db_path:文件数据库目录，此处为Atm_Project\atm/db/accounts
        sql_list，把自定义的查询语句根据关键字where拆分成2个元素的列表。
            比如：sql_list此处为['select * from accounts ', ' account=1234']
            后续根据语句字段[0]的内容分别进行不同的操作。
                如果是select开头，就判断该账户数据库文件是否存在，如果存在就提取并返回json格式的账户信息。
                如果是update开头，就执行写入数据库的操作。
        column,val ，把sql_list第二个元素继续拆分后的值，比如，account，1234
        account_file，用户账户数据库文件的绝对路径，此处为Atm_Project\atm/db/accounts/1234.json
        account_data，从kwargs字典变量组中，传入了新的用户账户信息文件，
        于是获取关键字为"account_data"的数据，并赋值到account_data。

    需要注意的方法:
        os.path.isfile()，指定一个文件路径，判断是否存在，存在就返回true。
        把列表元素赋值给变量的方法:
            注意此处的通过类别赋值的操作：a,b=[1,2]，则a=1,b=2。
        kwargs.get("account_data")


    具体的操作：
        首先获取主配置文件的数据库类型信息。通过此信息获取数据库文件所在的目录路径。
        使用第一次的split方法获取2个字段，第一个字段用于判断是执行select还是update,第二个字段用于获取数据文件的绝对路径。
            如果是select操作：
                对sql查询语句的第二个字段再次split，获取了column数据库类型字段，以及val,用户账户id的值。
                如果column为account，就生成json数据库文件的绝对路径。
                使用os.path.isfile方法判断json文件是否存在。
                    如果账号文件存在，就打开此文件，并用load方法读取json数据的内容，把内容赋值给变量account_data。
                    如果账号文件不存在，就直接退出程序，并打印错误提示。
            如果是updata操作：
                update语句下的操作，并且有where子句存在。先取出where子句中的字段名和值，如账号id和值。
                并把字段名和值，赋值给变量，column, val，生成json账号文件的绝对路径。
                判断json账户文件是否存在，如果存在，就通过kwrgs.get方法获取待更新的用户数据文件。
                然后使用json.dump把待更新的数据写入json文件中。
    返回值：
        如果是查询语句，
            正常情况下，返回读取到的json数据库的内容。
            否则，直接退出程序，返回用户不存在的提示信息。
        如果是更新语句，updata操作完成后，返回值为True，表示更新操作顺利完成。
    '''
    conn_params = settings.DATABASE #再次获取数据库参数信息。
    db_path = '%s/%s' % (conn_params['path'], conn_params['name'])
    print(sql,db_path)
    print(sql,db_path)
    sql_list = sql.split("where")   #把查询语句拆分成列表。
    if sql_list[0].startswith("select") and len(sql_list)> 1:#如果列表元素大于1，说明有where子句。
        column,val = sql_list[1].strip().split("=")     #把where子句再次拆分，一个是字段名，一个是值。
        if column == 'account':
            account_file = "%s/%s.json" % (db_path, val)

            if os.path.isfile(account_file):
                with open(account_file, 'r') as f:
                    account_data = json.load(f)
                    return account_data
            else:
                return None
                #exit("\033[31;1mAccount [%s] does not exist!\033[0m" % val )

    elif sql_list[0].startswith("update") and len(sql_list)> 1:

        column, val = sql_list[1].strip().split("=")
        if column == 'account':
            account_file = "%s/%s.json" % (db_path, val)
            if os.path.isfile(account_file):
                account_data = kwargs.get("account_data")#待更新的用户数据文件。
                with open(account_file, 'w') as f:
                    json.dump(account_data, f)
                return True















def db_handler():
    '''
    通过读取全局配置文件中的数据库连接参数，判断数据库的类型，根据不同的类型，执行不同的操作。
    :param conn_parms: the db connection params set in settings,数据库的连接参数，包括数据库类型，数据库名称，数据库文件的绝对路径。
    :return:a
    '''
    conn_params = settings.DATABASE#获取数据库连接参数
    if conn_params['engine'] == 'file_storage':
        return file_db_handle(conn_params)  #判断数据库类型，如果是文件数据库，就交给文件数据库处理函数。
    elif conn_params['engine'] == 'mysql':
        pass #todo如果是sql数据库，就交给sql数据库处理函数。待更新。



file_execute("select * from accounts where account=Jerry in ATM")