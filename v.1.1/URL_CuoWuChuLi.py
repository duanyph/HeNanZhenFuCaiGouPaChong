import socket,sqlite3,re
from urllib import request,parse
from urllib.parse import quote
from bs4 import BeautifulSoup
socket.setdefaulttimeout(10)
URL_ShuJvKu=sqlite3.connect("ShuJvJi.db")
YouBiao=URL_ShuJvKu.cursor()
CuoWuRiZhi=open("URL_RiZhi.log","r")
HouZui=["mp3","mp4","txt","pdf","fiv","doc","png","img","jpg","jpeg","bmp","tmp"]
ZhenZeHouZhui=r"(."+r"|.".join(HouZui)+r")$"
header1={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0"}
def RiZhiChuLi(CuoWuMa,url="",pmbh="",url2="",JiCi1=""):
    RiZhiWenJian=open("URL_RiZhi.log","a+")
    RiZhiWenJian.write(str(CuoWuMa)+"|"+"0"+"|"+url+"|"+pmbh+"|"+url2+"|"+str(JiCi1)+"\n")
    RiZhiWenJian.close()
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
            print("采集链接："+LianJie)
        else:
            del(LianJie)
            print("重复链接，略过！")
            continue
    URL_ShuJvKu.commit()
#列表页处理
def POST_Biao(JiCi1):
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
    POST_Tou=parse.urlencode(POST_Tou).encode(encoding='UTF-8')
    Request3=request.Request(url=QingQiu,headers=header1,data=POST_Tou)
    try:
        DaKai_QingQiu=request.urlopen(Request3)
    except :
        try:
            DaKai_QingQiu=request.urlopen(Request3)
        except :
            print("打开链接"+URL+"超时！略过此链接！")
            RiZhiChuLi(3,URL,pmbh,"",JiCi1)
            return
    BeautifulSoup2=BeautifulSoup(DaKai_QingQiu,"html.parser",from_encoding="utf-8")
    BeautifulSoup2=BeautifulSoup2.find("div",class_="sc_list")
    LianJieJi=BeautifulSoup2.find_all("a",href=re.compile(r"(\S+\s?)+"))
    LianJieChuli(LianJieJi)
for RiZhi in CuoWuRiZhi:
    CuoWuMa=re.findall(r"(\d)\|",RiZhi)[0]
    pmbh=re.findall(r"\|(\w+)\|",RiZhi)[1]
    try:
        if CuoWuMa=="2":
            URL=re.findall(r"http://www.hngp.gov.cn/wsscnew/egp/jy/xyghjy/xyghxm/xyghzy/xzsp/XyspList.html(\S+)\|",RiZhi)[0]
            URL="http://www.hngp.gov.cn/wsscnew/egp/jy/xyghjy/xyghxm/xyghzy/xzsp/XyspList.html"+URL
            URL=quote(URL,'\/:?=;@&+$,%.#\n')
            Request1=request.Request(URL,headers=header1)
            try:
                DaKai_url=request.urlopen(Request1)
            except :
                try:
                    DaKai_url=request.urlopen(Request1)
                except :
                    print("打开链接"+url+"超时！略过此链接！")
                    RiZhiChuLi(2,url,pmbh,"","")
                continue
            print("打开链接"+URL)
            BeautifulSoup1=BeautifulSoup(DaKai_url,"html.parser",from_encoding="utf-8")
            # 列表页处理
            YeShu=BeautifulSoup1.find("span",style="float:right").get_text()
            YeShu=re.findall(r"共(\d+)页",YeShu)[0]
            QingQiu="http://www.hngp.gov.cn/wsscnew/egp/jy/xyghjy/xyghxm/xyghzy/xzsp/XyspList,form.direct"
            for JiCi1 in range(int(YeShu)):
                JiCi1+=1
                POST_Biao(JiCi1)
        elif CuoWuMa=="3":
            JiCi1=re.findall(r"(\d+)$",RiZhi)[0]
            POST_Biao(JiCi1)
    except KeyboardInterrupt:
        print("终止运行！")
        break
    except :
        RiZhiChuLi(4,URL,pmbh,"",JiCi1)
        print("|打开链接"+URL+"出现异常！略过此链接！")
        continue