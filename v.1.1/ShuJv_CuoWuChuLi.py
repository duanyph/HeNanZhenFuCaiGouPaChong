#coding:utf-8
from urllib import request,parse
from urllib.parse import quote
from bs4 import BeautifulSoup
import sqlite3,re,socket
socket.setdefaulttimeout(10)
RiZhi=open("ShuJv_RiZhi.log","w")
RiZhi.close()
header1={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0"}
JiCi=0
ShuJvKu=sqlite3.connect("ShuJvJi.db")
YouBiao=ShuJvKu.cursor()
URL_ShuJvKu=sqlite3.connect("URL_Ji.db")
YouBiao2=URL_ShuJvKu.cursor()
#数据提取
def ShuJv(BeautifulSoup1,xhbh):
    ShangPingXingXi=BeautifulSoup1.find("div",class_="sc_wz").get_text()
    ShangPingXingXi=re.findall(r"\-(\w+)\-(\w+)",ShangPingXingXi)
    PingZhong=ShangPingXingXi[0][0]
    PingMu=ShangPingXingXi[0][1]
    ShangPing=BeautifulSoup1.find("div",class_="sc_pro_m").find("h1").get_text()
    BeautifulSoup2=XiangQingBiao(xhbh)
    if BeautifulSoup2==None:
        return
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
        YouBiao.execute("insert into ShuJvJi (品种,品目,商品,得分,供货商,服务承诺,报价,联系人,移动电话,办公电话,更新时间) values('"+PingZhong+"','"+PingMu+"','"+ShangPing+"','"+FenShu+"','"+GongHuo+"','"+FuWu+"','"+BaoJia+"','"+LianXiRen+"','"+ShouJi+"','"+DianHua+"','"+GengXinShiJian+"')")
        print("采集数据:",PingZhong,PingMu,ShangPing,FenShu,GongHuo,FuWu,BaoJia,LianXiRen,ShouJi,DianHua,GengXinShiJian)
        ShuJvKu.commit()
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
    try:
        XiangYing=request.urlopen(Request1,timeout=5)
    except:
        try:
            XiangYing=request.urlopen(Request1,timeout=5)
        except:
            print("POST包响应超时！略过此POST包！")
            RiZhiChuLi(2,url,xhbh,url2)
            return None
    BeautifulSoup1=BeautifulSoup(XiangYing,"html.parser",from_encoding="utf-8")
    return BeautifulSoup1
#错误日志处理
def RiZhiChuLi(CuoWuMa,url=None,xhbh=None,url2=None):
    RiZhi=open("ShuJv_RiZhi.log","a+")
    RiZhi.write(str(CuoWuMa)+"|"+str(JiCi)+"|"+url+"|"+xhbh+"|"+url2+"\n")
    RiZhi.close()
while 1:
    JiCi+=1
    YouBiao2.execute("select URL from URL_Ji where ID="+str(JiCi))
    url=YouBiao2.fetchone()
    if url!=None:
        url=url[0]
    else:
        break
    try:
        if re.search(r"DirectLink_4.direct",url)!=None:
            xhbh=re.findall(r"sp=S?(\w+)&",url)[0]
            url2="http://www.hngp.gov.cn/wsscnew/egp/public/gg_spzsxx/SpxhMainTab.html?xhbh="+xhbh+"&xmxh=null&area=00390019&lastcgsl=0&cgje=0.0&lastcgje=0.0&cgsl=0&isnwwbz=ww&czy=null&lbbs=null"
            url2=quote(url2,'\/:?=;@&+$,%.#\n')
            Request1=request.Request(url=url2,headers=header1)
            try:
                DaKai_url2=request.urlopen(Request1,timeout=5)
            except:
                try:
                    DaKai_url2=request.urlopen(Request1,timeout=5)
                except:
                    print("打开链接"+url2+"超时！略过此链接！")
                    RiZhiChuLi(1,url,xhbh,url2)
                    continue
            print(str(JiCi)+"|打开链接："+url2)
            BeautifulSoup2=BeautifulSoup(DaKai_url2,"html.parser",from_encoding="utf-8")
            ShuJv(BeautifulSoup2,xhbh)
    except KeyboardInterrupt:
        print("终止运行！")
        break
    except :
        RiZhiChuLi(3,url,xhbh,url2)
        print("|打开链接"+url2+"异常！略过此链接！")
        continue
ShuJvKu.commit()
ShuJvKu.close()
URL_ShuJvKu.close()