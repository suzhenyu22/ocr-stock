"""
输入一串数字图像，然后识别出图片中的数字串
"""
import os
import pandas as pd
from sklearn.externals import joblib

from ocrstock.config.config import gvariable


# 到处图片处理函数
from ocrstock.common import cut_pic

# 训练好的模型
model=os.path.join(gvariable.work_path,r'ml\recognize_num','recognition_num_lr_model.m')
# model=r"F:\wo\python_code\ocrstock\ml\recognize_num\recognition_num_lr_model.m"
m=joblib.load(model)


def rec_nums(im):
    """识别图片中的数字串"""
    # 导入训练好的模型
    # m = joblib.load(model)

    # 删除图片左右两边和上下两边的空白
    im=cut_pic.cut_blank(im)
    # 切分成单个数字
    words=cut_pic.split_num(im)
    # resize
    words=[cut_pic.resize_pic(p,10,15) for p in words]
    # 转成矩阵，摊平处理
    words = [p.ravel().reshape(1, -1) for p in words]

    # 下面是识别程序了
    nums=[m.predict(p)[0] for p in words]
    to_str=lambda x: str(x) if x<10 else '.'
    nums=''.join([to_str(x) for x in nums])
    return nums



def test():
    """测试数字串的识别"""
    from PIL import Image
    import numpy as np
    import matplotlib.pyplot as plt

    # 读取图片
    file=r"E:\stock_data\test_money2.png"
    im=np.array(Image.open(file).convert('L'),dtype=int)
    im[im<=200]=0
    im[im>200]=1
    plt.imshow(im)

    # 识别图片中的文字
    rec_nums(im)
