#coding:utf-8
from urllib import request,parse
from urllib.parse import quote
from bs4 import BeautifulSoup
import socket,sqlite3,re,time
url_QiShi="http://222.143.21.205:8081"
socket.setdefaulttimeout(15)
RiZhi=open("URL_RiZhi.log","r+")
RiZhi.readline()
# RiZhi.write("错误码|错误链接|pmbh码|错误地址|错误链接2\n")
# RiZhi.close()
header1={"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0",
        # "Cookie":open("Cookie.txt","r").read()
        }
""" HouZui=["mp3","mp4","txt","pdf","fiv","doc","png","img","jpg","jpeg","bmp","tmp"]
ZhenZeHouZhui=r"(."+r"|.".join(HouZui)+r")$" """
URL_ShuJvKu=sqlite3.connect("ShuJvJi.db")
YouBiao=URL_ShuJvKu.cursor()
#链接处理
def LianJieChuli(LianJieJi):
    for LianJie in LianJieJi:
        LianJie=LianJie.find("a")["href"]
        LianJie=url_QiShi+LianJie
        #链接去重
        YouBiao.execute("select URl from URL_Ji2 where URL='"+LianJie+"'")
        if YouBiao.fetchone()==None:
            YouBiao.execute("insert into URL_Ji2 (URL) values ('"+LianJie+"')")
        else:
            continue
        print("采集链接："+LianJie)
    URL_ShuJvKu.commit()
def LieBiaoYe(pmbh,YeShu):
    QingQiu="http://222.143.21.205:8081/category/list"
    for JiCi1 in range(1,int(YeShu)+1):
        POST_Tou={
            "pmbh":pmbh,
            "pageNo":JiCi1,
        }
        POST_Tou=parse.urlencode(POST_Tou).encode(encoding='UTF8')
        Request3=request.Request(url=QingQiu,headers=header1,data=POST_Tou)
        try:
            DaKai_QingQiu=request.urlopen(Request3)
        except :
            try:
                DaKai_QingQiu=request.urlopen(Request3)
            except :
                print("获取参数为pmbh="+pmbh+",pageNo="+JiCi1+"的响应数据超时，略过！")
                continue
        BeautifulSoup3=BeautifulSoup(DaKai_QingQiu,"lxml",from_encoding="utf-8")
        LianJieJi=BeautifulSoup3.find_all("div",class_="item-pic")
        LianJieChuli(LianJieJi)
        time.sleep(0.5)
while 1:
    DuHang=RiZhi.readline()
    if DuHang==None:
        break
    DuHang=DuHang.split("|")
    if DuHang[0]=="1" or DuHang[0]=="3":
        #提取链接
        pmbh=re.findall(r"pmbh=(\w+)",DuHang[1])[0]
        url2="http://222.143.21.205:8081/category/list?pmbh="+pmbh
        url2=quote(url2,'\/:?=;@&+$,%.#\n')
        Request2=request.Request(url=url2,headers=header1)
        try:
            DaKai_url2=request.urlopen(Request2)
        except :
            try:
                DaKai_url2=request.urlopen(Request2)
            except :
                print("打开链接："+url2+"超时，略过！")
                continue
        print("打开链接："+url2)
        BeautifulSoup2=BeautifulSoup(DaKai_url2,"html.parser",from_encoding="utf-8")
        #列表页处理
        YeShu=BeautifulSoup2.find("li",class_="disabled controls").get_text()
        YeShu=re.findall(r"当前\s\d+\/(\d+)页",YeShu)[0]
        LieBiaoYe(pmbh,YeShu)
    elif DuHang[0]=="2":
        LieBiaoYe(DuHang[2],DuHang[3])
RiZhi.close()
URL_ShuJvKu.commit()
URL_ShuJvKu.close()
