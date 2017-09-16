"""
屏幕截图

获取屏幕截图，转成numpy数组，供其他模块进行分析
"""

from PIL import ImageGrab
import matplotlib.pyplot as plt
import numpy as np

def get_screenshot():
    """
    屏幕截图，二值化，然后转成numpy数组返回
    :return:
    """
    im = np.array(ImageGrab.grab().convert('L'), dtype=int)
    return im

def show_screenshot():
    """
    屏幕截图，二值化，然后绘制图形
    :return:
    """
    im = np.array(ImageGrab.grab().convert('L'),dtype=int)
    plt.imshow(im)

    plt.imsave(im,r"C:\Users\zhenyu\Desktop\test\p1-2.png")