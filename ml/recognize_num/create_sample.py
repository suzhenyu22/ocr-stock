"""
批量生成测试需要的图片
"""
import os
import datetime
import numpy as np
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
resize_dim=(10,15)




def create_pic(string, pix=15, font_path=None, threshold=150):
    """
    将数字写到图片中，返回numpy数组的图片
    """
    # 字体
    if not font_path:
        font_path=r"C:\Windows\Fonts\jdytjian.TTF"  # 经典圆体简
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
    im[im<=threshold]=0
    im[im > threshold] = 1
    return im

def create_random_num():
    """生成随机数字字符串，结尾加上小数点"""
    t=[str(i) for i in np.random.randint(0, 10, size=10)]
    t=''.join(t)+'.'
    return t


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
                nums1 = split_num(im)
                x,y=resize_dim
                nums2 = [resize_pic(p, x, y) for p in nums1]
                # 保存图片,之所以搞这么多余，是因为在宋体下，有可能两个数字粘连导致无法切分出错
                if len(nums1)==len(string):
                    for i in range(len(nums1)):
                        name = '10' if string[i] == '.' else string[i]
                        # 保存原图
                        file1 = os.path.join(pict_path, '%s_%d_old.png' % (name, id))
                        Image.fromarray(nums1[i]).save(file1)
                        # 保存resize图
                        file2 = os.path.join(pict_path, '%s_%d_resize.png' % (name, id))
                        Image.fromarray(nums2[i]).save(file2)
                        # id自增
                        id+=1
                # 打印信息
                t=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print('%s pix=%2d string=%s font=%s'%(t,pix,string,os.path.split(font)[-1]))
    #
    return


def test():

    # 生成测试样本数据
    create_sample()

    # 拿其中的两幅图画出来看看
    from ocrstock.common.visualization import plot_many_im_arrays
    file1=''
    file2=''
    im1 = np.array(Image.open(file1).convert('L'),dtype=int)
    im2 = np.array(Image.open(file2).convert('L'), dtype=int)
    plot_many_im_arrays([im1,im2])











