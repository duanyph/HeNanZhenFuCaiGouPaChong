#coding:utf-8
from urllib import request,parse
from urllib.parse import quote
from bs4 import BeautifulSoup
import socket,sqlite3,re,time
JiCi=1
url_QiShi="http://222.143.21.205:8081"
socket.setdefaulttimeout(15)
RiZhi=open("URL_RiZhi.log","w")
RiZhi.write("错误码|错误链接|pmbh码|错误地址|错误链接2\n")
RiZhi.close()
header1={"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0",
        # "Cookie":open("Cookie.txt","r").read()
        }
""" HouZui=["mp3","mp4","txt","pdf","fiv","doc","png","img","jpg","jpeg","bmp","tmp"]
ZhenZeHouZhui=r"(."+r"|.".join(HouZui)+r")$" """
URL_ShuJvKu=sqlite3.connect("ShuJvJi.db")
YouBiao=URL_ShuJvKu.cursor()
try:
    YouBiao.execute("drop table URL_Ji2")
except:
    pass
YouBiao.execute("CREATE TABLE URL_Ji2 (ID INTEGER PRIMARY KEY,URL TEXT)")
URL_ShuJvKu.commit()
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
#错误日志处理
def RiZhiChuLi(CuoWuMa,url="None",pmbh="None",JiCi1="None",url2="None"):
    RiZhi=open("URL_RiZhi.log","a+")
    RiZhi.write(str(CuoWuMa)+"|"+url+"|"+pmbh+"|"+str(JiCi1)+"\n")
    RiZhi.close()
while 1:
    JiCi+=1
    YouBiao.execute("select URL from URL_Ji1 where ID="+str(JiCi))
    url=YouBiao.fetchone()
    if url==None:
        break
    try:
        #提取链接
        pmbh=re.findall(r"pmbh=(\w+)",url[0])[0]
        url2="http://222.143.21.205:8081/category/list?pmbh="+pmbh
        url2=quote(url2,'\/:?=;@&+$,%.#\n')
        Request2=request.Request(url=url2,headers=header1)
        try:
            DaKai_url2=request.urlopen(Request2)
        except :
            try:
                DaKai_url2=request.urlopen(Request2)
            except :
                print("打开链接："+url+"超时，略过此链接！")
                RiZhiChuLi(1,url2,None,None,None)
                continue
        print(str(JiCi)+"|打开链接："+url2)
        BeautifulSoup2=BeautifulSoup(DaKai_url2,"html.parser",from_encoding="utf-8")
        #列表页处理
        YeShu=BeautifulSoup2.find("li",class_="disabled controls").get_text()
        YeShu=re.findall(r"当前\s\d+\/(\d+)页",YeShu)[0]
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
                    RiZhiChuLi(2,None,pmbh,JiCi1,None)
                    continue
            BeautifulSoup3=BeautifulSoup(DaKai_QingQiu,"lxml",from_encoding="utf-8")
            LianJieJi=BeautifulSoup3.find_all("div",class_="item-pic")
            LianJieChuli(LianJieJi)
        time.sleep(0.5)
    except KeyboardInterrupt:
        print("终止运行！")
        break
    except :
        RiZhiChuLi(3,url,pmbh,JiCi1,url2)
        print("出现异常,已记录到日志！")
        continue
URL_ShuJvKu.commit()
URL_ShuJvKu.close()
