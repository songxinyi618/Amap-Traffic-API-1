# -*- coding: utf-8 -*-
"""
Created on Mon Jul  8 12:09:22 2019

@author: xin-yi.song
"""

import os
import glob
import xlrd
import time
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
#%matplotlib qt5 #在命令行中输入，用于在窗口显示图片
#%matplotlib inline #在console中显示 


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
 
###########################主要部分#######################################
domain = r'C:\Users\Xin-yi.Song\Desktop\百度API\董家渡\结果'
file_list = ['高德_合并_0703','高德_合并_0629', '高德_合并_0630']
week_list = ['周三','周六','周日']
savefile_path = r'C:\Users\Xin-yi.Song\Desktop\百度API\董家渡\结果\高德_全合并'

if not os.path.exists(savefile_path+'\\'+'图片_合并'): #判断一个目录是否存在
    os.mkdir(savefile_path+'\\'+'图片_合并') #创建目录

os.chdir(domain+'\\'+file_list[0])
roads = glob.glob('*.csv')
#roads = ['中华路.csv']

for road in roads:
####保存变量
    wb = xlrd.open_workbook(savefile_path+'\\'+'已标记_'+road.split('.csv')[0]+'_路段全合并.xlsx',encoding_override='gbk')
    sheet = pd.read_excel(wb,engine='xlrd')
    sheet = sheet[['从','到','角度','标记']]
    nn = locals() #动态定义变量 
   
    for i in range(0,len(file_list)):
        #删除不需要的路段
        f = open(domain+'\\'+file_list[i]+'\\'+road, encoding='utf-8')
        df = pd.read_csv(f,header=0)
        df = pd.merge(df,sheet,how='inner', on=['从','到','角度'])
        df = df[df['标记']==1]
        df.drop(columns=['标记'],inplace=True)
        #统计方向个数
        direction = df['自定义方向']
        dd = list(direction.unique())
        #将数据按时间、按方向保存在单独的变量中
        for j in range(0,len(dd)):
            nn['d%s_%s' %(i,j)] = df[df['自定义方向']==dd[j]].reset_index(drop = True)
####针对每条路进行绘图
    fig = plt.figure(figsize=(23, 10))###########设置图片大小
           
    mark = 0 
    for i in range(0,len(file_list)):
        for j in range(0,len(dd)):
            
            mark=mark+1         
            for t in range(0,nn['d%s_%s' %(i,j)].shape[0]):
                hour = nn['d%s_%s' %(i,j)].loc[t,'时']
                minute = nn['d%s_%s' %(i,j)].loc[t,'分']
                nn['d%s_%s' %(i,j)].loc[t,'时间'] = '%02d:%02d' % (hour,minute)
        
            info= nn['d%s_%s' %(i,j)].describe()
            #print(file_list[i],dd[j],info)
            nn['d%s_%s' %(i,j)] = minimum(nn['d%s_%s' %(i,j)])
            nn['d%s_%s' %(i,j)] = fifteen(nn['d%s_%s' %(i,j)])
        
            #################补充完整时间表#########################################
            hour_new = []
            for hh in range(7,21):
                hour_new.extend([hh]*60)
                minute_new = list(range(0,60))*14
            new_table = pd.DataFrame(data ={'时':hour_new, '分':minute_new})
        
            dff = pd.merge(new_table,nn['d%s_%s' %(i,j)],how='left', on=['时','分'])#进行全表格拼接
            dff['时间'] = list(map(lambda y,z: '%02d:%02d' % (y,z), dff['时'],dff['分']))
                    
            x = np.arange(0,840,30)
            x_ticks = dff['时间'].iloc[x]
            y = dff['自定义速度']
        
            #################绘图设置###############################################
            index = [ii for ii in range(len(y)) if not math.isnan(y[ii])]
            for ii in index[:-2]: 
                iii = index[index.index(ii)+1]
                time1array = time.strptime(dff.loc[ii,'日期']+' '+dff.loc[ii,'时间'],'%Y-%m-%d %H:%M') #先将字符串转化为时间数组
                time2array = time.strptime(dff.loc[iii,'日期']+' '+dff.loc[iii,'时间'],'%Y-%m-%d %H:%M')
            
                t1 = time.mktime(time1array) #将时间数组转化为时间戳
                t2 = time.mktime(time2array)  
          
                if (t2-t1)<18000:#如果时间差小于5小时*60分*60秒=18000
                    plt.subplot(len(file_list),len(dd),mark)
                    plt.subplots_adjust(wspace =0.15, hspace =0.5)#调整子图间距  
                    #print([ii,iii],[y[ii],y[iii]])
                    plt.plot([ii,iii],[y[ii],y[iii]],color='red',linewidth=1.5,linestyle='-')
                            
            #######设置图片格式########
            title_1 = road.split('.csv')[0]    
            title_2 = dd[j]
            title_3 = nn['d%s_%s' %(i,j)].loc[1,'日期']
            title_4 = week_list[i]
            title = title_1+'-'+title_2+'('+title_3+','+title_4+')'
            plt.title(title, loc ='center', fontsize=20,fontproperties='FangSong')

            plt.xlim((0,841))
            plt.ylim(0,51)  

            plt.xticks(x,x_ticks,rotation=45,fontsize='small',fontproperties='FangSong')
            plt.yticks(np.arange(0,51,5))
        
            plt.xlabel('时间',fontproperties='FangSong')
            plt.ylabel('自定义速度',fontproperties='FangSong') 
       
    plt.show()

    plt.savefig(savefile_path+'\\'+'图片_合并'+'\\'+road.split('.csv')[0]+'_合并.png')
    plt.close()
    
 
            
            


