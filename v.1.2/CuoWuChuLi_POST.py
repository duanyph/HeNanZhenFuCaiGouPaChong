#coding:utf-8
from urllib import request,parse
from urllib.parse import quote
from bs4 import BeautifulSoup
import socket,sqlite3,re
socket.setdefaulttimeout(10)
QingQiu="http://www.hngp.gov.cn/wsscnew/egp/jy/xyghjy/xyghxm/xyghzy/xzsp/XyspList,form.sdirect"
header1={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0",
        "Cookie":open("Cookie.txt","r").read()}
HouZui=["mp3","mp4","txt","pdf","fiv","doc","png","img","jpg","jpeg","bmp","tmp"]
ZhenZeHouZhui=r"(."+r"|.".join(HouZui)+r")$"
URL_ShuJvKu=sqlite3.connect("ShuJvJi.db")
YouBiao=URL_ShuJvKu.cursor()
URL_ShuJvKu.commit()
#链接处理
def LianJieChuli(LianJieJi):
    for LianJie in LianJieJi:
        LianJie=LianJie["href"]
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
        if re.search(r"DirectLink_4", LianJie,re.M|re.I)==None:
            del(LianJie)
            continue
        #链接去重
        YouBiao.execute("select URl from URL_Ji2 where URL='"+LianJie+"'")
        if YouBiao.fetchone()==None:
            YouBiao.execute("insert into URL_Ji2 (URL) values ('"+LianJie+"')")
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
JiCi1=str(input("请输入错误地址2："))
pmbh=input("请输入pmbh码：")
POST_Tou={
        "formids":"gysmcword,skeyword,AddGwc,search,change,jgqj_1,jgqj_2,jgqj_3,jgqj_4,jgqj_5,jgqj_6,xltj,jgtj,sjsjtj,ghslb_qb,ghslb_ds,ghslb_gys",
        "xmxh":"null",
        "area":"00390019",
        "Hidden":pmbh,
        "Hidden_0":"null",
        "cgsl":"0",
        "cgje":"0.0",
        "lastcgsl":"0",
        "lastcgje":"0.0",
        "xyghbh":"null",
        "pmbh":pmbh,
        "ppbh":"null",
        "isnwwbz":"ww",
        "currentPage_Split":JiCi1,
        "pageSize_Split":"12",
        "goToPage_Split":JiCi1,
        }
POST_Tou=parse.urlencode(POST_Tou).encode(encoding='UTF8')
Request3=request.Request(url=QingQiu,headers=header1,data=POST_Tou)
try:
    DaKai_QingQiu=request.urlopen(Request3)
except :
    try:
        DaKai_QingQiu=request.urlopen(Request3)
    except :
        print("打开链接"+url+"超时！略过此链接！")
        RiZhiChuLi(3,url,pmbh,url2,JiCi1)
BeautifulSoup3=BeautifulSoup(DaKai_QingQiu,"lxml",from_encoding="utf-8")
BeautifulSoup3=BeautifulSoup3.find("div",class_="sc_list")
LianJieJi=BeautifulSoup3.find_all("a",href=re.compile(r"(\S+\s?)+"))
LianJieChuli(LianJieJi)
URL_ShuJvKu.commit()
URL_ShuJvKu.close()
