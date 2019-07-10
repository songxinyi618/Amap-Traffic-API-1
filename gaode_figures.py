# -*- coding: utf-8 -*-
"""
Created on Wed Jul  3 11:50:03 2019

@author: xin-yi.song
"""

import os
import xlrd
import glob
import pandas as pd

savefile_path = r'C:\Users\Xin-yi.Song\Desktop\百度API\董家渡\结果\高德_合并_0629'   #拼接后要保存的文件路径
section_path = r'C:\Users\Xin-yi.Song\Desktop\百度API\董家渡\结果\高德_合并_0629\路段组合'   
roads = ['复兴东路','河南南路','陆家浜路','中山南路','蓬莱路','中华路','江阴路','紫霞路','王家码头路','董家渡路','外仓桥街','南仓街']

###########################删除不需要的路#######################################
os.getcwd()
os.chdir(savefile_path)

file_list = glob.glob('*.csv')

for file in file_list:
    file_name = file.split('.csv')[0]
    
    if file_name not in roads:
        os.remove(savefile_path+'\\'+file)
        
##########################导入方向#############################################
os.getcwd()
os.chdir(section_path)

roads_list = glob.glob('*.xlsx')

for road in roads_list:
    wb = xlrd.open_workbook(section_path+'\\'+road,encoding_override='gbk')
    sheet = pd.read_excel(wb,engine='xlrd')
    sheet = sheet[['从','到','自定义方向']]
    
    road_name = road.split('.xlsx')[0]
    f = open(savefile_path+'\\'+road_name+'.csv',encoding='utf-8')
    df = pd.read_csv(f)
    
    dff = pd.merge(df,sheet,how='left', on=['从','到'])
    print(dff)
    
    ###########################不要重复生成########################
    dff.to_csv(savefile_path+'\\'+road_name+'.csv',encoding="utf_8_sig",index=False)
    
##########################自定义挑选最小值函数###################################
def minimum(dataframe):

    dataframe = dataframe.reset_index().sort_values(by=['时间','速度'],ascending=True) 
    dataframe.drop_duplicates(subset='时间',keep='first',inplace = True)
    return dataframe
    
##########################按方向画图###########################################

import matplotlib.pyplot as plt
#%matplotlib qt5 #在命令行中输入，用于在窗口显示图片
#%matplotlib inline #在console中显示 


os.getcwd()
os.chdir(savefile_path)


if not os.path.exists(savefile_path+'\\'+'图片'): #判断一个目录是否存在
    os.mkdir(savefile_path+'\\'+'图片') #创建目录

file_list = glob.glob('*.csv')

for file in file_list:
    fff = open(savefile_path+'\\'+file, encoding='utf-8')
    dfff = pd.read_csv(fff)
    
    direction = dfff['自定义方向']
    dd = list(direction.unique())
    #print(direction.value_counts())
    
    names = locals() #动态定义变量
    for i in range(0,len(dd)):
        title_1 = file.split('.csv')[0]
        title_2 = dd[i]
        title_3 = dfff.loc[1,'日期']#定义日期，可更换
        
        names['d%s' %i] = dfff[dfff['自定义方向']==dd[i]].reset_index(drop = True)
        for j in range(0,names['d%s' %i].shape[0]):
            hour = names['d%s' %i].loc[j,'时']
            minute = names['d%s' %i].loc[j,'分']
            names['d%s' %i].loc[j,'时间'] = '%02d:%02d' % (hour,minute)
        #print(names['d%s' %i]['时间'])
        
        names['d%s' %i] = minimum(names['d%s' %i])
        
        x = list(range(0,names['d%s' %i].shape[0]))#标记共有多少行
        y = names['d%s' %i]['速度']
        x_ticks = (names['d%s' %i]['时间'])
        title = title_1+'-'+title_2+'('+title_3+')'
        
        plt.figure(figsize=(20,7))
        plt.title(title, loc ='center', fontsize='large',fontproperties='FangSong')
        plt.xlim((0,names['d%s' %i].shape[0]-1))
        plt.xticks(x,x_ticks,rotation=90,fontproperties='FangSong')
        plt.xlabel('时间',fontproperties='FangSong')
        plt.ylabel('速度',fontproperties='FangSong')
        fig, = plt.plot(x,y,color='red',linewidth=1.5,linestyle='-')
        plt.show()
        plt.savefig(savefile_path+'\\'+'图片'+'\\'+title+'.png')
        plt.close()
       
        del names['d%s' %i] #删除变量