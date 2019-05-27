#!/usr/bin/python
# -*- coding:utf-8 -*-

'''
天气查询脚本
输入城市名称即可获取天气情况
'''

import xml.dom.minidom as xml
from urllib.error import URLError
import urllib
import requests
import re


def GetData( msg, num):
    '''
    获取对应信息
    :param msg: 标签类型
    :param num: 第几天
    :return:
    '''
    try:
        dom = xml.parse("WeatherApi")
    except:
        print("数据解析出错")
        exit()
    num=int(num)
    data = dom.documentElement
    dom = data.getElementsByTagName(msg)
    x = dom[num].firstChild.data
    return x

class weather():
    def __init__(self,name):
        self.cityname = name


    def ParseUrl(self):
        '''
        拼接url
        :return:
        '''
        self.url = "http://wthrcdn.etouch.cn/WeatherApi?city="+self.cityname   #url拼接
        #print(self.url)


    def UrlRequest(self):
        '''
        获取网页文本信息
        :return:
        '''
        try:
            result = requests.get(self.url)       #url访问
            res = result.text                     #获取网页文本
            self.result=result.content
            m=re.search('invalid city',res,re.S)
            if m != None:
                print("抱歉，查询不到"+self.cityname+"的信息")    #如果城市名不正确或查询不到，显示错误
                exit()

        except URLError as e:
            print(e)

    def DataWrite(self):
        '''
        保存xml数据到本地
        :return:
        '''

        with open("WeatherApi","wb") as f:
            f.write(self.result)
            f.close()





    def LoadsResult(self):
        '''
        解析xml格式数据
        需要转换为utf8编码
        :return:
        '''


        for i in range(0,3):              #一共有四组信息
            msg="[  城市： ]  "+GetData("city","0")+"\n"\
                    "[  日期： ]  "+GetData("date",i)+"\n"\
                    "[  温度： ]  "+GetData("wendu","0")+"\n"\
                    "[ 最高温：]  "+GetData("high",i)+"\n"\
                    "[ 最低温：]  "+GetData("low",i)+"\n"\
                    "[  风向： ]  "+GetData("fengxiang",i)+"\n"\
                    "[  风力： ]  "+GetData("fengli",i)+"\n"\
                    "[  天气： ]  "+GetData("type",i)+"\n"
            print(msg)

        print("-----温馨提示-----\n")
        for i in range(0,10):
            msg=GetData("name",i)+"："+GetData("value",i)+"\n"+"[  tips： ]  "+GetData("detail",i)+"\n"
            print(msg)



def main():
    city = input("请输入需要查询的城市\n")    #获取城市名称
    x = weather(city)                         #类方法
    x.ParseUrl()                              #构造url
    x.UrlRequest()                            #访问url
    x.DataWrite()                             #存储xml数据
    x.LoadsResult()                           #解析数据

if __name__ == "__main__":
    main()