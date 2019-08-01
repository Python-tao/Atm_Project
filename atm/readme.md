# 主题：ATM信用卡账户管理工具

需求：
    给用户提供一个与信用卡账户进行交互的界面。提供了提款、还款、转账、查询余额等功能。


# 提款
```
    打印户的当前额度，以及余额。
    提示用户输入提款的金额，初步判断输入金额的合法性。
    调用make_transaction模块处理交易，
    判断交易是否成功，如果成功，就提示新的余额的金额，并更新user_data临时文件状态。
```
# 还款
```
打印户的当前额度，以及余额。
要求用户输入还款金额，提交给make_transaction模块处理，
如果成功，提示新的余额的金额。并更新user_data临时文件状态。 
    
```

# 转账
```
提示用户输入收款人的id，调用accounts模块，检查该收款人的id是否有效。
提示用户输入转账金额。调用transaction模块，把当前用户的账户余额减去转账金额。
如果成功，就再次调用transaction模块，把转账金额转入收款人的账户。
当以上2步都执行成功，才会完成整个转账操作。
如果交易成功，返回true。
```



# 数据库结构：
```
    id,用户id
    password,用户密码
    credit，额度
    balance，余额
    enroll_date,注册日期
    expire_date,失效日期
    pay_day,还款日期
    status,账户的状态。
    
```
# 目录结构
```
- bin 
    -atm.py        程序启动入口
- conf
    -settinggs.py   全局配置文件，保存用户账户文件的路径以及账户交易相关的配置信息。
    
-core               核心代码
    -main.py        主函数，包括交互主菜单，打印账户信息的函数，提款，还款，转账的函数。
    -accounts.py     与用户账户进行交互的中间函数。
    -auth.py        用用户登陆时的密码验证相关的模块。
    -db_handler.py      与数据库文件进行直接操作的引擎。
    -transaction.py      与账户交易（提款，还款，转账）相关的操作。
-db                 本地json数据库管理
    -accounts文件夹      保存各个用户的账户文件的目录。
        -Jack.json      jack用户的账户文件。
    -account_sample.py  json数据库数据结构的初始化
-logs           与日志功能相关的文件夹。日志功能未完成。

readme.md       readme文件



```