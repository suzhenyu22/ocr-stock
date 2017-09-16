"""
整理生成测试数据.
生成的测试图片已经是二值图了

"""

import os
import numpy as np
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt

path=r'C:\Users\zhenyu\Desktop\test\train_data'

def load_all_pic(path):
    """读取所有图片"""
    files=[os.path.join(path,file) for file in os.listdir(path) if 'resize' in file ]
    ims=[]
    lables=[]
    ids=[]
    for file in files:
        # 读取图片，转成array数组，然后摊平成一维数组
        im=np.array(Image.open(file).convert('L'),dtype=int).ravel().tolist()
        ims.append(im)
        # 解析标签
        label=os.path.split(file)[-1].split('_')[0]
        lables.append(label)
        # 解析id
        id=os.path.split(file)[-1].split('_')[1].split('.')[0]
        ids.append(id)
    # 转成dataframe
    data=pd.DataFrame(ims)
    data.columns=['c%d'%(i+1) for i in range(data.shape[1])]
    # 定义标签列
    data['label']=lables
    data['id']=ids
    # 将字符标转成数字标签
    def to_int(s):
        if s=='.':
            return 10
        else:
            return int(s)
    data['label']=data['label'].apply(to_int)
    return data

# file=r'C:\Users\zhenyu\Desktop\test\train_data\10_73.png'

def main():
    # 定义路径
    path = r'C:\Users\zhenyu\Desktop\test\train_data'

    # 读取所有图片数据
    data=load_all_pic(path)

    # 保存到文件
    file=r"C:\Users\zhenyu\Desktop\test\train_data.csv"
    data.to_csv(file,index=False)