# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 09:48:33 2019

@author: xin-yi.song
"""

import pandas as pd
#%matplotlib qt5 #在命令行中输入，用于在窗口显示图片
#%matplotlib inline #在console中显示 


domain = r'C:\Users\Xin-yi.Song\Desktop\百度API\董家渡\结果'
file_list = ['高德_合并_0703','高德_合并_0629', '高德_合并_0630']

######################修改方向###############################################
for file in file_list:
    
    f = open(domain+'\\'+file+'\\'+'中华路.csv', encoding='utf-8')
    df = pd.read_csv(f,header=0)
    
    for i,element in enumerate(df['自定义方向']):
        if element=='西向东':
            df.loc[i,'自定义方向']='西向北'
        elif element=='南向北':
            df.loc[i,'自定义方向']='西向北'
        elif element=='东向西':
            df.loc[i,'自定义方向']='北向西'
        elif element=='北向南':
            df.loc[i,'自定义方向']='北向西'
    
    df.to_csv(domain+'\\'+file+'\\'+'中华路.csv',encoding="utf_8_sig",index=False)