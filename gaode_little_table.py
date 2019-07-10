# -*- coding: utf-8 -*-
"""
Created on Mon Jul  8 12:09:22 2019

@author: xin-yi.song
"""

import os
import glob
import pandas as pd
#%matplotlib qt5 #在命令行中输入，用于在窗口显示图片
#%matplotlib inline #在console中显示 

domain = r'C:\Users\Xin-yi.Song\Desktop\百度API\董家渡\结果'
file_list = ['高德_合并_0629', '高德_合并_0630', '高德_合并_0703']
savefile_path = r'C:\Users\Xin-yi.Song\Desktop\百度API\董家渡\结果\高德_全合并'

os.getcwd()
os.chdir(domain+'\\'+file_list[0])

roads = glob.glob('*.csv')

for road in roads:
    dataframe = pd.DataFrame(columns=['道路等级','道路名称','日期','时','分',
                  '区域拥堵描述','畅通所占百分比','缓行所占百分比',	'拥堵所占百分比','未知路段所占百分比',
                  '道路路况','方向','从','到','角度','速度','经纬度','自定义方向'])
    for file in file_list:
        f = open(domain+'\\'+file+'\\'+road, encoding='utf-8')
        df = pd.read_csv(f,header=0)
        dataframe = pd.concat([dataframe, df], axis=0, ignore_index=True)
    
    group = dataframe.groupby(['从','到','角度']).size().reset_index().sort_values(by=['从','到','角度'],ascending=True)
    group.to_excel(savefile_path+'\\'+road.split('.csv')[0]+'_路段全合并.xlsx',encoding="utf_8_sig",index=False)

