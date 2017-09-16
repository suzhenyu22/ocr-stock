"""
获取子图的位置
"""

import numpy as np
from numba import jit


def get_sub_location(pic, sub, xrange, yrange):
    """获取子图在主图的的起点坐标"""
    x, y = pic.shape
    sx, sy = sub.shape
    cnt = sx * sy
    # 计算搜索范围
    xstart,xend=int(x*xrange[0]), int(x*xrange[1])
    ystart,yend=int(y*yrange[0]), int(y*yrange[1])
    # 防止index超出最大检索范围
    xend=xend if xend<x else x-1
    yend=yend if yend<y else y-1
    # 开始搜索
    for i in range(xstart,xend):
        for j in range(ystart,yend):
            if (i + sx) > x or (j + sy) > y:
                continue
            elif np.sum(np.abs((pic[i:i + sx, j:j + sy]-sub)))<cnt*0.05 :
                return i,j
    return -1, -1

def find_location(pic, sub, xrange=[0,1], yrange=[0,1], which='center'):
    """
    计算子图的位置，然后获取鼠标应该点击的位置。点击位置就是子图的中心点。
    :param pic:
    :param sub:
    :param which: 返回左上角还是中间还是右下角位置坐标
    :return:
    """
    # 起始位置，如果没有找到就是 -1，-1

    x,y=get_sub_location(pic, sub, xrange, yrange)
    sx, sy = sub.shape
    # 下面判断是要找哪个位置
    if x==-1 or y==-1:
        return x,y
    if which=='leftup':
        return x,y
    if which=='center':
        cx, cy = int(x + sx / 2), int(y + sy / 2)
        return cx,cy
    if which=='leftdown':
        cx,cy=x+sx, y   # 注意不是坐标，是行数和列数
        return cx, cy
    if which=='rightup':
        cx,cy=x,y+sy
        return cx,cy
    if which=='rightdown':
        cx,cy=x+sx,y+sy
        return cx, cy