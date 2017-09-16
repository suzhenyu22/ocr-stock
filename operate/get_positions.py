# -*- coding: utf-8 -*-
"""
获取持仓信息。

1.找到证券代码，然后找到左边和右边的x1,x2, x1+1, x2-1
2.往下走，找到分割线y1, y1+2 得到表格开始位置
3.往下走，找到分割线y2, y2-1 得到表格结束位置
4.如果y2-y1>30,说明没有持仓

"""
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image

from ocrstock.common.screenshot import get_screenshot  # 截图
from ocrstock.common.location import find_location     # 获取子图位置
from ocrstock.common.cut_pic import cut_blank   # 切除图片四周空白
from ocrstock.common.userinput import mouse_click, keyboard_input

from ocrstock.ml.recognize_num.recognize_nums import rec_nums  # 识别数字串

from ocrstock.config import config    # 全局配置信息
from ocrstock.logs.logger import mylogger

# 配置全局日志，使用默认文件名，指定日志名称为 get_positions
log=mylogger(name='get_positions')


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


def get_cols_pic_info(pic, im, xrange, yrange, maxdown=None):
    """对一列数字的图像解析，划分截取"""
    # 找到表格的最下位置，方法查找过界
    xdown=pic.shape[0]*0.9 if not maxdown else maxdown

    # 找到子图在主图的左下角和右下角坐标
    x1, y1 = find_location(pic, im, xrange, yrange, 'leftdown')
    y2 = y1+im.shape[1]
    xmax,ymax=pic.shape
    # 往左边找到边界
    while True:
        y1=y1-1
        if pic[x1,y1]==0 and y1<ymax:
            y1=y1+1
            break
    # 往右边找到边界
    while True:
        y2=y2+1
        if pic[x1,y2]==0 and y2<ymax:
            y2=y2-1
            break
    # 往下找到边界位置，并越过边界
    while True:
        x1=x1+1
        if pic[x1,y1]==0 and x1<xmax:
            x1=x1+1
            break
    # 经过前面的步骤，找打了有数字表格的位置
    xstart,ystart,yend=x1,y1,y2
    # 下面找到xend就可以切割一个区域了
    notend=True
    nums=[]
    while notend:
        # 往下找到分割线
        x,xend=xstart,xstart
        while True:
            x=x+1
            if pic[x,ystart]==0 and x < xdown:  # 找到边界并且没有越界
                xend=x-1
                nums.append(pic[xstart: xend, y1:y2])
                # 接着越过边界，找到下一个查找开始坐标
                while True:
                    x=x+1
                    if pic[x,y1]==1 and x<xdown:
                        xstart=x
                        break
                    elif x>=xdown:
                        break
                break  # 既然找到了就接着开始下一行数字查找
            # 如果找了很久没有找到，说明已经到头了
            if x-xstart>30 or x>=xdown:
                notend=False
                break
    # 接下来就是解析nums数字
    nums=[rec_nums(num) for num in nums]
    # 最后返回该列数据
    return nums


def get_position_table():
    """获取指定列的数据"""
    # 获取焦点
    get_focus()
    # 功能键F1，转到买入选项卡
    keyboard_input(function_key='F4')

    log.info('获取程序焦点，调出股票持仓查询页面')

    # 第一步是先获取屏幕截图
    pic=get_screenshot()

    log.info('获取屏幕截图')

    # 获取表格下边框，防止搜索过界
    info = config.pic_info['持仓_汇总']
    bin = info['bin']
    xrange = info['xrange']
    yrange = info['yrange']
    # 获取子图
    file = os.path.join(config.gvariable.work_path, 'pic', '持仓_汇总.png')
    print(file)
    im = read_im(file, threshold=bin)  # 因为已经是二值图，这里的阈值就没必要了
    im = cut_blank(im)
    # 获取主图的二值图
    pic2 = to_bin_img(pic.copy(), threshold=bin)
    # 接下来就是找到边界了
    maxdown,y=find_location(pic2,im,xrange,yrange,'leftup')

    log.info('获取最大搜索下边界 %d'%maxdown)

    # 开始循环获取数字串
    cols = ['持仓_证券代码', '持仓_股票余额', '持仓_可用余额', '持仓_冻结数量',
            '持仓_成本价', '持仓_市价', '持仓_市值']
    # col=cols[0]
    tables=[]
    for col in cols:
        # 获取准备好的子图信息
        info=config.pic_info[col]
        bin=info['bin']
        xrange=info['xrange']
        yrange=info['yrange']
        # 获取子图
        file=os.path.join(config.gvariable.work_path,'pic',col+'.png')
        im=read_im(file,threshold=bin)  # 因为已经是二值图，这里的阈值就没必要了
        im=cut_blank(im)
        # 获取主图的二值图
        pic2=to_bin_img(pic.copy(),threshold=bin)
        # 接下来就是获取列的信息了
        col_info=get_cols_pic_info(pic2,im,xrange,yrange,maxdown)
        tables.append(col_info)

        log.info('完成 %s 数据解析'%col)

    # 转成dataframe
    position=pd.DataFrame(tables,index=cols).T

    log.info('完成表格所有列解析\n'+str(position))

    return position



def test():
    #
    # 读入全图
    file = r"E:\python_code\ocrstock\pic\全图.png"
    # file=r"F:\wo\python_code\ocrstock\pic\全图.png"
    pic = read_im(file, threshold=200)
    plt.imshow(pic)

    # 找到证券代码位置
    file = r"E:\python_code\ocrstock\pic\持仓_证券代码.png"
    # file=r"F:\wo\python_code\ocrstock\pic\证券代码.png"
    im = read_im(file, threshold=100)
    im = cut_blank(im, 0, 0)
    plt.imshow(im)

    get_position_table()

