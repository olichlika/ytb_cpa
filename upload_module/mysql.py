# -*- coding:utf-8 -*-
# author:Kyseng
# file: mysql.py
# time: 2018/4/28 上午11:37
# functhion:
import datetime
import pymysql

MYSQL_HOST = '45.77.30.101'
MYSQL_PORT = 3306
MYSQL_DBNAME = 'cpa_db'
MYSQL_USER = 'root'
MYSQL_PASSWD = 'qwerchen07@@'

# 用于数据库存储
class DBPipeline(object):
    def __init__(self):
        # 连接数据库
        self.connect = pymysql.connect(
            host = MYSQL_HOST,
            port = MYSQL_PORT,
            db = MYSQL_DBNAME,
            user = MYSQL_USER,
            passwd = MYSQL_PASSWD,
            charset='utf8',
            use_unicode=True)

        # 通过cursor执行增删查改
        self.cursor = self.connect.cursor();

    # def insert_new_row(self, skinName, url):
    #     try:
    #         self.cursor.execute(
    #             """insert into fortnite_skin_table(skinName, url) value (%s, %s)""",
    #             (skinName, url))
    #         self.connect.commit()
    #         return 'ok'
    #
    #     except Exception as error:
    #         # 出现错误时打印错误日志
    #         print error
    #         return 'error'
    #
    # def check_exist(self, skinName):
    #     try:
    #         self.cursor.execute(
    #             """select * from fortnite_skin_table where skinName = %s""", skinName
    #         )
    #         repetition = self.cursor.fetchone()
    #         if repetition:
    #             # print "data exist"
    #             return "exist"
    #         else:
    #             # print "data not exist"
    #             return "noexist"
    #     except Exception as error:
    #         # 出现错误时打印错误日志
    #         return 'error'

    def getSkin(self, oauth):
        try:
            self.cursor.execute(
                """SELECT * FROM `fortnite_skin_table` WHERE skinName NOT IN (SELECT skinName FROM `fortnite_skin_ytb_table` WHERE oauth = %s)""",
                oauth
            )
            # self.connect.commit()
            date = self.cursor.fetchall()

            if date:
                return date
            else:
                return None

        except Exception as error:
            print error

    def insert_new_row(self, oauth, skinName):
        t = datetime.datetime.now()
        t = str(t.strftime('%Y-%m-%d %H:%M:%S'))

        try:
            self.cursor.execute(
                """insert into fortnite_skin_ytb_table(oauth, skinName, upload_time) value (%s, %s, %s)""",
                (oauth, skinName, t))
            self.connect.commit()
            return 'ok'

        except Exception as error:
            # 出现错误时打印错误日志
            print error
            return 'error'