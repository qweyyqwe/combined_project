# -*- coding: utf-8 -*-
# @Time    : 2021/11/22 
# @File    : db.py
# @Software: PyCharm


"""
import pymysql
import threading

lock = threading.Lock()


class DB:
    def __init__(self):
        self.conn = pymysql.connect(host='localhost', port=3306, user='root', password='9', db='social',
                                    charset='utf8', cursorclass=pymysql.cursors.DictCursor)
        self.cursor = self.conn.cursor()

    # def reConnect(self):
    #     try:
    #         self.conn.ping()
    #     except:
    #         self.conn()

    # 更新添加
    def update(self, sql):
        self.cursor.execute(sql)
        self.conn.commit()

    # 获取一条
    def find_one(self, sql):
        self.cursor.execute(sql)
        res = self.cursor.fetchone()
        return res

    # 获取多条
    def find_all(self, sql):
        lock.acquire()
        self.cursor.execute(sql)
        res = self.cursor.fetchall()
        lock.release()
        return res

    # 提交
    def common(self):
        self.conn.commit()

    # 回滚
    def rollback(self):
        self.conn.rollback()

    # 关闭
    def close(self):
        self.cursor.close()
        self.conn.close()


db1 = DB()
"""

import pymysql
import threading

lock = threading.Lock()


class DB:
    def __init__(self) -> None:
        # cursorclass=pymysql.cursors.DictCursor 以字典形式返回数据
        self.conn = pymysql.connect(host='127.0.0.1', port=6379, user='root', db='2',
                                    cursorclass=pymysql.cursors.DictCursor, charset='utf8')
        self.cousor = self.conn.cursor()

    # 添加，修改，删除
    def update(self, sql):
        self.cousor.execute(sql)
        # self.conn.commit()
        # # 返回当前修改数据的id
        # return self.cousor.lastrowid

    # 提交
    def commit(self):
        self.conn.commit()
        return self.cousor.lastrowid

    # 回滚
    def rollbock(self):
        self.conn.rollback()

    # 查询单个
    def find_one(self, sql):
        lock.acquire()
        self.cousor.execute(sql)
        res = self.cousor.fetchone()
        lock.release()
        return res

    # 查询所有
    def find_all(self, sql):
        lock.acquire()
        self.cousor.execute(sql)
        res = self.cousor.fetchall()
        lock.release()
        return res

    # 关闭
    def close(self):
        self.cousor.close()
        self.conn.close()


db1 = DB()
