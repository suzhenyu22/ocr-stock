"""
分割图片成子图片.

原理是，两个文字之间应该是有空格的，通过捕捉这样的空间来切分开来。

只对二值化的图片切割。

对二值化图像按列进行sum之后，如果某列都是空白的，那么这一列的sum值达到最大，通过识别这个值来确定分割点。

注意：
1. 二值化后，亮的地方是1，表示空白，文字或者图片信息是黑色的，数值是0
2. 图片im尺寸x*y, 但是 im.shape = y,x


"""
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt


def cut_blank(im, xleft=0, yleft=0):
    """
    删除图片左右两边和上下两边的空白。
    left表示要留的空白的数量，如果left>0,表示不是完全删除，而是部分删除。
    毕竟全部删了也不好看。
    概念类似深度学习中的padding。
    :param im:
    :param xleft:
    :param yleft:
    :return:
    """
    # 先按照left=0方法找到边界值
    # 计算图片的尺寸
    sy, sx = im.shape
    x = im.sum(axis=0)
    y = im.sum(axis=1)
    # 剔除左右两边的空白
    # 找到左边第一个非空值
    px1,px2=0,0
    py1,py2=0,0
    for i in range(sx):  # 一共有64个位置
        # 如果是空，则该位置的加和是sy，因为所有点的像素值是1呀
        if x[i] < sy:
            px1 = i
            break
    # 找到右边第一个非空值
    for i in range(sx - 1, -1, -1):
        if x[i] < sy:
            px2 = i
            break
    # 同理，对上下的空白删除
    for i in range(sy):
        if y[i] < sx:
            py1 = i
            break
    for i in range(sy - 1, -1, -1):
        if y[i] < sx:
            py2 = i
            break
    # 找到四个边界值后，看看left的值
    px1, px2 = px1 - xleft, px2 + xleft
    py1, py2 = py1 - yleft, py2 + yleft
    # 判断是否越界
    px1 = px1 if px1 >= 0 else 0
    px2 = px2 if px2 <= sx - 1 else sx - 1
    py1 = py1 if py1 >= 0 else 0
    py2 = py2 if py2 <= sy - 1 else sy - 1
    # 最后是切割图形
    im = im[py1:py2 + 1, px1:px2 + 1]  # 注意顺序
    return im

def split_num(im):
    """
    切分图像中的数字。要求图像不能有中英文，必须全是数字和小数点。
    之所以单独写一个分割数字的，是因为一串数字之间，一定会有空格的，很好区分。
    而且单个数字内，x轴的sum()值一定是连续的。
    所有数字的高度一定是一样的。
    :param im:
    :return:
    """
    x = im.sum(axis=0)
    up = x.max()  # 找到分割点的阈值
    # 初始化
    for i in range(len(x)):
        if x[i]<up:
            start,nexti=i,i
            break
    # 开始
    words=[]
    while True:
        # 判断是否结束
        if nexti == len(x) - 1:
            if nexti-start>0:
                words.append(im[:,start: nexti+1])  # 注意，如果要取得最后一列，要+1
            break
        # 如果没有结束，就下一步处理
        nexti=nexti+1
        # 判断上一个是否是空，是的话要丢掉上一个
        if x[start]==up:
            start=nexti
            continue
        # 如果到了分割点，就分割处理
        if x[nexti]==up:
            words.append(im[:, start: nexti])
            start=nexti
    # 返回
    return words




def draw_pic_of_num(words):
    """将分割出来的数字绘制出来。注意，数字个数要求<=9"""
    pic_cnt = len(words)
    # 布局
    cols = 3  # 每行3个子图
    rows = int(pic_cnt / cols) if pic_cnt / cols == int(pic_cnt / cols) else  int(pic_cnt / cols) + 1  # 行数
    # 绘图
    ixs = [(rows, cols, i + 1) for i in range(pic_cnt)]
    for i in range(len(words)):
        r, c, ii = ixs[i]
        plt.subplot(r, c, ii)
        plt.imshow(words[i])
    return

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
    im=np.array(im.resize((x,y), Image.ANTIALIAS))
    return im



def test():
    # 读取图片
    file=r"C:\Users\zhenyu\Desktop\test\test_num.png"
    file=r"C:\Users\zhenyu\Desktop\test\test_money2.png"
    im=np.array(Image.open(file).convert('L'))
    im[im<=180]=0
    im[im>180]=1
    plt.imshow(im)
    # 删除四周空白
    im=cut_blank(im)
    # 切分数字
    words=split_num(im)
    # 查看每个数字的大小
    [word.shape for word in words]
    # 绘制图片
    draw_pic_of_num(words)
