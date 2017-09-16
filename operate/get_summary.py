"""
获取持仓汇总
也就是持仓页的总资产，可用资金等信息
"""
import pandas as pd
import numpy as np
import os
from PIL import Image
import matplotlib.pyplot as plt


from ocrstock.common.screenshot import get_screenshot
from ocrstock.common.cut_pic import cut_blank
from ocrstock.common.location import find_location
from ocrstock.common.userinput import mouse_click,keyboard_input
from ocrstock.ml.recognize_num.recognize_nums import rec_nums


from ocrstock.config import config
from ocrstock.logs.logger import mylogger

# 配置全局日志，使用默认文件名，指定日志名称为 get_summary
log=mylogger(name='get_summary')



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

def get_coordinate(pic,im_name):
    """获取指定子图的坐标"""
    # 读取子图，及其config数据
    file=os.path.join(config.gvariable.picpath,im_name+'.png')
    info=config.pic_info[im_name]
    bin = info['bin']
    xrange = info['xrange']
    yrange = info['yrange']
    # 读取子图，转成二值图
    im=read_im(file, info['bin'])
    im=cut_blank(im)
    # 主图也转成二值图
    pic2=to_bin_img(pic,threshold=bin)
    # 找到四个角坐标
    x1,y1=find_location(pic2,im,xrange,yrange,'leftup')
    x2,y2=x1+im.shape[0], y1+im.shape[1]
    return x1,x2,y1,y2

def get_mony_summary():
    """获取资金汇总"""
    # 获取焦点
    get_focus()
    # 功能键F4，转到买入选项卡
    keyboard_input(function_key='F4')

    log.info('获取程序焦点，调出股票持仓查询页面')

    # 第一步是先获取屏幕截图
    pic = get_screenshot()
    # plt.imshow(pic)
    log.info('获取屏幕截图')

    # 获取下面几个子图的坐标
    # 注意，尽量不要使用循环，而是一个个写，防止位置顺序乱了
    # 资金余额
    x1_zjye,x2_zjye, y1_zjye,y2_zjye = get_coordinate(pic.copy(), '资金汇总_资金余额')
    # 可取金额 ，注意 ‘可用金额’ 和 ‘可取金额’ 还是不一样的
    x1_kqje, x2_kqje, y1_kqje, y2_kqje = get_coordinate(pic.copy(), '资金汇总_可取金额')
    # 冻结金额
    x1_djje, x2_djje, y1_djje, y2_djje = get_coordinate(pic.copy(), '资金汇总_冻结金额')
    # 股票市值
    x1_gpsz, x2_gpsz, y1_gpsz, y2_gpsz = get_coordinate(pic.copy(), '资金汇总_股票市值')
    # 可用金额
    x1_kyje, x2_kyje, y1_kyje, y2_kyje = get_coordinate(pic.copy(), '资金汇总_可用金额')
    # 总资产
    x1_zzc, x2_zzc, y1_zzc, y2_zzc = get_coordinate(pic.copy(), '资金汇总_总资产')

    log.info('获取资金汇总的6个字段的上下左右坐标')

    # 下面计算数字所在表格的高度和宽度
    xhigh=x2_zjye-x1_zjye+2  # 上下增加1行空白
    ywidth=y1_kqje-y2_zjye-4  # 所以说顺序很重要

    # 下面分别取对应的区域数字
    # 资金余额
    x1,x2,y1,y2=x1_zjye-1, x2_zjye+2, y2_zjye+2, y2_zjye+2+ywidth
    bin=config.pic_info['资金汇总_资金余额']['bin']
    zjye=rec_nums(to_bin_img(pic[x1:x2, y1:y2].copy(),bin))
    # 可取金额
    x1,x2,y1,y2 = x1_kqje-1, x2_kqje+2, y2_kqje+2, y2_kqje+2+ywidth
    bin = config.pic_info['资金汇总_可取金额']['bin']
    kqje = rec_nums(to_bin_img(pic[x1:x2, y1:y2].copy(),bin))
    # 冻结金额
    x1,x2,y1,y2 = x1_djje-1, x2_djje+2, y2_djje+2, y2_djje+2+ywidth
    bin = config.pic_info['资金汇总_冻结金额']['bin']
    djje = rec_nums(to_bin_img(pic[x1:x2, y1:y2].copy(),bin))
    # 股票市值
    x1,x2,y1,y2 = x1_gpsz-1, x2_gpsz+2, y2_gpsz+2, y2_gpsz+2+ywidth
    bin = config.pic_info['资金汇总_股票市值']['bin']
    gpsz = rec_nums(to_bin_img(pic[x1:x2, y1:y2].copy(),bin))
    # 可用金额
    x1,x2,y1,y2=x1_kyje-1, x2_kyje+2, y2_kyje+2, y2_kyje+2+ywidth
    bin = config.pic_info['资金汇总_可用金额']['bin']
    kyje = rec_nums(to_bin_img(pic[x1:x2, y1:y2].copy(),bin))
    # 总资产
    x1,x2,y1,y2=x1_zzc-1, x2_zzc+2, y2_zzc+2, y2_zzc+2+ywidth
    bin = config.pic_info['资金汇总_总资产']['bin']
    zzc=rec_nums(to_bin_img(pic[x1:x2, y1:y2].copy(),bin))

    # 将数据组合成dataframe
    data=pd.DataFrame([zjye,kqje,djje,gpsz,kyje,zzc],
                      index=['资金余额','可取金额','冻结金额','股票市值','可用金额','总资产']).T
    log.info('资产状况\n %s'%str(data.T))
    return data


def test():
    # 读取全图, 或者屏幕截图
    file=r"E:\python_code\ocrstock\pic\全图.png"
    pic=np.array(Image.open(file).convert('L'),dtype=int)
    # 解析总资产数据
    get_mony_summary()



