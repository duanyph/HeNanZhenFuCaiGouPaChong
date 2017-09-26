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
    YouBiao.execute("drop table URL_Ji")
except:
    pass
YouBiao.execute("CREATE TABLE URL_Ji (ID INTEGER PRIMARY KEY,URL TEXT)")
YouBiao.execute("insert into URL_Ji (URL) values('"+url_QiShi+"')")
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
        if re.search(r"http://www.hngp.gov.cn/wsscnew|https://www.hngp.gov.cn/wsscnew", LianJie,re.M|re.I)==None:
            del(LianJie)
            continue
        #链接去重
        YouBiao.execute("select URl from URL_Ji where URL='"+LianJie+"'")
        if YouBiao.fetchone()==None:
            YouBiao.execute("insert into URL_Ji (URL) values ('"+LianJie+"')")
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
    YouBiao.execute("select URL from URL_Ji where ID="+str(JiCi))
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
        #提取链接和数据
        if re.search(r"DirectLink.direct",url)!=None:
            pmbh=re.findall(r"sp=S?(\w+)&",url)[1]
            url2="http://www.hngp.gov.cn/wsscnew/egp/jy/xyghjy/xyghxm/xyghzy/xzsp/XyspList.html?pmbh="+pmbh+"&cgsl=0&cgje=0.0&ppbh=null&lastcgsl=0&lastcgje=0.0&xmxh=null&xyghbh=null&isnwwbz=ww&area=00390019&czy=null&lbbs=null"
            url2=quote(url2,'\/:?=;@&+$,%.#\n')
            Request2=request.Request(url=url2,headers=header1)
            try:
                DaKai_url2=request.urlopen(Request2)
            except :
                try:
                    DaKai_url2=request.urlopen(Request2)
                except :
                    print("打开链接"+url+"超时！略过此链接！")
                    RiZhiChuLi(2,url,pmbh,url2,JiCi1)
                    continue
            BeautifulSoup2=BeautifulSoup(DaKai_url2,"html.parser",from_encoding="utf-8")
            #列表页处理
            YeShu=BeautifulSoup2.find("span",style="float:right").get_text()
            YeShu=re.findall(r"共(\d+)页",YeShu)[0]
            QingQiu="http://www.hngp.gov.cn/wsscnew/egp/jy/xyghjy/xyghxm/xyghzy/xzsp/XyspList,form.direct"
            for JiCi1 in range(int(YeShu)):
                JiCi1+=1
                POST_Tou={
                "formids":"gysmcword,skeyword,AddGwc,search,change,jgqj_1,jgqj_2,jgqj_3,jgqj_4,jgqj_5,jgqj_6,xltj,jgtj,sjsjtj,ghslb_qb,ghslb_ds,ghslb_gys",
                "area":"00390019",
                "lastcgje":"0.0",
                "pmbh":pmbh,
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
                        continue
                BeautifulSoup3=BeautifulSoup(DaKai_QingQiu,"html.parser",from_encoding="utf-8")
                BeautifulSoup3=BeautifulSoup3.find("div",class_="sc_list")
                LianJieJi=BeautifulSoup3.find_all("a",href=re.compile(r"(\S+\s?)+"))
                LianJieChuli(LianJieJi)
        else:
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
