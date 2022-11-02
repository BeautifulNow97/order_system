# 导入PyMySQL库
import datetime
import pandas as pd
import pymysql
import re
import logger

log_sql = logger.Logger("debug")
# 导入数据库的配置信息
from config.settings import DB_CONFIG

# dept 部门表（deptno 部门编号/dname 部门名称/loc 地点）
sql_create = """
        CREATE TABLE `dept` (
               deptno int primary key COMMENT '部门编号',
               dname varchar(30) COMMENT '部门名称',
               loc varchar(30) COMMENT '地点'
            ) ENGINE = InnoDB DEFAULT CHARSET=utf8mb4;
    """

sql_insert = """
            INSERT INTO dept VALUES(10, '总经办', '本部'), (20, '行政部', '本部'),(30, '人事部', '本部'),(40, '财务部', '本部'),  (50, '运营部', '本部'),(60, '数据部', '本部'),(70, '业务一部', '本部'),(80, '业务二部', '本部')
        """

# emp 员工表（empno 员工号/ename 员工姓名/job 工作/mgr 上级编号/hiredate 受雇日期/sal 薪金/comm 佣金/deptno 部门编号）
sql_create = """
            create table emp(
               empno int primary key COMMENT '员工号',
               ename varchar(10) COMMENT '员工姓名',
               job varchar(10) COMMENT '工作',
               sex varchar(5) COMMENT '性别',
               idcard varchar(20) COMMENT '身份证号码',
               bank_id char(30) COMMENT '银行账号',
               bank_address varchar(255) COMMENT '开户行',
               tel varchar(20) COMMENT '联系电话',
               hiredate DATE COMMENT '受雇日期',
               sal DECIMAL(7,2) COMMENT '薪金',
               deptno int COMMENT '部门编号',
               foreign key(deptno) references dept(deptno))
               ENGINE = InnoDB DEFAULT CHARSET=utf8mb4;

    """

sql_insert_emp = """
                INSERT INTO emp VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """

# 客户表信息表
sql_create = """
         CREATE TABLE `customer` (
              `id` int NOT NULL AUTO_INCREMENT,
              `name` varchar(128) NOT NULL DEFAULT '' COMMENT '客户姓名',
              `prefix` varchar(32) NOT NULL UNIQUE DEFAULT '' COMMENT '客户前缀',
              `tel` varchar(64) NOT NULL DEFAULT '' COMMENT '客户电话',
              `idcard` char(18) NOT NULL DEFAULT '0' COMMENT '客户身份证号',
              `bank_id` varchar(128) NOT NULL DEFAULT '' COMMENT '客户银行卡号',
              `bank_address` varchar(128)  DEFAULT '' COMMENT '客户开户行',
              `remark` varchar(128) NOT NULL DEFAULT '无' COMMENT '客户备注',
              `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
              `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
              `empno` int COMMENT '员工号',
              PRIMARY KEY (`id`),
              foreign key(empno) references emp(empno)
            ) ENGINE = InnoDB DEFAULT CHARSET=utf8mb4;
            
    """
sql_insert_customer = """
                    INSERT INTO customer(name,prefix,tel,empno) VALUES (%s,%s,%s,%s)
                """
# 账号表
sql_create = """

          create table account(
          id int primary key auto_increment,
          name varchar(15) not null COMMENT '客户姓名' ,
          account varchar(30) not null unique COMMENT '账号名称' ,
          account_status Boolean not null comment '账号状态',
          `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
          `use_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '使用时间',
          customer_id int , 
          foreign key(customer_id) references customer(id)
            ) ENGINE = InnoDB DEFAULT CHARSET=utf8mb4;
"""
sql_account = "insert into account(name,tel,account,account_status) values (%s,%s,%s,%s)"

