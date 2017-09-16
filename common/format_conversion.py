"""
格式转换
"""
import numpy as np
from PIL import Image

def img2array(im, mode='L', dtype=int):
    """
    将image格式图片转成numpy.array格式图片
    :param im:
    :param dtype:
    :return:
    """
    # 转成灰度图后，再转成array数组
    im=np.array(im.convert(mode=mode),dtype=dtype)
    return im

def array2img(array):
    """
    将numpy数组转成image格式图片
    :param array:
    :return:
    """
    return Image.fromarray(array)

def img2binary(im, threshold ,pic='array'):
    """
    将图片转成二值化
    :param array:
    :return:
    """
    # 转灰度图，转成array数组
    if pic=='image':
        im=np.array(im.convert('L'),dtype=int)
    # 二值化
    im[im <= threshold]=0
    im[im > threshold] = 1
    return im


