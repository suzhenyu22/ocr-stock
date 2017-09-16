"""
将操作窗口最大化.

包括：
1. 点击任务栏图标获取焦点
2. 判断是否最小化
3. 是，则点击任务栏图标最大化
4. 判断是否锁屏
5. 是，则解锁交易界面
6. 判断是否最大化
7. 否，则最大化，是，则不操作
"""
import time
from PIL import Image
import numpy as np
import os
import matplotlib.pyplot as plt

from ocrstock.common.userinput import mouse_click,keyboard_input, keyboard_enter  # 模拟鼠标键盘
from ocrstock.common.location import find_location
from ocrstock.common.cut_pic import cut_blank
from ocrstock.common.screenshot import get_screenshot

from ocrstock.config import config
from ocrstock.logs.logger import mylogger

# 定义全局日志，日志名为 maximization
log=mylogger(name='maximization')


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



def get_app_focus():
    """点击一下软件的任务栏图标，获取焦点"""
    # 获取图标信息
    name='界面_任务栏图标'
    im, bin, xrange, yrange=read_im_info(name)
    # 截屏
    pic=get_screenshot()
    pic=to_bin_img(pic, bin)
    # 查找位置
    x_ico, y_ico=find_location(pic,im,xrange,yrange,'center')

    log.info('找到任务栏图标位置 %d %d'%(x_ico, y_ico))

    # 接下来是鼠标点击
    # 由于无法实现鼠标点击任务栏图标事件，暂时空着
    #
    return x_ico,y_ico

def max_apps_windows():
    """判断当前是否最小化，如果是，则点击任务栏图标，实现最大化"""

    # 找到最大化窗口图标位置
    im, bin, xrange, yrange = read_im_info('界面_已最大化窗口')
    # 截图，判断匹配位置
    pic = get_screenshot()
    pic2 = to_bin_img(pic.copy(), bin)
    x, y = find_location(pic2, im, xrange, yrange, 'center')
    # 判断是否已经最大化
    if x>0 or y>0:
        log.info('窗口已经最大化，无需点击')
        return 0
    # 没有最大化，找到点击窗口图标
    log.info('窗口未最大化，需要最大化窗口')
    im, bin, xrange, yrange = read_im_info('界面_需最大化窗口')
    im=cut_blank(im)
    pic2 = to_bin_img(pic.copy(), bin)
    x, y = find_location(pic2, im, xrange, yrange, 'center')

    if x==-1 or y==-1:
        log.info('没有找到最大化窗口图标，请检查是否最小化或者锁频了')
        return -1
    else:
        mouse_click(x, y)
        log.info('点击窗口最大化 %d %d ，解锁交易界面' % (x, y))


def unlock(passwd='123456'):
    """判断是否需要解锁界面"""
    # 找到锁屏标志
    im, bin, xrange, yrange = read_im_info('界面_解锁密码')
    # 截图，判断匹配位置
    pic = get_screenshot()
    pic2 = to_bin_img(pic.copy(), bin)
    x, y = find_location(pic2, im, xrange, yrange, 'center')
    # 判断是否锁屏
    if x==-1 or y==-1:
        log.info('交易界面没有锁定，无需解锁')
    else:
        log.info('交易界面锁定，需要解锁')
        mouse_click(x,y)
        keyboard_input(passwd)
        log.info('移动到 %d %d ,输入解锁密码'%(x,y))

        # 找到确认按钮
        im, bin, xrange, yrange = read_im_info('界面_解锁确认')
        im=cut_blank(im)
        x1=(x-100)/pic.shape[0] if x-100>=0 else 0
        x2=(x+100)/pic.shape[0] if x+100<=pic.shape[0] else 1
        y1=(y-200)/pic.shape[1] if y-200>=0 else 0
        y2=(y+200)/pic.shape[1] if y+200<=pic.shape[1] else 1

        xrange, yrange = [x1,x2], [y1,y2]
        pic2 = to_bin_img(pic.copy(), bin)
        xc, yc = find_location(pic2, im, xrange, yrange, 'center')
        mouse_click(xc,yc)
        log.info('点击确认按钮 %d %d ，解锁交易界面'%(xc,yc))
    return




