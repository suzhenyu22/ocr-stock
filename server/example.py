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

from bottle import route, run, request
import requests

from ocrstock.logs.logger import mylogger

# 定义全局日志
log=mylogger('webserver.log', 'webserver')


def data_to_url(url, data):
    """将dict字典参数添加到url中，使用get方法请求"""
    data=['%s=%s'%(str(k),str(v)) for k,v in data.items()]
    data='&'.join(data)
    new_url=url+'?'+data
    return new_url


# 方法1，使用路由的方式
# @route('/senddata/<data>')
# def getdata(data=''):
#     print('you get : ', data)
#     return 'i have received the data you send !'
#
# def test():
#     import requests
#     url='http://localhost:8080/senddata/{"score": 9.8, "name": "me", "id": 1}'
#     r=requests.get(url)
#     if r.status_code==200:
#         r.content

# 方法2，使用get方法
# 但是需要知道字典的键名是什么
# @route('/senddata')
# def getdata():
#     data=request.params  # 获取字典参数
#     for k,v in data.items():
#         print(k,v)
#     return 'i have received the data you send !'
#
# def test():
#     import requests
#     url='http://localhost:8080/senddata?data=12312&id=asdf'
#     r=requests.get(url)
#     if r.status_code==200:
#         r.content

# post 请求实例
# @route('/hello',method='POST')
# def test_post():
#     print(request.json)
#     return 'Hello, how are you?'
#
# def test():
#     data={'id':123,
#       'name':'sdf',
#       'score':232}
#     url='http://localhost:8080/hello'
#     r=requests.post(url,json=data)



# @route('/')
# @route('/hello/<name>',method='POST')
# def test_post(name='szy'):
#     print('name=',name)
#     print(request.json)
#     return template('Hello {{name}}, how are you?', name=name)


# @route('/hello',method='POST')
# def test_post():
#     print(request.POST['name'])
#     name=request.forms.get('name')
#     print(name)
#     return template('Hello {{name}}, how are you?', name=name)


#############################################################
# run(host='localhost', port=8080, debug=True)

# def test():
#     #
#     import requests
#     url='http://localhost:8080/senddata'
#     data={"score": 232, "name": "sdf", "id": 123}
#     url=data_to_url(url,data)
#     r=requests.get(url)
#     r.status_code
#     r.content
#############################################################