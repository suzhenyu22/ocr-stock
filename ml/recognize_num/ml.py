"""
使用逻辑回归训练模型
"""
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report


pict_path=r'C:\Users\zhenyu\Desktop\test\train_data'  # 生成的训练样本数据存放目录


def load_data(file):
    """加载数据"""
    data=pd.read_csv(file)
    # 划分训练集测试集
    trains,tests=train_test_split(data)
    # 区分x,y，id
    xcol = [col for col in data.columns if 'c' in col]
    ycol = ['label']
    idcol=['id']
    xtrain,xtest=np.array(trains[xcol]),np.array(tests[xcol])
    ytrain,ytest=np.array(trains[ycol]),np.array(tests[ycol])
    id_train,id_test=np.array(trains[idcol]),np.array(tests[idcol])
    # 将y_test转一维数组
    ytest=ytest.ravel()
    id_test=id_test.ravel()
    # 返回
    return xtrain,xtest,ytrain,ytest,id_train,id_test


def find_wrong_sample(ytest,ypred, xtest, id_test):
    """找出那些真实值和预测值不一样的样本"""
    # 将y_test转一维数组
    pics, true, wrong, idx=[],[],[],[]
    for i in range(len(ytest)):
        if ytest[i]!=ypred[i]:
            pics.append(xtest[i])       # 找到图片
            true.append(ytest[i])   # 真实值
            wrong.append(ypred[i])     # 错误预测的值
            idx.append(id_test[i])      # 图片id
    #
    print('真实值和预测值对比')
    [print('%2d_%2d -> %2d '%(t,id,p)) for t, p,id in zip(true, wrong,idx)]
    return pics, true, wrong, idx

def get_true_pic(true, idx):
    """读取真实图数据"""
    true_pics=[]
    for i in range(len(idx)):
        file=str(true[i])+'_'+str(idx[i])+'_old.png'
        file=os.path.join(pict_path,file)
        pic=np.array(Image.open(file).convert('L'),dtype=int)
        true_pics.append(pic)
    return true_pics



def plot_wrong_sample(pics, true, wrong, idx):
    """将真实值和预测值绘制在同一张图上"""
    # 随机取5个
    cnt=5 if len(true)>10 else len(true)
    nums=list(range(cnt))
    pics=[pics[i].reshape(15,10) for i in nums]
    idx=[idx[i] for i in nums]
    # 布局，绘图
    # 左边绘制真实图，右边绘制预测图
    # 读取预测图
    true_pics=get_true_pic(true, idx)
    # 绘图
    ixs=[(cnt,2,i+1) for i in range(cnt*2)]
    for i in range(cnt*2):
        r,c,ii=ixs[i]
        plt.subplot(r,c,ii)
        if i%2==0:
            plt.imshow(true_pics[i])
        else:
            plt.imshow(pics[i])
    # 打印对比情况
    print('true-pred')
    tp=[print(t,'-',p) for t,p in zip(true,wrong)]










def test():
    """测试"""

    # 加载数据，划分训练集和测试集
    file=r"E:\stock_data\train_data.csv"
    xtrain, xtest, ytrain, ytest, id_train, id_test=load_data(file)


    # 建立多分类模型
    from sklearn.linear_model import LogisticRegression
    m=LogisticRegression(max_iter=500)
    m.fit(xtrain,ytrain)
    ypred=m.predict(xtest)

    # 评估模型
    print(classification_report(ytest, ypred))


    # 朴素贝叶斯
    from sklearn.naive_bayes import GaussianNB
    from sklearn.naive_bayes import MultinomialNB
    from sklearn.naive_bayes import BernoulliNB
    m=GaussianNB()
    m=MultinomialNB()
    m=BernoulliNB()
    m.fit(xtrain, ytrain)
    ypred = m.predict(xtest)

    # 评估模型
    print(classification_report(ytest, ypred))

    # 决策树
    from sklearn.tree import DecisionTreeClassifier
    m=DecisionTreeClassifier()
    m.fit(xtrain, ytrain)
    ypred = m.predict(xtest)

    # 评估模型
    print(classification_report(ytest, ypred))

    # svm
    from sklearn.svm import SVC
    m=SVC()
    m.fit(xtrain, ytrain)
    ypred = m.predict(xtest)

    # 评估模型
    print(classification_report(ytest, ypred))

    # 保存模型
    from sklearn.externals import joblib
    file=r'E:\python_code\ocrstock\ml\recognition_num\recognition_num_lr_model.m'
    joblib.dump(m, file)

