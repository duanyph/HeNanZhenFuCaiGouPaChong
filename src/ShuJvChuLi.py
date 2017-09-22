#coding:utf-8
from urllib import request
from bs4 import BeautifulSoup
from urllib.parse import quote
from urllib import parse
import sqlite3
import csv
import time
import re
header1={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0"}
JiCi=0
URL_ShuJvKu=sqlite3.connect("URL_Ji.db")
YouBiao=URL_ShuJvKu.cursor()
try:
    YouBiao.execute("drop table ShuJvJi")
except:
    pass
YouBiao.execute("""
CREATE TABLE ShuJvJi (
    ID INTEGER PRIMARY KEY,
    商品 TEXT,
    得分 TEXT,
    供货商 TEXT,
    服务承诺 TEXT,
    报价 TEXT,
    联系人 TEXT,
    移动电话 TEXT,
    办公电话 TEXT,
    更新时间 TEXT)
""")
URL_ShuJvKu.commit()
#数据提取
def ShuJv(BeautifulSoup1,xhbh):
    ShangPing=BeautifulSoup1.find("div",class_="sc_pro_m").find("h1").get_text()
    BeautifulSoup2=XiangQingBiao(xhbh)
    tr_ji=BeautifulSoup2.find_all("tr")
    tr_ji=tr_ji[1:]
    for tr in tr_ji:
        JiLu=tr.find_all("td")
        FenShu=JiLu[1].get_text()
        GongHuo=JiLu[2].find("a").get_text()
        FuWu=re.findall(r"\w",JiLu[3].get_text())[0]
        BaoJia=JiLu[4].get_text()
        LianXiRen=JiLu[5].get_text()
        ShouJi=JiLu[6].get_text()
        DianHua=re.findall(r"(\S+)*",JiLu[7].get_text())[0]
        GengXinShiJian=JiLu[8].get_text()
        print("采集数据:",ShangPing,FenShu,GongHuo,FuWu,BaoJia,LianXiRen,ShouJi,DianHua,GengXinShiJian)
        YouBiao.execute("insert into ShuJvJi (商品,得分,供货商,服务承诺,报价,联系人,移动电话,办公电话,更新时间) values('"+ShangPing+"','"+FenShu+"','"+GongHuo+"','"+FuWu+"','"+BaoJia+"','"+LianXiRen+"','"+ShouJi+"','"+DianHua+"','"+GengXinShiJian+"')")
        URL_ShuJvKu.commit()
#商品列表处理
def XiangQingBiao(xhbh):
    QingQiu="http://www.hngp.gov.cn/wsscnew/egp/public/gg_spzsxx/SpxhMainTab,form.direct"
    POST_Tou={
    "formids":"If,sl,jbcsPage,ghsPage,jgqsPage,picPage,spxqPage,Xzsp,Gwc,Xmxx,Dzdd,Ddys,selgys",
    "If":"F",
    "xhbh":xhbh,
    "area":"00390019",
    "ghsPage":"供货商",
    }
    POST_Tou=parse.urlencode(POST_Tou).encode(encoding='UTF8')
    Request1=request.Request(url=QingQiu,headers=header1,data=POST_Tou)
    XiangYing=request.urlopen(Request1)
    BeautifulSoup1=BeautifulSoup(XiangYing,"html.parser",from_encoding="utf-8")
    return BeautifulSoup1
while 1:
    JiCi+=1
    YouBiao.execute("select URL from URL_Ji where ID="+str(JiCi))
    url=YouBiao.fetchone()
    if url!=None:
        url=url[0]
    else:
        break
    try:
        if re.search(r"DirectLink_4.direct",url)!=None:
            url=quote(url,'\/:?=;@&+$,%.#\n')
            Request1=request.Request(url,headers=header1)
            xhbh=re.findall(r"sp=S?(\w+)&",url)[0]
            url2="http://www.hngp.gov.cn/wsscnew/egp/public/gg_spzsxx/SpxhMainTab.html?xhbh="+xhbh+"&xmxh=null&area=00390019&xyghbh=ff80808151561b4701517a41b243602e&lastcgsl=0&cgje=0.0&lastcgje=0.0&cgsl=0&isnwwbz=ww&czy=null&lbbs=null"
            url2=quote(url2,'\/:?=;@&+$,%.#\n')
            Request3=request.Request(url=url2,headers=header1)
            DaKai_url2=request.urlopen(Request3)
            print(str(JiCi)+"|打开链接："+url2)
            BeautifulSoup2=BeautifulSoup(DaKai_url2,"html.parser",from_encoding="utf-8")
            ShuJv(BeautifulSoup2,xhbh)
    except KeyboardInterrupt:
        print("终止运行！")
        break
    except :
        print("|打开链接"+url2+"出现异常！略过此链接！")
        continue
URL_ShuJvKu.commit()
URL_ShuJvKu.close()