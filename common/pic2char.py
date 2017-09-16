"""
将图片转成字符画
"""



from PIL import Image

def transform(image_file):
    """
    将图片转成字符画
    :param image_file:
    :return:
    """
    # 生成字符画所需的字符集
    codeLib = '''@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,"^`'. '''
    count = len(codeLib)
    # 转换为黑白图片，参数"L"表示黑白模式
    image_file = image_file.convert("L")
    #
    codePic = ''
    for h in range(0,image_file.size[1]):  #size属性表示图片的分辨率，'0'为横向大小，'1'为纵向
        for w in range(0,image_file.size[0]):
            gray = image_file.getpixel((w,h)) #返回指定位置的像素，如果所打开的图像是多层次的图片，那这个方法就返回一个元组
            codePic = codePic + codeLib[int(((count-1)*gray)/256)]#建立灰度与字符集的映射
        codePic = codePic + '\n'
    return codePic

def draw_char_pic(file):
    """
    读取图片，转成字符图
    :param file:
    :return:
    """
    im = Image.open(file)    # 读取图片
    im = im.resize((int(im.size[0] * 0.1), int(im.size[1] * 0.1)))  # 调整图片大小为原来的10%
    txt = transform(im) #转
    print(txt)  # 打印效果