# 订单表
sql_create = '''
            create table t_order(
                id INT auto_increment COMMENT '订单ID',
                company varchar ( 255 ) DEFAULT '轩利兴' NOT NULL COMMENT '公司名称',
                dname varchar ( 255 ) NOT NULL COMMENT '公司部门',
                empno INT NOT NULL COMMENT '员工ID',
                emp_date  date NOT NULL COMMENT '员工下单日期',
                order_num INT(64)  NOT NULL COMMENT '订单数量',
                customer_id INT NULL COMMENT '客户id',
                pay_type TINYINT NOT NULL COMMENT '支付方式：1网站、2微信、3支付宝、4转私/公',
                account_id VARCHAR ( 255 ) DEFAULT '请输入账号' NOT NULL COMMENT '网站登录账号',
                account_pwd VARCHAR ( 255 ) DEFAULT '123456' NOT NULL COMMENT '网站账号密码：默认123456',
                create_time datetime DEFAULT CURRENT_TIMESTAMP NOT NULL COMMENT '订单创建时间',
                remark VARCHAR ( 255 ) DEFAULT '无' NULL COMMENT '订单备注'
            ) COMMENT '订单表', ENGINE = InnoDB DEFAULT CHARSET=utf8mb4;
  '''

# 下单表
sql_create = """
            drop table if exists tb_down_order;
            CREATE TABLE tb_down_order (
                `id` INT PRIMARY KEY auto_increment COMMENT '下单表自增ID',
                `empno` INT NOT NULL COMMENT '员工工号',
                `ename` VARCHAR(255) NOT NULL COMMENT '员工姓名',
                `dname` VARCHAR(255) NOT NULL COMMENT '部门',
                `customer_id` VARCHAR(255) NOT NULL COMMENT '客户姓名（id）外键',
                `web_order_number` SMALLINT UNSIGNED NOT NULL DEFAULT 0 COMMENT '网站下单数量，范围0〜65535',
                `web_order_account` VARCHAR ( 255 ) NOT NULL DEFAULT '无' COMMENT '网站下单账号',
                `not_web_order_number` SMALLINT UNSIGNED NOT NULL DEFAULT 0 COMMENT '非网站下单数量，范围0〜65535',
                `not_web_order_account` VARCHAR ( 255 ) NOT NULL DEFAULT '无' COMMENT '非网站下单账号',
                `order_date` date NOT NULL COMMENT '下单日期',
                `order_cycle` TINYINT UNSIGNED NOT NULL COMMENT '下单周期,范围0 〜255',
                `order_total` SMALLINT UNSIGNED NOT NULL COMMENT '总下单量，范围0〜65535',
                `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '在数据库中创建时间',
                `update_time` TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '在数据库中创建时间'
            )ENGINE = INNODB DEFAULT CHARSET = utf8mb4;
"""

# 下单表
sql_create = """
            drop table if exists tb_wechat;
            CREATE TABLE tb_down_order (
                `id` INT PRIMARY KEY auto_increment COMMENT '下单表自增ID',
                `ename` VARCHAR(255) NOT NULL COMMENT '员工姓名',
                `submission_time` datetime COMMENT '员工提交订单时间',
                `empno` INT NOT NULL COMMENT '员工工号',
                `dname` VARCHAR(255) NOT NULL COMMENT '部门',
                `customer_id` VARCHAR(255) NOT NULL COMMENT '客户姓名（id）外键',
                `web_order_number` SMALLINT UNSIGNED NOT NULL DEFAULT 0 COMMENT '网站下单数量，范围0〜65535',
                `web_order_account` VARCHAR ( 255 ) NOT NULL DEFAULT '无' COMMENT '网站下单账号',
                `not_web_order_number` SMALLINT UNSIGNED NOT NULL DEFAULT 0 COMMENT '非网站下单数量，范围0〜65535',
                `not_web_order_account` VARCHAR ( 255 ) NOT NULL DEFAULT '无' COMMENT '非网站下单账号',
                `order_date` date NOT NULL COMMENT '下单日期',
                `order_cycle` TINYINT UNSIGNED NOT NULL COMMENT '下单周期,范围0 〜255',
                `order_total` SMALLINT UNSIGNED NOT NULL COMMENT '总下单量，范围0〜65535',
                `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '在数据库中创建时间',
                `update_time` TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '在数据库中创建时间'
            )ENGINE = INNODB DEFAULT CHARSET = utf8mb4;
"""

