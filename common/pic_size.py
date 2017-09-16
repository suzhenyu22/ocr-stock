"""
与图片缩放有关的
"""
from numpy import array
from PIL import Image



def resize_pic(im,x=10,y=15):
    """
    resize图片大小。
    :param im:
    :param x: 缩放后水平长度
    :param y: 缩放后垂直高度
    :return:
    """
    # 将图片缩放成指定的大小，方便后面统一模型训练和预测
    # 先转成image格式
    if not isinstance(im, Image.Image):
        im=Image.fromarray(im)
    # 缩放，转回array
    im=array(im.resize((x,y), Image.ANTIALIAS))
    return im