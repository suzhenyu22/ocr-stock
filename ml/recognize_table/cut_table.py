"""
识别图片中的table

原理挺简单的，首先是根据边框提取一个个单元格，然后识别单元格的内容
"""

import numpy as np
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt


# 读取图片
file=r"E:\python_code\ocrstock\pic\c持仓_表格.png"
im=np.array(Image.open(file).convert('L'),dtype=int)
im[im<=100]=0
im[im>100]=1
plt.imshow(im)


def add_jamb_to_pic(im, jamb=0, padding=1):
    """
    在二值图im的外围添加一个边框.jamb=0表示添加黑色边框，1则是亮的白色边框。
    padding=1表示添加一个像素的边框。
    """
    for i in range(padding):
        x,y=im.shape
        h=np.array([[jamb for i in range(y)]])
        im=np.concatenate((h,im,h),axis=0)
        x, y = im.shape
        c=np.array([[jamb] for i in range(x)])
        im = np.concatenate((c, im, c), axis=1)
    return im

im=add_jamb_to_pic(im,0,1)
plt.imshow(im)


# 找到行与列的分割点
xup,yup=im.shape  #(88, 295)
# 对列求和,得到x轴坐标
x_axis=im.sum(axis=0)  # 295个元素
# 对行求和，得到y轴坐标
y_axis=im.sum(axis=1)  # 88个元素

# 找到图片分割点坐标，也就是sum=0的点
x_axis=[i for i in range(len(x_axis)) if x_axis[i]==0]
y_axis=[i for i in range(len(y_axis)) if y_axis[i]==0]

# 接下来开始分割
# 从左往右，从上往下
all_pic=[]
for j in range(len(y_axis)-1):
    row_pic=[]
    for i in range(len(x_axis)-1):
        x1,x2=x_axis[i],x_axis[i+1]
        y1,y2=y_axis[j],y_axis[j+1]
        if x2-x1<=1 or y2-y1<=1:
            continue
        else:
            row_pic.append(im[y1+1:y2, x1+1:x2])  # 注意y和x的顺序
    all_pic.append(row_pic)


# 批量绘制
from ocrstock.common.visualization import plot_many_im_matrix,plot_many_im_arrays
plot_many_im_matrix(all_pic)

plot_many_im_arrays(all_pic[1])  #

# 接下来就是解析图片信息了
# 正常情况下，最上面的一行，要么都有内容，要么都没内容
# 因此判断是否需要删除最上面的一行
def cut_frame_non_pic(all_pic):
    """删除四周空白图片"""
    def is_non_pic(sub_im):
        pix_sum = sub_im.shape[0] * sub_im.shape[1]
        # 用0.98或0.02，是默认可以有少数斑点存在
        if sub_im.sum()>= pix_sum*0.995 or sub_im.sum()<=pix_sum*0.005:
            return 1
        else:
            return 0
    # 删除上面的空白图片
    all_pic2=[]
    for i in range(len(all_pic)):
        row=[]
        for j in range(len(all_pic[0])):
            non=is_non_pic(all_pic[i][j])
            print('i=%d j=%d non=%d'%(i,j,non))
            row.append(all_pic[i][j]) if not non else ''
        if len(row)>0:
            all_pic2.append(row)

# 接下来对第一行进行标题识别，对剩下的进行数字串识别
positions=[[],[]]

# 将识别后的内容转成dataframe
positions2=pd.DataFrame(positions[1:],columns=positions[0])




