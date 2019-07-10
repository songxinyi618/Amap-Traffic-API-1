# -*- coding: utf-8 -*-
"""
Created on Mon Jul  1 10:15:01 2019

@author: xin-yi.song
"""

import os
import glob
import pandas as pd

domain = r'C:\Users\Xin-yi.Song\Desktop\百度API\董家渡'
folder_list = ['高德2','高德3','高德4','高德5']  #要拼接的文件夹
folder_path = r'C:\Users\Xin-yi.Song\Desktop\百度API\董家渡\高德' #第一个CSV文件所在文件夹
savefile_path = r'C:\Users\Xin-yi.Song\Desktop\百度API\董家渡\结果\高德_合并_1'   #拼接后要保存的文件路径
roads = ['复兴东路','河南南路','陆家浜路','中山南路','蓬莱路','中华路','江阴路','紫霞路','王家码头路','董家渡路','外仓桥街','南仓街']

os.getcwd()
#修改当前工作目录
os.chdir(folder_path)
#将该文件夹下的所有文件名存入一个列表
file_list = glob.glob('*.csv')


for file in file_list:
    #读取第一个CSV文件并包含表头
    f = open(folder_path+'\\'+file)
    df = pd.read_csv(f)
    #将读取的第一个CSV文件写入合并的文件保存
    df.to_csv(savefile_path+'\\'+file,encoding="utf_8_sig",index=False)
    
    #循环遍历所有文件夹中各个CSV文件，并追加到合并后的文件
    for folder in folder_list:
        filepath = domain+'\\'+folder+'\\'+file
        if os.path.isfile(filepath):
            ff = open(filepath)
            dff = pd.read_csv(ff)
            dff.to_csv(savefile_path+'\\'+file,encoding="utf_8_sig",index=False, header=False, mode='a+')


            
################################清理重复数据并划分道路################################
for file in file_list:
    fff = open(savefile_path+'\\'+file, encoding='utf-8')
    dfff = pd.read_csv(fff, header=None)
    if dfff.iloc[0,0]=='道路等级':
        dfff.drop([0],inplace=True)
    dfff.columns=['道路等级','道路名称','日期','时','分',
                  '区域拥堵描述','畅通所占百分比','缓行所占百分比',	'拥堵所占百分比','未知路段所占百分比',
                  '道路路况','方向','角度','速度','经纬度']
    
    #关键词：道路名称、日期、时、分、角度
    subset=[u'道路名称',u'日期',u'时',u'分',u'经纬度']
    #if '道路名称' in dfff.keys():
    dfff = dfff.drop_duplicates(subset,keep='first').reset_index(drop = True)
    
    col_name = dfff.columns.tolist()
    #print(col_name)
    col_name.insert(12,'从')#在方向后1列插入
    col_name.insert(13,'到')#在方向后1列插入
    dfff = dfff.reindex(columns=col_name)
    
    for i,element in enumerate(dfff['方向']):
        element = element.lstrip('从')
        list_temp = element.split('到')
        if len(list_temp) >1:
            dfff.loc[i,'从'] = list_temp[0]
            dfff.loc[i,'到'] = list_temp[1]
        else:
            dfff.loc[i,'从'] = list_temp[0]
    
    dfff.to_csv(savefile_path+'\\'+file,encoding="utf_8_sig",index=False)
    
    if not os.path.exists(savefile_path+'\\'+'路段组合'): #判断一个目录是否存在
        os.mkdir(savefile_path+'\\'+'路段组合') #创建目录
    group = dfff.groupby(['从','到']).size().reset_index().sort_values(by=['从','到'],ascending=True)   
    group.to_csv(savefile_path+'\\'+'路段组合'+'\\'+file,encoding="utf_8_sig",index=False)
    

