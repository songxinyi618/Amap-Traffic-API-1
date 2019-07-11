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

#input your own key. Here is xinyi's key.
ak=r"9f32c962835c771c560ead42368febe7"

#input the coordinates
left_bottom = [121.488254,31.205333] #Should be in Baidu coordinate system
right_top = [121.513445,31.226069] #Should be in Baidu coordinate system

#input your filepath
filepath=r"C:\Users\Xin-yi.Song\Desktop\百度API\董家渡\高德13\\" #设置存放路径,最后需要两个斜杠，其中一个是转义符

#input step_length(seconds),data will be collected every step_length
step_length=300

#prefix of gaode API
url0=r"https://restapi.amap.com/v3/traffic/status/rectangle?"
#https://restapi.amap.com/v3/traffic/status/rectangle?key=您的key&rectangle=116.351147,39.966309;116.357134,39.968727
############################提取参数###########################################

lng1=str(left_bottom[0])
lat1=str(left_bottom[1])
lng2=str(right_top[0])
lat2=str(right_top[1])
#矩形对角线不能超过10公里

'''
默认值：level=5 
1：高速路 
2：快速路、国道
3：高速辅路
4：主要道路 
5：一般道路 
6：无名道路
'''

#################判断空函数#############################
def valid(arr,key):#此处定义了判断字典key值是否存在,arr为输入的字典,key为需要判断的关键字
    if key in arr.keys():
        return arr[key]
    else:
        return '此值为空'
    
############################Get road names####################################
def road_names(): #此处定义了road_names()函数，用于创建文件并写表头
    
    for i in range(1,7):
        url=url0+'key='+ak+'&rectangle='+lng1+','+lat1+';'+lng2+','+lat2+'&extensions=all'+'&level='+str(i)
        res=urlopen(url)
        cet=res.read()
        result=json.loads(cet)
        #print(result)
    
        trafficinfo=result['trafficinfo']
        roads=trafficinfo['roads']
    
        if len(roads)==0:
            print('level=',i,'区域内无可查询道路！')
        else:
            for element in roads:
                road_name=element['name']
                Header = u'道路等级',u'道路名称',u'日期',u'时',u'分',u'区域拥堵描述',u'畅通所占百分比',u'缓行所占百分比',u'拥堵所占百分比',u'未知路段所占百分比',u'道路路况',u'方向',u'角度',u'速度',u'经纬度'
                filename = filepath+road_name+'.csv'
                with open(filename, "w", newline='') as csv_file:
                    writer = csv.writer(csv_file, delimiter=',')
                    writer.writerow(Header)
                
        
###########################Get congestion info#################################
def road_congestion(sc):

    start = time.clock()#记录开始时间，为了观察爬取一次需要多久
    print('开始时间为：',start)    

    for i in range(1,7):
        print('现在开始查询level=',i)
        url=url0+'key='+ak+'&rectangle='+lng1+','+lat1+';'+lng2+','+lat2+'&extensions=all'+'&level='+str(i)
        res=urlopen(url)
        cet=res.read()
        result=json.loads(cet)
        print(result)
    
        date=(time.strftime('%Y-%m-%d',time.localtime(time.time())))
        h=(time.strftime('%H',time.localtime(time.time())))
        m=(time.strftime('%M',time.localtime(time.time())))
    
        trafficinfo=result['trafficinfo']
        description=trafficinfo['description']#'区域拥堵描述'
        expedite=trafficinfo['evaluation']['expedite']#'畅通所占百分比'
        congested=trafficinfo['evaluation']['congested']#'缓行所占百分比'
        blocked=trafficinfo['evaluation']['blocked']#'拥堵所占百分比'
        unknown=trafficinfo['evaluation']['unknown']#'未知道路所占百分比'
    
        roads=trafficinfo['roads']
 
        if len(roads)==0:
            print('level=',i,'区域内无可查询道路！')
        else:
            for element in roads:
                road_name=element['name']
                filename = filepath+road_name+'.csv'
            
                if len(element)==1:#只返回路名，不包含拥堵情况
                    traffic=[i,road_name,date,h,m,description,expedite,congested,blocked,unknown]
                else:
                    status=valid(element,'status')#道路路况
                    direction=valid(element,'direction')#'方向'
                    angle=valid(element,'angle')#'角度'
                    speed=valid(element,'speed')#'速度'
                    polyline=valid(element,'polyline')#'平均通行速度'
                    traffic=[i,road_name,date,h,m,description,expedite,congested,blocked,unknown,status,direction,angle,speed,polyline]
                
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
    

