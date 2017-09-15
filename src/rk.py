#coding:utf-8
"""http://www.hngp.gov.cn/wsscnew/egp/jy/xyghjy/xyghxm/xyghzy/xzsp/XyspList.html?pmbh=00480001000800100030&cgsl=0&cgje=0.0&ppbh=null&lastcgsl=0&lastcgje=0.0&xmxh=null&xyghbh=null&isnwwbz=ww&area=00390019&czy=null&lbbs=null"""
from urllib import request
from bs4 import BeautifulSoup
from urllib.parse import quote
import csv
import time
import re
JiCi=0
url_QiShi="http://www.hngp.gov.cn/wsscnew/egp/jy/xyghjy/xyghxm/XyghxmIndex.html?area=00390019"
HouZui=["mp3","mp4","txt","pdf","fiv","doc","png","img","jpg","jpeg","bmp","tmp"]
ZhenZeHouZhui=r"(."+r"|.".join(HouZui)+r")$"
url_Du=open("url_ji.txt","r")
url_Du2=open("url_ji.txt","r")
url_Xie=open("url_ji.txt","a")
url_Xie.write(url_QiShi+"\n")
url_Xie.flush()
WenJian=open("数据集.csv","a+",encoding='utf-8',newline='')
xie=csv.writer(WenJian,dialect="excel")
xie.writerow([])
#数据提取
def ShuJv(html1):
    pass
#链接处理
def LianJieChuli(LianJieJi,url_Ji):
    url_Ji2=[]
    for LianJie in LianJieJi:
        LianJie=LianJie["href"]
        if re.search(r"^\/$\#\S+",LianJie,re.M|re.I)!=None:
            del(LianJie)
        elif re.search(r"javascript",LianJie,re.I|re.M)!=None:
            del(LianJie)
        elif re.search(r"\#\S*",LianJie,re.M|re.I)!=None:
            del(LianJie)
        elif re.search(r"^\\\\$",LianJie,re.M|re.I)!=None:
            del(LianJie)
        elif re.search(r"^\\$",LianJie,re.M|re.I)!=None:
            del(LianJie)
        elif re.search(ZhenZeHouZhui,LianJie,re.M|re.I)!=None:
            del(LianJie)
        elif re.search(r"^\/\/$",LianJie,re.M|re.I)!=None:
            del(LianJie)
        elif re.search(r"^\/\/\S", LianJie,re.M|re.I)!=None:
            LianJie="http:"+LianJie
        elif re.search(r"^\/\S", LianJie,re.M|re.I)!=None:
            LianJie="http://www.hngp.gov.cn"+LianJie
        elif re.search(r"\w\/$", LianJie,re.M|re.I)!=None:
            LianJie=LianJie[:-1]
        else:
            del(LianJie)
        if re.search(r"http://|https://", LianJie,re.M|re.I)==None:
            del(LianJie)
        if LianJie in url_Ji:
            del(LianJie)
        else:
            LianJie=LianJie+"\n"
            url_Ji2.append(LianJie)
    url_Ji2=list(set(url_Ji2))
    url_Xie.writelines(url_Ji2)
    url_Xie.flush()
for url in url_Du:
    url_Du.flush()
    url_Du2.flush()
    url_Ji=url_Du2.read()
    JiCi+=1
    #打开链接
    url=quote(url,'\/:?=;@&+$,%.#\n')
    print(url)
    Request1=request.Request(url)
    Request1.add_header("User-Agent","Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0")
#     try:
    DaKai_url=request.urlopen(Request1)
    if DaKai_url.getcode()!=200:
        print(str(JiCi)+"|打开链接"+url+"失败！略过此链接！")
#         continue
#     else:
#         print(str(JiCi)+"|打开链接"+url+"成功！")
    BeautifulSoup1=BeautifulSoup(DaKai_url,"html.parser",from_encoding="utf-8")
    #数据提取
#         if re.search(r"",url)!=None:
#             ShuJv(BeautifulSoup1)
    #提取链接
    LianJieJi=BeautifulSoup1.find_all("a",href=re.compile(r"(\S+\s?)+"))
    LianJieChuli(LianJieJi,url_Ji)
#     except KeyboardInterrupt:
#         print("终止运行！")
#         break
#     except :
#         print(str(JiCi)+"|打开链接"+url+"出现异常！略过此链接！")
#         continue
#     time.sleep(0.2)
    #循环次数控制
#     if JiCi>=100:
#         break
url_Xie.close()
url_Du.close()
url_Du2.close()
WenJian.close()