"""
买入,卖出股票。

由于买入和卖出的操作一样，这里就写在同一个文件里面了

"""
from PIL import Image
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt

from ocrstock.common.screenshot import get_screenshot
from ocrstock.common.location import find_location
from ocrstock.common.cut_pic import cut_blank
from ocrstock.common.userinput import keyboard_input,mouse_click

from ocrstock.config import config
from ocrstock.logs.logger import mylogger

# 定义全局日志，日志名为 buy_sell
log=mylogger(name='buy_sell')


def read_im(file, threshold):
    """读取子图，并转成二值图"""
    im=np.array(Image.open(file).convert('L'),dtype=int)
    im[im<=threshold]=0
    im[im>threshold]=1
    return im

def to_bin_img(pic, threshold):
    """将全图进行二值化"""
    pic[pic<=threshold]=0
    pic[pic>threshold]=1
    return pic

def read_im_info(name):
    """读取子图，已经相关搜索参数"""
    info = config.pic_info[name]
    bin = info['bin']
    xrange, yrange = info['xrange'], info['yrange']
    file = os.path.join(config.gvariable.picpath, name + '.png')
    im = np.array(Image.open(file).convert('L'), dtype=int)
    im[im <= bin] = 0
    im[im > bin] = 1
    return im, bin, xrange, yrange


def get_focus():
    """获取界面焦点"""
    im, bin, xrange, yrange = read_im_info('界面_标题')
    # 截屏
    pic=get_screenshot()
    pic=to_bin_img(pic, bin)
    # 查找位置
    x, y=find_location(pic,im,xrange,yrange,'center')
    mouse_click(x,y)
    log.info('点击，获取界面焦点 %d %d'%(x,y))

def buy(symbol, price, amount):
    """买入股票"""
    # 获取焦点
    get_focus()
    # 功能键F1，转到买入选项卡
    keyboard_input(function_key='F1')

    log.info('获取程序焦点，调出股票买入页面')

    # 截图
    pic = get_screenshot()
    # 获取 买入股票 标志坐标
    im, bin, xrange, yrange = read_im_info('买入_买入页')
    im=cut_blank(im)
    pic2=to_bin_img(pic.copy(),threshold=bin)
    x,y=find_location(pic2,im,xrange,yrange,'leftup')

    log.info('买入股票 坐标 %d %d '%(x,y))

    # 计算其他几个标志的查找范围
    high=pic.shape[0]*0.3
    width=pic.shape[1]*0.3
    x1=(x-10)/pic.shape[0] if x-10>=0 else 0
    x2=(x+high)/pic.shape[0] if x+high<=pic.shape[0] else 1
    y1=(y-10)/pic.shape[1] if y-10>0 else 0
    y2=(y+width)/pic.shape[1] if y+width<=pic.shape[1] else 1

    # 获取 证券代码，买入价格，买入数量，买入
    # 证券代码
    im, bin, xrange, yrange = read_im_info('买入_证券代码')
    im=cut_blank(im)
    pic2=to_bin_img(pic.copy(), bin)
    x_zqdm,y_zqdm = find_location(pic2,im,[x1,x2],[y1,y2],'center')
    log.info('证券代码 坐标 %d %d ' % (x_zqdm, y_zqdm))

    # 买入价格
    im, bin, xrange, yrange = read_im_info('买入_买入价格')
    im=cut_blank(im)
    pic2=to_bin_img(pic.copy(), bin)
    x_mrjg,y_mrjg = find_location(pic2,im,[x1,x2],[y1,y2],'center')
    log.info('买入价格 坐标 %d %d ' % (x_mrjg, y_mrjg))

    # 买入数量
    im, bin, xrange, yrange = read_im_info('买入_买入数量')
    im=cut_blank(im)
    pic2=to_bin_img(pic.copy(), bin)
    x_mrsl,y_mrsl = find_location(pic2,im,[x1,x2],[y1,y2],'center')
    log.info('买入数量 坐标 %d %d ' % (x_mrsl, y_mrsl))

    # 买入确认
    im, bin, xrange, yrange = read_im_info('买入_买入确认')
    im=cut_blank(im)
    pic2=to_bin_img(pic.copy(), bin)
    x_mrqr,y_mrqr = find_location(pic2,im,[x1,x2],[y1,y2],'center')
    log.info('买入确认 坐标 %d %d ' % (x_mrqr, y_mrqr))

    # 重填
    im, bin, xrange, yrange = read_im_info('买入_重填')
    im = cut_blank(im)
    pic2 = to_bin_img(pic.copy(), bin)
    x_ct, y_ct = find_location(pic2, im, [x1, x2], [y1, y2], 'center')
    log.info('买入重填 坐标 %d %d ' % (x_ct, y_ct))

    # 下面买入股票
    # 重置所有输入
    mouse_click(x_ct, y_ct)
    # 输入代码
    mouse_click(x_zqdm,y_zqdm)
    keyboard_input(symbol)
    # 输入价格
    mouse_click(x_mrjg,y_mrjg)
    keyboard_input(str(price))
    # 输入数量
    mouse_click(x_mrsl,y_mrsl)
    keyboard_input(str(amount))
    # 点击确认
    mouse_click(x_mrqr,y_mrqr)

    log.info('买入 symbol=%s price=%f amount=%d'%(symbol,price,amount))
    # 后面还有弹出确认框的确认
    log.info('后面还有弹出确认框的确认, 未处理')



