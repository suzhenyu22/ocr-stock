"""
识别图片是否是表格的标题，用于提取持仓信息步骤
"""
import os
import datetime
import numpy as np
import pandas as pd
from PIL import Image,ImageDraw,ImageFont

# 导入图片处理函数
from ocrstock.common.cut_pic import cut_blank, split_num, resize_pic


# 制定数据存放位置
pict_path=r'C:\Users\zhenyu\Desktop\test\train_data'  # 生成的训练样本数据存放目录

# 定义字体位置
win_fonts=[ r'‪C:\Windows\Fonts\simsun.ttc', # 宋体
            r'C:\Windows\Fonts\simkai.ttf',  # 楷体
            r'C:\Windows\Fonts\jdytjian.TTF', # 经典圆体简
            r'‪C:\Windows\Fonts\msyh.ttc',   # 微软雅黑
           # r'C:\Windows\Fonts\arial.ttf',
           # r'C:\Windows\Fonts\calibri.ttf'
    ]

# resize图片的尺寸
resize_dim=(40,15)

# title-num的映射
labels={'持仓':0, '可买':1, '可卖':2}




def create_pic(string, pix=15, font_path=None, threshold=100):
    """
    将数字写到图片中，返回numpy数组的图片
    """
    # 生成图片的高度和宽度
    size=(500,300)
    # 背景颜色，默认为白色
    bgcolor = (255, 255, 255)
    # 字体颜色，默认为黑色
    fontcolor = (0, 0, 0)
    # 下面开始干活
    image = Image.new('RGBA', size, bgcolor)  # 创建图片
    font = ImageFont.truetype(font_path, pix)  # 验证码的字体，指定字体大小
    draw = ImageDraw.Draw(image)  # 创建画笔
    text = string
    draw.text((2, 2), text, font=font, fill=fontcolor)  # 填充字符串
    # image.save(r"C:\Users\zhenyu\Desktop\test\create.png")
    im=np.array(image.convert('L'),dtype=int)
    # 二值化
    im[im <= threshold]=0
    im[im > threshold] = 1
    return im

def create_random_num(labels):
    """随机抽取一个标题返回"""
    i=np.random.randint(0,len(labels),1)[0]
    return list(labels.keys())[i]


def create_sample():
    """
    将上面的流程串起来，批量生成测试图片
    :return:
    """
    # 测试的字体
    fonts=win_fonts
    # 测试的字号变化
    pixs=list(range(15,25))
    # 循环测试
    id=0
    for font in fonts:
        for pix in pixs:
            for _ in range(10):
                # 生成随机字符串
                string = create_random_num()
                # 生成对应的图片数组, # 删除周边空白 # 切割图片 # resize图片
                im = create_pic(string, pix=pix, font_path=font)
                im = cut_blank(im, xleft=0, yleft=0)
                x,y=resize_dim
                im2=resize_pic(im,x,y)
                # 保存原图
                file1 = os.path.join(pict_path, '%s_%d_old.png' % (string, id))
                Image.fromarray(im).save(file1)
                # 保存resize图
                file2 = os.path.join(pict_path, '%s_%d_resize.png' % (string, id))
                Image.fromarray(im2).save(file2)
                # id自增
                id+=1
                # 打印信息
                t=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print('%s pix=%2d string=%s font=%s'%(t,pix,string,os.path.split(font)[-1]))
    #
    return


def transform_pic_to_train_data():
    """将图片读取出来，摊平，得到train data"""
    path=''
    files = [os.path.join(path, file) for file in os.listdir(path) if 'resize' in file]
    ims = []
    lables = []
    ids = []
    for file in files:
        # 读取图片，转成array数组，然后摊平成一维数组
        im = np.array(Image.open(file).convert('L'), dtype=int).ravel().tolist()
        ims.append(im)
        # 解析标签，将中文映射为数字
        label = os.path.split(file)[-1].split('_')[0]
        label = labels[label]
        lables.append(label)
        # 解析id
        id = os.path.split(file)[-1].split('_')[1].split('.')[0]
        ids.append(id)
    # 转成dataframe
    data = pd.DataFrame(ims)
    data.columns = ['c%d' % (i + 1) for i in range(data.shape[1])]
    # 定义标签列
    data['label'] = lables
    data['id'] = ids
    return data









def test():
    # 生成测试样本数据
    create_sample()

    # 拿其中的两幅图画出来看看
    from ocrstock.common.visualization import plot_many_im_arrays
    file1 = ''
    file2 = ''
    im1 = np.array(Image.open(file1).convert('L'), dtype=int)
    im2 = np.array(Image.open(file2).convert('L'), dtype=int)
    plot_many_im_arrays([im1, im2])