sql_tb_down_order = """
                insert into tb_down_order(
                ename,submission_time,dname,customer_id,web_order_number,web_order_account,
                not_web_order_number,not_web_order_account,order_date,order_cycle,order_total) 
                values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""


class MysqlUtil:
    """
    数据库操作类
    """

    def __init__(self):
        self.cursor = None
        self.db = None

    def open(self):
        # 读取配置文件，初始化pymysql数据库连接
        self.db = pymysql.connect(**DB_CONFIG)
        # 创建数据库游标  返回字典类型的数据
        self.cursor = self.db.cursor(cursor=pymysql.cursors.DictCursor)

    # 获取单条数据
    def get_fetchone(self, sql):
        self.open()
        self.cursor.execute(sql)
        # print("sql是", sql)
        self.close()
        return self.cursor.fetchone()

    # 获取多条数据
    def get_fetchall(self, sql):
        self.open()
        self.cursor.execute(sql)
        # print("sql是", sql)
        self.close()
        return self.cursor.fetchall()

    # 执行更新类sql
    def sql_execute(self, sql):
        try:
            # db对象和指针对象同时存在
            self.open()
            if self.db and self.cursor:
                print("sql是", sql)
                self.cursor.execute(sql)
                # 提交执行sql到数据库，完成insert或者update相关命令操作，非查询时使用
                self.db.commit()
                # print("sql执行成功！")
                self.close()
                return True
        except Exception as e:
            # 出现异常时，数据库回滚
            self.db.rollback()
            print("sql执行失败！", e)
            self.close()
            return False

    def sql_executemany(self, sql, value):
        try:
            self.open()
            # db对象和指针对象同时存在
            if self.db and self.cursor:
                print("sql是", sql)
                self.cursor.executemany(sql, value)
                # 提交执行sql到数据库，完成insert或者update相关命令操作，非查询时使用
                self.db.commit()
                print(f"sql执行成功！{value}")
                self.close()
                return True
        except Exception as e:
            # 出现异常时，数据库回滚
            self.db.rollback()
            print("sql执行失败！", e)
            self.close()
            return False

    def to_excel(self, name, path=r'D:\04PrivateDrive\SetWin10\mysql_test\outsql.xlsx'):
        sql = f"""select * from {name} """
        res = self.get_fetchall(sql)
        data_df = pd.DataFrame(res)
        print(data_df)
        data_df.to_excel(path, index=False)
        return data_df

    # 关闭对象，staticmethod静态方法，可以直接使用类名.静态方法
    # @staticmethod
    def close(self):
        # 关闭游标对象
        if self.cursor is not None:
            self.cursor.close()
        # 关闭数据库对象
        if self.db is not None:
            self.db.close()


def inset_new_dept(inset_dept_name: str, inset_loc: str = '本部'):
    """
    插入部门
    :param inset_dept_name: 部门名称
    :param inset_loc: 部门地址
    :return:

    inset_dept('浩宇星空部', '分公司')
    inset_dept('行政1部', '分公司')
    """
    mysql = MysqlUtil()
    # 获取当前最大部门编号，薪增部门自动加10
    query_sql = """select max(deptno) as max_deptno from dept"""
    res = mysql.get_fetchone(query_sql)
    inset_deptno = res['max_deptno'] + 10
    # 插入值
    inset_sql = f"""INSERT INTO dept(deptno,dname,loc) VALUES({inset_deptno}, '{inset_dept_name}', '{inset_loc}')"""
    mysql.sql_execute(inset_sql)
    mysql.close(mysql)


def add_emp_message(insert_message: dict) -> bool:
    """
    新增员工信息
    :param insert_message:
    :return:bool
    """
    dic = {'提交人': '张先生',
           '类型': '员工信息录入',
           '部门': '数据部',
           '岗位': '数据专员',
           '入职日期': '2022-10-01',
           '姓名': '黄生会',
           '性别': '男',
           '电话': '18702303793',
           '身份证': '510225197110086547',
           '开户行': '中国建设银行南坪支行',
           '卡号': '6227003762610012416'}

    mysql = MysqlUtil()
    # 获取当前最大员工编号，薪增员工自动加1
    query_sql = """select max(empno) as max_empno from emp"""
    query_deptno = f"""select  deptno from dept where dname ='{insert_message['部门']}'"""
    res = mysql.get_fetchone(query_sql)

    empno = res['max_empno'] + 1
    ename = insert_message['姓名']
    job = insert_message['岗位']
    mgr = 0
    sex = insert_message['性别']
    idcard = insert_message['身份证']
    bank_id = insert_message['卡号']
    bank_address = insert_message['开户行']
    tel = insert_message['电话']
    hiredate = insert_message['入职日期']
    sal = 0
    comm = 0

    deptno = mysql.get_fetchone(query_deptno)['deptno']
    # 写入信息
    # message_tuple = (empno,ename,job,mgr,sex,idcard,bank_id)
    # 插入值
    inset_sql = f"""insert into emp values ({empno}, '{ename}', '{job}',{mgr},'{sex}','{bank_id}','{idcard}','{bank_address}','{tel}','{hiredate}',{sal},{comm},{deptno})"""
    # print(inset_sql)
    return mysql.sql_execute(inset_sql)


def delete_emp_message(emp_id: int) -> bool:
    """
    删除员工信息
    :param emp_id:
    :return:bool
    """
    delete_sql = f""" delete from emp where empno ={emp_id} """
    mysql = MysqlUtil()
    return mysql.sql_execute(delete_sql)


def update_emp_message(emp_id: int, update_dict: dict) -> bool:
    """
    修改员工信息
    :param emp_id:
    :param update_dict:
    :return:

    """
    dict_key = {'提交人': 'ename',
                '类型': 'type',
                '部门': 'deptno',
                '岗位': 'job',
                '入职日期': 'hiredate',
                '姓名': 'ename',
                '性别': 'sex',
                '电话': 'tel',
                '身份证': 'idcard',
                '开户行': 'bank_address',
                '卡号': 'bank_id'}
    query_sql_emp = f""" select * from emp where empno = {emp_id} """
    query_sql_dname = f""" select * from dept where dname = '{update_dict['部门']}' """
    # print(query_sql_dname)
    mysql = MysqlUtil()
    # 数据库中员工信息=字典
    emp_old_dict = mysql.get_fetchone(query_sql_emp)
    deptno_dict = mysql.get_fetchone(query_sql_dname)
    update_dict['部门'] = deptno_dict['deptno']

    # 根据key进行转换
    for key_words in update_dict.keys():
        key_name = dict_key[key_words]
        emp_old_dict[key_name] = update_dict[key_words]

    # print(update_dict)

    update_sql = f"""update emp set 
                        deptno = '{emp_old_dict['deptno']}',
                        job = '{emp_old_dict['job']}',
                        hiredate = '{emp_old_dict['hiredate']}',
                        ename = '{emp_old_dict['ename']}',
                        sex = '{emp_old_dict['sex']}',
                        tel = '{emp_old_dict['tel']}',
                        idcard = '{emp_old_dict['idcard']}',
                        bank_address = '{emp_old_dict['bank_address']}',
                        bank_id = '{emp_old_dict['bank_id']}' where empno ={emp_id}
                        """
    return mysql.sql_execute(update_sql)


def query_emp_message(emp_id: int) -> dict:
    """
    查询员工信息
    :param emp_id:
    :return: 员工信息字典
    """

    query_sql = f""" select *  from emp where empno = '{emp_id}'"""

    mysql = MysqlUtil()
    res = mysql.get_fetchone(query_sql)

    return res


def add_customer_message(customer_dict: dict) -> bool:
    """
    {'empno': '9', '提交人': '张强', '类型': '客户信息录入', '姓名': '黄生会', '电话': '18702303793', '身份证': '510225197110086547', '开户行': '中国建设银行南坪支行', '卡号': '6227003762610012416'}
    新增客户信息
    :param customer_dict:
    :return:
    """
    # 写入信息
    message_tuple = (customer_dict['姓名'], customer_dict['prefix'], customer_dict['电话'],
                     customer_dict['身份证'], customer_dict['卡号'], customer_dict['开户行'],
                     customer_dict['empno'])

    insert_sql = """insert into customer (name,prefix,tel,idcard,bank_id,bank_address,empno) values ('%s','%s','%s','%s','%s','%s',%s);""" \
                 % (message_tuple)
    # 创建数据库对象
    mysql = MysqlUtil()
    # 执行插入
    result = mysql.sql_execute(insert_sql)
    # 查询刚刚用户的id
    query_sql = f"""select * from  customer where prefix = '{customer_dict['prefix']}'"""
    result_dict = mysql.get_fetchone(query_sql)
    print(result_dict)
    customer_id = result_dict['id']

    return result, customer_id


def delete_customer_message(customer_id: int) -> bool:
    """
    删除客户信息
    :param customer_id:
    :return:
    """


def update_customer_message(customer_id: int, update_dict: dict) -> bool:
    """
    修改客户信息
    :param customer_id:
    :param update_dict:
    :return:
    """


def query_customer_message_id(customer_id: int) -> dict:
    """
    查询客户信息
    :param customer_id:
    :return: 员工信息字典
    """
    # sql语句
    query_sql = f""" select *  from customer where 'id' = {customer_id}"""
    # 创建对象
    mysql = MysqlUtil()
    # 执行sql
    res = mysql.get_fetchall(query_sql)

    return res


def query_is_customer(message_dict: dict):
    """
    {'提交人': '张先生', '类型': '客户信息录入', '姓名': '黄生会', '电话': '18702303793', '身份证': '510225197110086547', '开户行': '中国建设银行南坪支行', '卡号': '6227003762610012416'}
    查询客户是否存在
    :param message_dict:
    :return:
    """
    # 字典的所有key列表
    keys_list = message_dict.keys()
    query_sql = f""" select * from customer """

    sql_list = []

    if 'id' in keys_list:
        # sql语句
        query_sql = query_sql + f""" where id = '{message_dict['id']}' """

    else:

        if '姓名' in keys_list:
            sql_list.append(f""" name = '{message_dict['姓名']}' """)
        if '电话' in keys_list:
            sql_list.append(f""" tel = '{message_dict['电话']}' """)
        if '身份证' in keys_list:
            sql_list.append(f""" idcard = '{message_dict['身份证']}' """)
        if '开户行' in keys_list:
            sql_list.append(f""" bank_address = '{message_dict['开户行']}' """)
        if '卡号' in keys_list:
            sql_list.append(f""" bank_id = '{message_dict['卡号']}' """)
        append_len = len(sql_list)

        # 拼接SQL
        if append_len == 0:
            return None
        elif append_len == 1:
            query_sql = ' where '.join([query_sql, sql_list[0]])
        else:
            query_sql = ' where '.join([query_sql, sql_list[0]])
            sql_list.pop(0)
            sql_list.insert(0, query_sql)
            query_sql = ' and '.join(sql_list)

    print(query_sql)
    # 创建对象
    mysql = MysqlUtil()
    # 执行sql
    result = mysql.get_fetchall(query_sql)
    print(result)
    # 返回有结果表示该用户以存在,反之
    if len(result) > 0:
        return result[0]
    else:
        return None


def debug_query_is_customer():
    dic = {'提交人': '张先生', '类型': '客户信息录入', '客户姓名': '黄生会', '客户电话': '18702303793',
           '身份证': '510225197110086547',
           '开户行': '中国建设银行南坪支行',
           '卡号': '6227003762610012416'}
    print(query_is_customer(dic))


def query_user_status(customer_id: str, status: bool, order_by: str = "ASC"):
    """# 查询用户使用终止账号

    :param customer_id:
    :param status:
    :param order_by:
    :return:
    {'id': 6754, 'name': '左罗', 'account': 'XLZL01', 'account_status': 1, 'create_time': datetime.datetime(2022, 9, 18, 9, 7, 2), 'use_time': datetime.datetime(2022, 9, 18, 9, 7, 2), 'customer_id': 18, 'tel': '18512380086'}
    """
    sql = f"""
        SELECT
            * 
        FROM
            (SELECT
                a.*,b.tel
                FROM
                account as a
                JOIN
                    customer as b
                ON a.customer_id =b.id) as a
        WHERE
            account_status = {status}
            AND customer_id = "{customer_id}" 
           
        ORDER BY
            id {order_by} 
    """
    mysql = MysqlUtil()
    res = mysql.get_fetchone(sql)
    print(res)
    return res


def debug_sum_account_number():
    for i in range(130, 150):
        print(sum_account_number(i))


def sum_account_number(message_dict: dict) -> dict:
    """
    # 计算账号已注册账号未使用个数
    :param message_dict:
    :return:

    ['张雪',‘1582353003470'，XLZX', 3, 47, 45]
    {'id': 38,
     'name': '张三',
     'prefix': 'XLZS',
     'tel': '13896107831',
     'begin':1,
     'end':10,
     'length':10}
    客户id,客户姓名，电话，账号前缀，未使用号、注册终止号，账号余量
    """
    # print(f'sum_account_number{message_dict}')
    # 未使用开始数
    account = query_user_status(message_dict['id'], 0)
    result_dict = {'id': '',
                   'name': '',
                   'prefix': '',
                   'tel': '',
                   'begin': '',
                   'end': '',
                   'length': ''}
    if account:
        prefix = re.findall(r"\D+", account['account'])[0]
        tel = account['tel']
        begin = int(re.findall(r"\d+\.?\d*", account['account'])[0])
        end = int(re.findall(r"\d+\.?\d*", query_user_status(message_dict['id'], 0, "DESC")['account'])[0])

        res = [message_dict['id'], tel, prefix, begin, end, end - begin + 1]
        result_dict['id'] = message_dict['id']
        result_dict['name'] = message_dict['name']
        result_dict['prefix'] = message_dict['prefix']
        result_dict['tel'] = message_dict['tel']
        result_dict['begin'] = begin
        result_dict['end'] = end
        result_dict['length'] = end - begin + 1

        # print(f"sum_account_number,result{result_dict}")
        return result_dict
    else:
        log_sql.debug(f'请注意：{message_dict}账号剩余量为：0')
        print('请注意：', message_dict, "账号剩余量为：0")
        account = query_user_status(message_dict, 1, "DESC")
        prefix = re.findall(r"\D+", account['account'])[0]
        tel = account['tel']
        begin = int(re.findall(r"\d+\.?\d*", account['account'])[0])
        end = begin
        res = [message_dict, tel, prefix, begin, end, 0]
        return res


def update_account_status(prefix: str, begin: int, length: int, status: bool = True):
    """
    更新账号使用状态
    :param prefix: 账号前缀
    :param begin: 开始数
    :param length: 订单数
    :return:
    """

    for change in range(begin, begin + length):
        if change < 10:
            change = '0' + str(change)
        sql = f"""
                update account set account_status={status}  where  account = '{prefix}{change}'
            """
        mysql = MysqlUtil()
        res = mysql.sql_execute(sql)


def insert_account_one(customer_id: int, account: str, status: bool = False):
    """
    插入单账号信息
    :param name:客户姓名
    :param account:账号
    :param status:插入状态
    :return:
    insert_account_one("张三", "XLZS01", False)
    """
    # 根据name找到对应的客户编号 id
    sql_query = f"""select * from customer where id = {customer_id}"""
    mysql = MysqlUtil()
    result = mysql.get_fetchone(sql_query)
    # print(result)
    name = result['name']
    # 插入账号信息
    sql_insert = f"insert into account(name,account,account_status,customer_id) values ('{name}','{account}',{status},{customer_id})"
    log_sql.debug(
        f"尝试保存在数据库：客户id:{customer_id} 姓名：" + name + " 账号：" + account + " 账号状态" + str(status))
    flag = mysql.sql_execute(sql_insert)
    if flag:
        log_sql.debug(
            f"完成保存在数据库：客户id:{customer_id} 姓名：" + name + " 账号：" + account + " 账号状态" + str(status))
    else:
        log_sql.debug(
            f"保存失败在数据库：客户id:{customer_id} 姓名：" + name + " 账号：" + account + " 账号状态" + str(status))


def insert_account_many(customer_id: int, begin: int, length: int, status: bool = False):
    """
    插入多账号信息
    :param customer_id:客户姓名
    :param begin: 开始数
    :param length: 账号个数
    :param status:插入状态
    :return:

    """
    mysql = MysqlUtil()
    # 根据id找到对应的客户信息
    sql_query = f"""select * from customer where id = '{customer_id}'"""
    result_dict = mysql.get_fetchone(sql_query)
    # print(res_lis)
    name = result_dict['name']
    prefix = result_dict['prefix']
    inset_list = []
    sql_insert = f"insert into account(name,account,account_status,customer_id) values (%s,%s,%s,%s)"
    end = begin + length
    for change in range(begin, end):
        account = prefix + str(change).zfill(2)
        inset_list.append((name, account, status, customer_id))

    flag = mysql.sql_executemany(sql_insert, inset_list)
    if flag:
        log_sql.debug(f"保存成功，客户id:{customer_id} 姓名：{name} 账号：{prefix}{begin}-{end - 1} 账号状态:{status}")
    else:
        log_sql.debug(f"保存失败，客户id:{customer_id} 姓名：{name} 账号：{prefix}{begin}-{end - 1} 账号状态:{status}")


def update_account_customer_id():
    """
    更新账号id与对应客户表相对于
    :param prefix: 账号前缀
    :param begin: 开始数
    :param length: 订单数
    :return:
    """

    sql = f"""
            update account set customer_id= 51  where  name = '向邦容'
        """
    query_sql = """
        select name,account from account where name ='向邦容'
    """
    sql_aa = """
                SELECT
                id,name
                FROM
                customer"""
    mysql = MysqlUtil()
    que_res = mysql.get_fetchall(sql_aa)
    print(que_res)
    for name in que_res:
        change_sql = f"""update account set customer_id= {name['id']}  where  name = '{name['name']}'"""
        mysql.sql_execute(change_sql)
    # res = mysql.get_fetchall(query_sql)
    print(que_res)


def query_customer_message(message_dict: dict) -> tuple:
    """
    根据提供字典信息进行客户信息查询
    :param message_dict: 提供信息字典
    :return: 客户信息字典，查询结果文字提示
    """
    # {'id': 38, 'name': '张三', 'prefix': 'XLZS', 'tel': '13896107831', 'idcard': '50010319910719214X', 'bank_id': '6230 9437 6000 8888 888', 'bank_address': '张三银行', 'remark': '无', 'create_time': datetime.datetime(2022, 9, 18, 12, 28, 32), 'update_time': datetime.datetime(2022, 10, 9, 7, 49, 58), 'empno': 9}
    # 字典的所有key列表
    print(message_dict)
    keys_list = message_dict.keys()
    query_sql = f""" select * from customer """

    sql_list = []

    if 'id' in keys_list:
        # sql语句
        query_sql = query_sql + f""" where id = '{message_dict['id']}' """

    else:

        if '姓名' in keys_list:
            sql_list.append(f""" name = '{message_dict['姓名']}' """)
        if '电话' in keys_list:
            sql_list.append(f""" tel = '{message_dict['电话']}' """)
        if '身份证' in keys_list:
            sql_list.append(f""" idcard = '{message_dict['身份证']}' """)
        if '开户行' in keys_list:
            sql_list.append(f""" bank_address = '{message_dict['开户行']}' """)
        if '卡号' in keys_list:
            sql_list.append(f""" bank_id = '{message_dict['卡号']}' """)
        append_len = len(sql_list)

        # 拼接SQL
        if append_len == 0:
            result_str = f"信息有误，请检查信息后,重新发送"
            log_sql.debug(result_str)
            return None, result_str
        elif append_len == 1:
            query_sql = ' where '.join([query_sql, sql_list[0]])
        else:
            query_sql = ' where '.join([query_sql, sql_list[0]])
            sql_list.pop(0)
            sql_list.insert(0, query_sql)
            query_sql = ' and '.join(sql_list)

    log_sql.debug(query_sql)
    # 创建对象
    mysql = MysqlUtil()
    # 返回结果列表
    query_list = mysql.get_fetchall(query_sql)
    # 查询结果的客户的个数
    query_len = len(query_list)
    if query_len == 0:
        result_str = f"{message_dict['姓名']},客户不存在,请检查信息后,重新发送"
        log_sql.debug(result_str)
        return None, result_str
    elif query_len == 1:
        result_dict = query_list[0]
        result_str = f"""id:{result_dict['id']},客户姓名：{result_dict['name']},正在查询，请稍后！"""
        log_sql.debug(result_str)
        return result_dict, result_str
    else:
        result_str = f"""{message_dict['姓名']}存在重名,请提供更多有效信息进行查询"""
        log_sql.debug(result_str)
        return None, result_str


def query_account_message(customer_id: int):
    query_sql = f"""select * from customer where id = {customer_id}"""


def update_account_customer_id1():
    query_sql = f"""select id,name from customer """
    mysql = MysqlUtil()
    # 返回结果列表
    query_list = mysql.get_fetchall(query_sql)
    # print(query_list)
    for dic in query_list:
        print(dic)
        update_sql = f""" upate account set customer_id """


def update_account_customer_bank():
    query_sql = f""" select * from customer"""
    mysql = MysqlUtil()
    # 返回结果列表
    query_list = mysql.get_fetchall(query_sql)
    for i in query_list:
        # print(i)
        lis = re.findall('\d+', i['bank_address'])
        if lis:
            print(lis)
            change_sql = f"""update customer set  bank_address = '{i['bank_id']}',bank_id = '{i['bank_address']}' where  id= {i['id']} """
            mysql.sql_execute(change_sql)


def update_emp_bank():
    query_sql = f""" select * from emp"""
    mysql = MysqlUtil()
    # 返回结果列表
    query_list = mysql.get_fetchall(query_sql)
    for i in query_list:
        # print(i)
        lis = i['bank_id']
        if lis:
            print(lis)
            change_sql = f"""update emp set  bank_address = '{i['idcard']}',idcard = '{i['bank_id']}' where  empno= {i['empno']} """
            mysql.sql_execute(change_sql)


if __name__ == '__main__':
    # print(query_customer_message("张三"))
    # for i in get_names():
    #     print(sum_account_number(i))
    # print()
    # print(get_need_change_accounts())
    # update_account_customer_id()
    # print(query_customer_message())
    # update_account_customer_id()
    # update_emp_message()
    # message_dict = {'id': 38, 'name': '张三', 'prefix': 'XLZS', 'tel': '13896107831', 'idcard': '50010319910719214X',
    #                 'bank_id': '6230 9437 6000 8888 888', 'bank_address': '张三银行', 'remark': '无',
    #                 'create_time': datetime.datetime(2022, 9, 18, 12, 28, 32),
    #                 'update_time': datetime.datetime(2022, 10, 9, 7, 49, 58), 'empno': 9}
    # print(query_user_status(message_dict['id'], 0))
    # insert_account_many(259, 251, 50, 0)
    dic = {'提交人': '张先生',
           '类型': '员工信息录入',
           '部门': '业务一部',
           '岗位': '数据专员',
           '入职日期': '2022-10-02',
           '姓名': '黄生会1',
           '性别': '男',
           '电话': '18702303793',
           '身份证': '510225197110086547',
           '开户行': '中国建设银行南坪支行',
           '卡号': '6227003762610012416'}
    # add_emp_message(dic)
    # debug_sum_account_number()

    dict_key = {'部门': 'deptno',
                '岗位': 'job',
                '入职日期': 'hiredate',
                '姓名': 'ename',
                '性别': 'sex',
                '电话': 'tel',
                '身份证': 'idcard',
                '开户行': 'bank_address',
                '卡号': 'bank_id'}
    print(dic)
    print('-' * 50)

    update_emp_message(24, dic)
