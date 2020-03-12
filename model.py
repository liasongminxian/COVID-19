# -*- coding: utf-8 -*-
"""
Created on Wed Feb  5 20:09:38 2020
project name:2019-nCoV logistic模型
@author: 帅帅de三叔
"""
import numpy as np #导入数值计算模块
import pandas as pd #导入数据处理模块
import matplotlib.pyplot as plt #导入绘图模块
from scipy.optimize import curve_fit #导入拟合模块
plt.rcParams["font.sans-serif"]="SimHei" #黑体中文
plt.rcParams["axes.unicode_minus"]=False #显示负号
# data=pd.read_csv("20200205病例.csv") #读取数据
data = pd.read_csv("F:\Python\疫情数据\\2020-03-10疫情数据\中国疫情历史数据.csv", encoding='GB2312') #读取数据
date = data['日期'] #日期
confirm = data['累计确诊病例'] #确诊数
t = range(len(confirm)) #构造横轴
# print(t)

fig=plt.figure(figsize=(10,4)) #建立画布
ax=fig.add_subplot(1, 1, 1)
ax.scatter(t,confirm, color="k",label="确诊人数") #真实数据散点图
ax.set_xlabel("日期") #横坐标
ax.set_ylabel("确诊人数") #纵坐标
ax.set_title("确诊人数随时间变化情况") #标题
ax.set_xticklabels(['', '1月13号', '1月23号', '2月2号', '2月10号','2月20号','3月1号'], rotation=30, fontsize=10) #自定义横坐标标签


def logistic(t,K,P0,r): #定义logistic函数
    exp_value=np.exp(r*(t))
    return (K*exp_value*P0)/(K+(exp_value-1)*P0)

coef, pcov = curve_fit(logistic, t, confirm) #拟合
print(coef) #logistic函数参数
y_values = logistic(t,coef[0], coef[1], coef[2]) #拟合y值
print(y_values)
ax.plot(t,y_values,color="blue", label="拟合曲线") #画出拟合曲线


x=np.linspace(len(confirm),66,67-len(confirm)) #构造期货日期
y_predict=logistic(x,coef[0], coef[1], coef[2]) #未来预测值
ax.scatter(x,y_predict, color="red",label="未来预测") #未来预测散点
ax.legend() #加标签
plt.show()


