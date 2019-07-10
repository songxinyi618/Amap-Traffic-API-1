# -*- coding: utf-8 -*-
"""
Created on Tue May 14 17:39:47 2019
@author: xin-yi.song
"""

import json
from urllib.request import urlopen
import time
import sched
import csv

#input your own key. Here is xinyi's ak.
ak=r"5UK6Um2nRBqID8cTTgYblTbGQREW8DtC"

#input the coordinates
left_bottom = [121.499083,31.2177] #Should be in Baidu coordinate system
right_top = [121.511839,31.228308] #Should be in Baidu coordinate system

#input your filepath
filepath=r"C:\Users\xin-yi.song\Desktop\百度API\董家渡\原始数据\百度_5\\" #设置存放路径,最后需要两个斜杠，其中一个是转义符

#input step_length(seconds),data will be collected every step_length
step_length=300

#prefix of Baidu API
url0=r"http://api.map.baidu.com/traffic/v1/bound?"
#http://api.map.baidu.com/traffic/v1/bound?ak=你的AK&bounds=39.912078,116.464303;39.918276,116.475442&coord_type_input=gcj02&coord_type_output=gcj02//GET请求

############################提取参数###########################################

lng1=str(left_bottom[0])
lat1=str(left_bottom[1])
lng2=str(right_top[0])
lat2=str(right_top[1])
url=url0+'ak='+ak+'&bounds='+lat1+','+lng1+';'+lat2+','+lng2+'&road_grade=0'

'''
默认值：road_grade=0 
0：全部驾车道路 
1：高速路 
2：环路及快速路 
3：主干路 
4：次干路 
5：支干路
'''

############################Get road names####################################
def road_names(): #此处定义了all_heads函数，用于创建文件并写表头
    
    res=urlopen(url)
    cet=res.read()
    result=json.loads(cet)
    print(result)
    
    road_traffic=result['road_traffic']
    if len(road_traffic)==0:
        print('区域内无可查询道路！')
    else:
        for element in road_traffic:
            road_name=element['road_name']
            Header = u'道路名称',u'日期',u'时',u'分',u'区域拥堵描述',u'区域路况评价',u'区域路况评价描述',u'拥堵路段',u'路段拥堵评价',u'较十分钟前拥堵趋势',u'拥堵距离',u'平均通行速度'
            filename = filepath+road_name+'.csv'
            with open(filename, "w", newline='') as csv_file:
                writer = csv.writer(csv_file, delimiter=',')
                writer.writerow(Header)
                
        
###########################Get congestion info#################################
def road_congestion(sc):

    start = time.clock()#记录开始时间，为了观察爬取一次需要多久
    print('开始时间为：',start)    
   
    res=urlopen(url)
    cet=res.read()
    result=json.loads(cet)
    print(result)
    
    date=(time.strftime('%Y-%m-%d',time.localtime(time.time())))
    h=(time.strftime('%H',time.localtime(time.time())))
    m=(time.strftime('%M',time.localtime(time.time())))
    
    x = result
    description=x['description']#'区域拥堵描述'
    evaluation_status=x['evaluation']['status']#'区域路况评价'
    evaluation_status_desc=x['evaluation']['status_desc']#'区域路况评价描述'
    road_traffic=x['road_traffic']
 
    if len(road_traffic)==0:
        print('区域内无可查询道路！')
    else:
        for element in road_traffic:
            road_name=element['road_name']
            filename = filepath+road_name+'.csv'
            
            if len(element)==1:#只返回路名，不包含拥堵情况
                traffic=[element['road_name'],date,h,m,description,evaluation_status,evaluation_status_desc]
            else:
                congestion=element['congestion_sections']
                section_desc=congestion[0]['section_desc']#'拥堵路段'
                status=congestion[0]['status']#'路段拥堵评价'
                congestion_trend=congestion[0]['congestion_trend']#'较十分钟前拥堵趋势'
                congestion_distance=congestion[0]['congestion_distance']#'拥堵距离'
                speed=congestion[0]['speed']#'平均通行速度'
                
                traffic=[element['road_name'],date,h,m,description,evaluation_status,evaluation_status_desc,section_desc,status,congestion_trend,congestion_distance,speed]
                
            #print(traffic)
            f = csv.writer(open(filename, "a+",newline=''))
            f.writerow(traffic)

    end = time.clock()#记录结束时间
    print('结束时间为',end)
    
    cost = end-start#计算程序运行时间，6条路大概占用2秒
    print("程序运行时间为 : %.03f seconds" %(cost)) 
    
    sc.enter(step_length, 1, road_congestion, (sc,))

#################主函数开始#########################      
s = sched.scheduler(time.time, time.sleep)

road_names()#创建文件，并写表头

s.enter(step_length, 1, road_congestion, (s,)) # 调用函数，格式为(delay, priority, action, argument)
s.run()        
    