def test_buy():
    # 测试买入
    symbol='601398'
    price=3.45
    amount=100
    buy(symbol,price,amount)


def sell(symbol, price, amount):
    """卖出股票"""
    # 获取焦点
    get_focus()
    # 功能键F2，转到买入选项卡
    keyboard_input(function_key='F2')

    log.info('获取程序焦点，调出股票卖出页面')

    # 截图
    pic = get_screenshot()
    # 获取 买入股票 标志坐标
    im, bin, xrange, yrange = read_im_info('卖出_卖出页')
    im = cut_blank(im)
    pic2 = to_bin_img(pic.copy(), threshold=bin)
    x, y = find_location(pic2, im, xrange, yrange, 'leftup')

    log.info('卖出股票 坐标 %d %d ' % (x, y))

    # 计算其他几个标志的查找范围
    high = pic.shape[0] * 0.3
    width = pic.shape[1] * 0.3
    x1 = (x - 10) / pic.shape[0] if x - 10 >= 0 else 0
    x2 = (x + high) / pic.shape[0] if x + high <= pic.shape[0] else 1
    y1 = (y - 10) / pic.shape[1] if y - 10 > 0 else 0
    y2 = (y + width) / pic.shape[1] if y + width <= pic.shape[1] else 1

    # 获取 证券代码，买入价格，买入数量，买入
    # 证券代码
    im, bin, xrange, yrange = read_im_info('卖出_证券代码')
    im = cut_blank(im)
    pic2 = to_bin_img(pic.copy(), bin)
    x_zqdm, y_zqdm = find_location(pic2, im, [x1, x2], [y1, y2], 'center')
    log.info('证券代码 坐标 %d %d ' % (x_zqdm, y_zqdm))

    # 买入价格
    im, bin, xrange, yrange = read_im_info('卖出_卖出价格')
    im = cut_blank(im)
    pic2 = to_bin_img(pic.copy(), bin)
    x_mcjg, y_mcjg = find_location(pic2, im, [x1, x2], [y1, y2], 'center')
    log.info('卖出价格 坐标 %d %d ' % (x_mcjg, y_mcjg))

    # 买入数量
    im, bin, xrange, yrange = read_im_info('卖出_卖出数量')
    # im = cut_blank(im)  # 数量和价格两个字段极容易无法识别区分，因此这里将cut_blank去掉
    pic2 = to_bin_img(pic.copy(), bin)
    x_mcsl, y_mcsl = find_location(pic2, im, [x1, x2], [y1, y2], 'center')
    log.info('卖出数量 坐标 %d %d ' % (x_mcsl, y_mcsl))

    # 买入确认
    im, bin, xrange, yrange = read_im_info('卖出_卖出确认')
    im = cut_blank(im)
    pic2 = to_bin_img(pic.copy(), bin)
    x_mcqr, y_mcqr = find_location(pic2, im, [x1, x2], [y1, y2], 'center')
    log.info('卖出确认 坐标 %d %d ' % (x_mcqr, y_mcqr))

    # 重填
    im, bin, xrange, yrange = read_im_info('卖出_重填')
    im = cut_blank(im)
    pic2 = to_bin_img(pic.copy(), bin)
    x_ct, y_ct = find_location(pic2, im, [x1, x2], [y1, y2], 'center')
    log.info('卖出重填 坐标 %d %d ' % (x_ct, y_ct))

    # 下面买入股票
    # 重置所有输入
    mouse_click(x_ct, y_ct)
    # 输入代码
    mouse_click(x_zqdm, y_zqdm)
    keyboard_input(symbol)
    # 输入价格
    mouse_click(x_mcjg, y_mcjg)
    keyboard_input(str(price))
    # 输入数量
    mouse_click(x_mcsl, y_mcsl)
    keyboard_input(str(amount))
    # 点击确认
    mouse_click(x_mcqr, y_mcqr)

    log.info('卖出 symbol=%s price=%f amount=%d' % (symbol, price, amount))
    # 后面还有弹出确认框的确认
    log.info('后面还有弹出确认框的确认, 未处理')


def test_sell():
    # 卖出测试
    symbol='601398'
    price=3.45
    amount=100
    sell(symbol,price,amount)
