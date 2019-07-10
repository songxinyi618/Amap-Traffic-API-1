# -*- coding: utf-8 -*-
"""
Created on Wed Jul  3 11:50:03 2019

@author: xin-yi.song
"""

import os
import time
import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#%matplotlib qt5 #在命令行中输入，用于在窗口显示图片
#%matplotlib inline #在console中显示 

savefile_path = r'C:\Users\Xin-yi.Song\Desktop\百度API\董家渡\结果\高德_合并_0629'   #拼接后要保存的文件路径

##########################自定义挑选最小值函数###################################
def minimum(dataframe):

    dataframe = dataframe.sort_values(by=['时间','速度'],ascending=True).reset_index(drop = True)
    dataframe.drop_duplicates(subset='时间',keep='first',inplace = True)
    dataframe = dataframe.reset_index(drop = True)
    
    return dataframe

##########################自定义合并函数###################################
def fifteen(dataframe):
    
    index = [j for j in range(2,dataframe.shape[0]) if (j+1)%3==0]
    index_all = dataframe.index.values.tolist()
    #print(index)
    
    for i in index:
             
        s1 = dataframe.loc[i-2,'速度'] 
        s2 = dataframe.loc[i-1,'速度'] 
        s3 = dataframe.loc[i,'速度']
        
        time1array = time.strptime(dataframe.loc[i-2,'日期']+' '+dataframe.loc[i-2,'时间'],'%Y-%m-%d %H:%M') #先将字符串转化为时间数组
        time2array = time.strptime(dataframe.loc[i-1,'日期']+' '+dataframe.loc[i-1,'时间'],'%Y-%m-%d %H:%M')
        time3array = time.strptime(dataframe.loc[i,'日期']+' '+dataframe.loc[i,'时间'],'%Y-%m-%d %H:%M')
        
        t1 = time.mktime(time1array) #将时间数组转化为时间戳
        t2 = time.mktime(time2array)
        t3 = time.mktime(time3array)
        
        #print(t1,t2,t3)
        
        
        if (t3-t1)<18000:#如果时间差小于5小时*60分*60秒=18000
            dataframe.loc[i-2,'自定义速度'] = dataframe.loc[i-1,'自定义速度'] = dataframe.loc[i,'自定义速度'] = min(s1,s2,s3)
        elif (t2-t1)<18000:#如果前两个在第一时段
            dataframe.loc[i-2,'自定义速度'] = dataframe.loc[i-1,'自定义速度'] = min(s1,s2)
            dataframe.loc[i,'自定义速度'] = s3
        elif (t3-t2)<18000:#如果后两个在第一时段
            dataframe.loc[i-2,'自定义速度'] = s1
            dataframe.loc[i-1,'自定义速度'] = dataframe.loc[i,'自定义速度'] = min(s2,s3) 
    #print(i)
    
    if (i+1 in index_all) and (i+2 in index_all):
        dataframe.loc[i+1,'自定义速度'] = dataframe.loc[i+2,'自定义速度'] = min(dataframe.loc[i+1,'速度'],dataframe.loc[i+2,'速度'])
    elif (i+1 in index_all) and (i+2 not in index_all):
        dataframe.loc[i+1,'自定义速度'] = dataframe.loc[i+1,'速度']    
        
    return dataframe

##########################按方向画图###########################################

os.getcwd()
os.chdir(savefile_path)


if not os.path.exists(savefile_path+'\\'+'图片_15_调整坐标轴'): #判断一个目录是否存在
    os.mkdir(savefile_path+'\\'+'图片_15_调整坐标轴') #创建目录

file_list = glob.glob('*.csv')

for file in file_list:
    f = open(savefile_path+'\\'+file, encoding='utf-8')
    df = pd.read_csv(f)
    
    direction = df['自定义方向']
    dd = list(direction.unique())
    #print(direction.value_counts())
    
    names = locals() #动态定义变量
    for i in range(0,len(dd)):
        title_1 = file.split('.csv')[0]
        title_2 = dd[i]
        title_3 = df.loc[1,'日期']#定义日期，可更换
        
        names['d%s' %i] = df[df['自定义方向']==dd[i]].reset_index(drop = True)
        for j in range(0,names['d%s' %i].shape[0]):
            hour = names['d%s' %i].loc[j,'时']
            minute = names['d%s' %i].loc[j,'分']
            names['d%s' %i].loc[j,'时间'] = '%02d:%02d' % (hour,minute)
        #print(names['d%s' %i]['时间'])
        
        names['d%s' %i] = minimum(names['d%s' %i])
        names['d%s' %i] = fifteen(names['d%s' %i])
        
        x = list(range(0,names['d%s' %i].shape[0]))#标记共有多少行
        y = names['d%s' %i]['自定义速度']
        x_ticks = (names['d%s' %i]['时间'])
        title = title_1+'-'+title_2+'('+title_3+')'+'-15min'
        #print(title, names['d%s' %i][['时间', '速度', '自定义速度']])
        
        plt.figure(figsize=(20,7))
        plt.title(title, loc ='center', fontsize='large',fontproperties='FangSong')
        plt.xlim((0,names['d%s' %i].shape[0]-1))
        plt.ylim(0,51)
        plt.xticks(x,x_ticks,rotation=90,fontproperties='FangSong')
        plt.yticks(np.arange(0, 51, 5))
        plt.xlabel('时间',fontproperties='FangSong')
        plt.ylabel('自定义速度',fontproperties='FangSong')
        fig, = plt.plot(x,y,color='red',linewidth=1.5,linestyle='-')
        plt.show()
        plt.savefig(savefile_path+'\\'+'图片_15_调整坐标轴'+'\\'+title+'.png')
        plt.close()
       
        del names['d%s' %i] #删除变量