# -*- coding: utf-8 -*-
"""
Created on Mon Jul  1 10:15:01 2019

@author: xin-yi.song
"""

import os
import shutil
import glob
import pandas as pd

source_path = r'C:\Users\Xin-yi.Song\Desktop\百度API\董家渡\原始数据\百度_1'   #原始文件夹
savefile_path = r'C:\Users\Xin-yi.Song\Desktop\百度API\董家渡\结果\百度_0629'   
roads = ['复兴东路','河南南路','陆家浜路','中山南路','蓬莱路','中华路','江阴路','紫霞路','王家码头路','董家渡路','外仓桥街','南仓街']

###########################复制有用的路#######################################
os.getcwd()
os.chdir(source_path)

file_list = glob.glob('*.csv')

for file in file_list:
    file_name = file.split('.csv')[0]
    
    if file_name in roads:
        shutil.copyfile(source_path+'\\'+file, savefile_path+'\\'+file)
        

############################画图##############################################
import math  
import matplotlib.pyplot as plt 
'''
路段拥堵评价(int)
支持以下值：
0：未知路况
1：畅通
2：缓行
3：拥堵
4：严重拥堵
'''    
        
os.getcwd()
os.chdir(savefile_path)

if not os.path.exists(savefile_path+'\\'+'图片'): #判断一个目录是否存在
    os.mkdir(savefile_path+'\\'+'图片') #创建目录

file_list = glob.glob('*.csv')

for file in file_list:
    f = open(savefile_path+'\\'+file, encoding='gbk')
    df = pd.read_csv(f)

    title_1 = file.split('.csv')[0]
    title_2 = df.loc[1,'日期']#定义日期，可更换
    
    for j in range(0,df.shape[0]):
        hour = df.loc[j,'时']
        minute = df.loc[j,'分']
        df.loc[j,'时间'] = '%02d:%02d' % (hour,minute)
    df['路段拥堵评价']=df['路段拥堵评价'].apply(lambda x: 1 if math.isnan(x) else x)#文字转数字

 
    x = list(range(0,df.shape[0]))#标记共有多少行
    y = df['路段拥堵评价']

    x_ticks = (df['时间'])
    title = title_1+'('+title_2+')'
        
    plt.figure(figsize=(20,7))
    plt.title(title, loc ='center', fontsize='large',fontproperties='FangSong')
    plt.xlim((0,df.shape[0]-1))
    plt.ylim((0,4))
    plt.xticks(x,x_ticks,rotation=90,fontproperties='FangSong')
    plt.yticks(range(0,5),['未知路况','畅通','缓行','拥堵','严重拥堵'],fontproperties='FangSong')
    plt.xlabel('时间',fontproperties='FangSong')
    plt.ylabel('路段拥堵评价',fontproperties='FangSong')
    fig, = plt.plot(x,y,color='red',linewidth=1.5,linestyle='-')
    plt.show()
    plt.savefig(savefile_path+'\\'+'图片'+'\\'+title+'.png')
    plt.close()



