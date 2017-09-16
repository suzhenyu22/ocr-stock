# -*- coding: utf-8 -*-
"""
将回传的数据保存到数据库
"""
import json
import psycopg2
from DBUtils.PooledDB import PooledDB

class mydb():
    """pg数据库连接"""
    __pool=None
    def __init__(self,host,port,user,password):
        self.params=[host,port,user,password]
        self.conn=self.__get_conn()

    def __get_conn(self):
        """从数据库连接池获取一个连接"""
        if mydb.__pool is None:
            host, port, user, password=self.params
            __pool = PooledDB(creator=psycopg2, mincached=1, maxcached=100,
                              host=host, port=port, user=user, password=password, database='postgres')
        return __pool.connection()

    def insert(self,data):
        """将量化平台传回来的data字典保存起来"""
        # 判断是否连接是否断开
        # 保存数据
        string=json.dumps(data)
        sql=""" insert into stock_signal (signal) values ('%s') """%(string)
        cur=self.conn.cursor()
        cur.execute(sql)
        self.conn.commit()
        cur.close()
