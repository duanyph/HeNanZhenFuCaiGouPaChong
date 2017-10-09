#coding:utf-8
from urllib import request,parse
from urllib.parse import quote
from bs4 import BeautifulSoup
import socket,sqlite3,re
JiCi=0
socket.setdefaulttimeout(5)
RiZhi=open("URL_RiZhi.log","w")
RiZhi.close()
header1={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0"}
url_QiShi="http://www.hngp.gov.cn/wsscnew/egp/jy/xyghjy/xyghxm/XyghxmIndex.html?area=00390019"
HouZui=["mp3","mp4","txt","pdf","fiv","doc","png","img","jpg","jpeg","bmp","tmp"]
ZhenZeHouZhui=r"(."+r"|.".join(HouZui)+r")$"
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
    for ShangPing_URl in LianJieJi:
        LianJie=ShangPing_URl["href"]
        if re.search(r"^\/$\#\S+",LianJie,re.M|re.I)!=None:
            del(LianJie)
            continue
        elif re.search(r"javascript",LianJie,re.I|re.M)!=None:
            del(LianJie)
            continue
        elif re.search(r"\#\S*",LianJie,re.M|re.I)!=None:
            del(LianJie)
            continue
        elif re.search(r"^\\\\$",LianJie,re.M|re.I)!=None:
            del(LianJie)
            continue
        elif re.search(r"^\\$",LianJie,re.M|re.I)!=None:
            del(LianJie)
        elif re.search(ZhenZeHouZhui,LianJie,re.M|re.I)!=None:
            del(LianJie)
            continue
        elif re.search(r"^\/\/$",LianJie,re.M|re.I)!=None:
            del(LianJie)
            continue
        elif re.search(r"^\/\/\S", LianJie,re.M|re.I)!=None:
            LianJie="http:"+LianJie
        elif re.search(r"^\/\S", LianJie,re.M|re.I)!=None:
            LianJie="http://www.hngp.gov.cn"+LianJie
        elif re.search(r"\w\/$", LianJie,re.M|re.I)!=None:
            LianJie=LianJie[:-1]
        else:
            del(LianJie)
            continue
        if re.search(r"http://www.hngp.gov.cn/wsscnew|https://www.hngp.gov.cn/wsscnew", LianJie,re.M|re.I)==None:
            del(LianJie)
            continue
        #链接去重
        YouBiao.execute("select URl from URL_Ji1 where URL='"+LianJie+"'")
        if YouBiao.fetchone()==None:
            ShangPing=ShangPing_URl.get_text()
            YouBiao.execute("insert into URL_Ji1 (URL,商品) values ('"+LianJie+"','"+ShangPing+"')")
        else:
            del(LianJie)
            continue
        print("采集链接："+LianJie)
    URL_ShuJvKu.commit()
#错误日志处理
def RiZhiChuLi(CuoWuMa,url=None,pmbh=None,url2=None,JiCi1=None):
    RiZhi=open("URL_RiZhi.log","a+")
    RiZhi.write(str(CuoWuMa)+"|"+str(JiCi)+"|"+url+"|"+pmbh+"|"+url2+"|"+str(JiCi1)+"\n")
    RiZhi.close()
while 1:
    JiCi+=1
    YouBiao.execute("select URL from URL_Ji1 where ID="+str(JiCi))
    url=YouBiao.fetchone()
    if url!=None:
        url=url[0]
    else:
        break
    url=quote(url,'\/:?=;@&+$,%.#\n')
    Request1=request.Request(url,headers=header1)
    try:
        try:
            DaKai_url=request.urlopen(Request1)
        except :
            try:
                DaKai_url=request.urlopen(Request1)
            except :
                print("打开链接"+url+"超时！略过此链接！")
                RiZhiChuLi(1,url,pmbh,url2,JiCi1)
                continue
        print(str(JiCi)+"|打开链接"+url)
        BeautifulSoup1=BeautifulSoup(DaKai_url,"html.parser",from_encoding="utf-8")
        #提取链接
        LianJieJi=BeautifulSoup1.find_all("a",href=re.compile(r"(\S+\s?)+"))
        LianJieChuli(LianJieJi)
    except KeyboardInterrupt:
        print("终止运行！")
        break
    # except :
        # RiZhiChuLi(3,url,pmbh,url2,JiCi1)
        # print("|打开链接"+url+"出现异常！略过此链接！")
        # continue
#     time.sleep(0.2)
    #循环次数控制
    # if JiCi>=50:
        # break
URL_ShuJvKu.commit()
URL_ShuJvKu.close()
