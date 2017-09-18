#coding:utf-8
from urllib import request
from bs4 import BeautifulSoup
from urllib.parse import quote
from urllib import parse
import csv
import time
import re
JiCi=0
header1={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0"}
url_QiShi="http://www.hngp.gov.cn/wsscnew/egp/jy/xyghjy/xyghxm/XyghxmIndex.html?area=00390019"
HouZui=["mp3","mp4","txt","pdf","fiv","doc","png","img","jpg","jpeg","bmp","tmp"]
ZhenZeHouZhui=r"(."+r"|.".join(HouZui)+r")$"
url_Du=open("url_ji.txt","w+")
url_Du2=open("url_ji.txt","r")
url_Xie=open("url_ji.txt","a")
url_Xie.write(url_QiShi+"\n")
url_Xie.flush()
WenJian=open("数据集.csv","w",encoding='gbk',newline='')
xie=csv.writer(WenJian,dialect="excel")
xie.writerow(["商品","得分","供货商","服务承诺","报价","联系人","移动电话","办公电话","更新时间"])
WenJian.close()
WenJian=open("数据集.csv","a+",encoding='gbk',newline='')
xie=csv.writer(WenJian,dialect="excel")
#数据提取
def ShuJv(BeautifulSoup2,xhbh):
    ShangPing=BeautifulSoup2.find("div",class_="sc_pro_m").find("h1").get_text()
    BeautifulSoup3=XiangQingBiao(xhbh)
    tr_ji=BeautifulSoup3.find_all("tr")
    tr_ji=tr_ji[1:]
    for tr in tr_ji:
        JiLu=tr.find_all("td")
        FenShu=JiLu[1].get_text()
        GongHuo=JiLu[2].find("a").get_text()
        FuWu=re.findall(r"\w",JiLu[3].get_text())[0]
        BaoJia=JiLu[4].get_text()
        LianXiRen=JiLu[5].get_text()
        ShouJi=JiLu[6].get_text()
        DianHua=re.findall(r"\w",JiLu[7].get_text())[0]
        GengXinShiJian=JiLu[8].get_text()
        xie.writerow([ShangPing,FenShu,GongHuo,FuWu,BaoJia,LianXiRen,ShouJi,DianHua,GengXinShiJian])
        # print(FenShu,GongHuo,FuWu,BaoJia,LianXiRen,ShouJi,DianHua,GengXinShiJian)
def XiangQingBiao(xhbh):
    QingQiu="http://www.hngp.gov.cn/wsscnew/egp/public/gg_spzsxx/SpxhMainTab,form.direct"
    QingQiuTou={
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:55.0) Gecko/20100101 Firefox/55.0",
    }
    POST_tou={
    "formids":"If,sl,jbcsPage,ghsPage,jgqsPage,picPage,spxqPage,Xzsp,Gwc,Xmxx,Dzdd,Ddys,selgys",
    "If":"F",
    "xhbh":xhbh,
    "area":"00390019",
    "ghsPage":"供货商",
    }
    POST_tou=parse.urlencode(POST_tou).encode(encoding='UTF8')
    Request2=request.Request(url=QingQiu,headers=QingQiuTou,data=POST_tou)
    XiangYing=request.urlopen(Request2)
    BeautifulSoup3=BeautifulSoup(XiangYing,"html.parser",from_encoding="utf-8")
    return BeautifulSoup3
#链接处理
def LianJieChuli(LianJieJi,url_Ji):
    url_Ji2=[]
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
        if re.search(r"http://www.hngp.gov.cn/wsscnew|https://www.hngp.gov.cn/wsscnew", LianJie,re.M|re.I)==None:
            del(LianJie)
            continue
        if LianJie in url_Ji:
            del(LianJie)
            continue
        else:
            LianJie=LianJie+"\n"
            url_Ji2.append(LianJie)
    url_Ji2=list(set(url_Ji2))
    url_Xie.writelines(url_Ji2)
    url_Xie.flush()
url_Du.flush()
for url in url_Du:
    url_Du.flush()
    url_Du2.flush()
    url_Ji=url_Du2.read()
    JiCi+=1
    #打开链接
    url=quote(url,'\/:?=;@&+$,%.#\n')
    Request1=request.Request(url,headers=header1)
#     try:
    DaKai_url=request.urlopen(Request1)
    if DaKai_url.getcode()!=200:
        print(str(JiCi)+"|打开链接"+url+"失败！略过此链接！")
        continue
    else:
        print(str(JiCi)+"|打开链接"+url+"成功！")
    BeautifulSoup1=BeautifulSoup(DaKai_url,"html.parser",from_encoding="utf-8")
    #提取链接
    if re.search(r"DirectLink.direct",url)!=None:
        pmbh=re.findall(r"sp=S?(\w+)&",url)[1]
        url2="http://www.hngp.gov.cn/wsscnew/egp/jy/xyghjy/xyghxm/xyghzy/xzsp/XyspList.html?pmbh="+pmbh+"&cgsl=0&cgje=0.0&ppbh=null&lastcgsl=0&lastcgje=0.0&xmxh=null&xyghbh=null&isnwwbz=ww&area=00390019&czy=null&lbbs=null"
        url2=quote(url2,'\/:?=;@&+$,%.#\n')
        Request2=request.Request(url=url2,headers=header1)
        DaKai_url2=request.urlopen(Request2)
        BeautifulSoup2=BeautifulSoup(DaKai_url2,"html.parser",from_encoding="utf-8")
        BeautifulSoup2=BeautifulSoup2.find("div",class_="sc_list")
        LianJieJi=BeautifulSoup2.find_all("a",href=re.compile(r"(\S+\s?)+"))
        LianJieChuli(LianJieJi,url_Ji)
    elif re.search(r"DirectLink_4.direct",url)!=None:
        xhbh=re.findall(r"sp=S?(\w+)&",url)[0]
        url2="http://www.hngp.gov.cn/wsscnew/egp/public/gg_spzsxx/SpxhMainTab.html?xhbh="+xhbh+"&xmxh=null&area=00390019&xyghbh=ff80808151561b4701517a41b243602e&lastcgsl=0&cgje=0.0&lastcgje=0.0&cgsl=0&isnwwbz=ww&czy=null&lbbs=null"
        url2=quote(url2,'\/:?=;@&+$,%.#\n')
        Request2=request.Request(url=url2,headers=header1)
        DaKai_url2=request.urlopen(Request2)
        BeautifulSoup2=BeautifulSoup(DaKai_url2,"html.parser",from_encoding="utf-8")
        ShuJv(BeautifulSoup2,xhbh)
    else:
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
    # if JiCi>=50:
        # break
url_Xie.close()
url_Du.close()
url_Du2.close()
WenJian.close()