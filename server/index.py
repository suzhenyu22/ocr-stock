# -*- coding: utf-8 -*-
"""
使用bottle作为网页服务器，接受不同量化平台回传的数据

方法1，使用路由方式
方法2，使用get方法
方法3，使用post方法

其实1,2是一个get，只是方式不一样而已
这里决定使用第2种，更加普遍，而且url将参数原样显示。
但是要额外写拼接参数方法

"""
import json
from bottle import route, run, request

from ocrstock.logs.logger import mylogger
from ocrstock.server.db import mydb


# 定义全局日志
log=mylogger('webserver.log', 'webserver')
# 定义全局数据库连接
db=mydb('localhost',5432,'postgres','123456')


def data_to_url(url, data):
    """将dict字典参数添加到url中，使用get方法请求"""
    data=['%s=%s'%(str(k),str(v)) for k,v in data.items()]
    data='&'.join(data)
    new_url=url+'?'+data
    return new_url

def senddata():
    """发送数据的例子"""
    import requests
    url = 'http://localhost:8080/senddata'
    data = {"score": 232, "name": "sdf", "id": 123}
    url = data_to_url(url, data)
    r = requests.get(url)
    print(r.content.decode())



##########################################################
# 下面定义真正的接受数据的函数

@route('/senddata')
def getdata():
    """处理请求数据"""
    # 获取参数，转成字典
    data=dict(request.params.items())
    # 打印发送过来的网址
    log.info(request.url)
    # 保存到数据库
    db.insert(data)
    log.info('请求数据保存到数据库')
    # 打印请求数据
    log.info(data)
    return 'i have received the data you send !'
##########################################################

run(host='localhost', port=6789, debug=True)
##########################################################
