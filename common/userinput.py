"""
模拟鼠标键盘操作。

本以为点击任务栏的图标很方便的，但是没有想到鼠标移动有效，点击就是没有小。
只能曲线实现了，先移动鼠标，显示缩略图后，再点击缩略图实现

"""

import time
from pymouse import PyMouse
from pykeyboard  import PyKeyboard

m=PyMouse()
k=PyKeyboard()

def click_ico(x,y):
    """
    针对点击图标专门写一个点击函数。
    需要注意的是，这里的x,y对应np.array.shape的y,x
    """
    # 在win10下一直无法实现，能移动鼠标，但是点击就是没有用
    m=PyMouse()
    m.click(x,y)


def mouse_click(x,y,button=1,n=1):
    """模拟鼠标点击"""
    # 注意，这里将 x,y=y,x
    # 是为了和 plt.image 的处理保存一致的理解
    m.click(x=y,y=x,button=button,n=n)
    time.sleep(0.5)

def keyboard_input(string=None,function_key=None, keys=[]):
    """模拟键盘输入"""
    # 如果是普通键盘输入
    if string:
        k.type_string(string)
        time.sleep(0.2)
        return
    #如果是功能键，比如F1,F2
    if function_key:
        num=int(function_key.lower().replace('f',''))
        k.tap_key(k.function_keys[num])  # Tap F5
        time.sleep(0.2)
        return

def keyboard_enter():
    """键盘回车键"""
    k.tab_key([k.enter_key])
    time.sleep(0.1)

def keyboard(string):
    """键盘输入"""























