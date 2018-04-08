#coding:utf-8
from urllib import request,parse
from urllib.parse import quote
from bs4 import BeautifulSoup
import socket,sqlite3,re
socket.setdefaulttimeout(5)
header1={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0"}
url_QiShi="http://222.143.21.205:8081"
# HouZui=["mp3","mp4","txt","pdf","fiv","doc","png","img","jpg","jpeg","bmp","tmp"]
# ZhenZeHouZhui=r"(."+r"|.".join(HouZui)+r")$"
URL_ShuJvKu=sqlite3.connect("ShuJvJi.db")
YouBiao=URL_ShuJvKu.cursor()
try:
    YouBiao.execute("drop table URL_Ji1")
except:
    pass
YouBiao.execute("CREATE TABLE URL_Ji1 (ID INTEGER PRIMARY KEY,URL TEXT,商品 TEXT)")
YouBiao.execute("insert into URL_Ji1 (URL) values('"+url_QiShi+"')")
URL_ShuJvKu.commit()
#链接处理
def LianJieChuli(LianJieJi):
    JiCi=0
    for ShangPing_URl in LianJieJi:
        JiCi+=1
        LianJie=ShangPing_URl["href"]
        LianJie=url_QiShi+LianJie
        #链接去重
        YouBiao.execute("select URl from URL_Ji1 where URL='"+LianJie+"'")
        if YouBiao.fetchone()==None:
            ShangPing=ShangPing_URl.get_text()
            YouBiao.execute("insert into URL_Ji1 (URL,商品) values ('"+LianJie+"','"+ShangPing+"')")
        else:
            continue
        print(str(JiCi)+"|采集链接："+LianJie)
    URL_ShuJvKu.commit()
YouBiao.execute("select URL from URL_Ji1 where ID=1")
url=YouBiao.fetchone()
url=quote(url[0],'\/:?=;@&+$,%.#\n')
Request1=request.Request(url,headers=header1)
try:
    DaKai_url=request.urlopen(Request1)
except :
    print("打开链接"+url+"错误！")
    exit()
print("打开链接:"+url)
BeautifulSoup1=BeautifulSoup(DaKai_url,"html.parser",from_encoding="utf-8")
#提取链接
LianJieJi=BeautifulSoup1.find_all("a",target="_self")
LianJieChuli(LianJieJi)
URL_ShuJvKu.commit()
URL_ShuJvKu.close()
