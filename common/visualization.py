"""
可视化
"""

from PIL import Image
import numpy as np
import matplotlib.pyplot as plt


def plot_im_array(array, title='', xlabel='',ylabel=''):
    """针对一个图片数组的绘图"""
    if not isinstance(array,np.ndarray):
        raise Exception('输入不是numpy.array，请检查')
    # 绘图
    plt.imshow(array)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.table(title)

def plot_many_im_arrays(arrays):
    """对多幅array图片绘图, arrays 是 list-np.array 格式"""
    # 子图数量
    pic_cnt=len(arrays)
    # 布局
    cols=3  # 每行3个子图
    rows=int(pic_cnt/cols) if pic_cnt/cols == int(pic_cnt/cols) else  int(pic_cnt/cols)+1   # 行数
    # 绘图
    ixs = [(rows,cols,i+1) for i in range(pic_cnt)]
    for i in range(len(arrays)):
        r,c,ii=ixs[i]
        plt.subplot(r,c,ii)
        plt.imshow(arrays[i])

def plot_many_im_matrix(llist):
    """对list-list存储的矩阵图绘图"""
    # 对图片resize，否则画在同一张图上很难看
    shape=[i.shape for j in llist for i in j]
    x=max([i[0] for i in shape])
    y=max([j[1] for j in shape])
    # 转成图片后resize
    all_pic=[]
    for i in range(len(llist)):
        row_pic=[]
        for j in range(len(llist[0])):
            subim=Image.fromarray(llist[i][j])
            subim = np.array(subim.resize((y, x), Image.ANTIALIAS))
            row_pic.append(subim)
        all_pic.append(row_pic)
    llist=all_pic
    # 行数，列数
    row=len(llist)
    col=max([len(i) for i in llist])
    # 绘图
    ixs=[(row,col,i+1) for i in range(row*col)]
    for i in range(row):
        for j in range(col):
            r,c,ii=ixs[i*row+j]
            if len(llist[i])<j+1:
                continue
            else:
                plt.subplot(r, c, ii)
                plt.imshow(llist[i][j])
