#coding:utf-8
from urllib import request,parse
from urllib.parse import quote
from bs4 import BeautifulSoup
import sqlite3,re,socket,time
socket.setdefaulttimeout(10)
RiZhi=open("ShuJv_RiZhi.log","w+")
RiZhi.close()
header1={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0",
        "Cookie":open("Cookie.txt","r").read()}
JiCi=0
URL_ShuJvKu=sqlite3.connect("ShuJvJi.db")
YouBiao=URL_ShuJvKu.cursor()
try:
    YouBiao.execute("drop table ShuJvJi")
except:
    pass
YouBiao.execute("""
CREATE TABLE ShuJvJi (
    ID INTEGER PRIMARY KEY,
    品目 TEXT,
    品牌 TEXT,
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
def ShuJv(BeautifulSoup1,xhbh,xyghbh):
    ShangPingXingXi=BeautifulSoup1.find("div",class_="sc_wz").get_text()
    ShangPingXingXi=re.findall(r"\-([^\-]+)",ShangPingXingXi)
    PingMu=ShangPingXingXi[0]
    PinPai=ShangPingXingXi[1]
    ShangPing=BeautifulSoup1.find("div",class_="sc_pro_m").find("h1").get_text()
    BeautifulSoup2=XiangQingBiao(xhbh,xyghbh)
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
        print("采集数据:",PingMu,PinPai,ShangPing,FenShu,GongHuo,FuWu,BaoJia,LianXiRen,ShouJi,DianHua,GengXinShiJian)
        YouBiao.execute("insert into ShuJvJi (品目,品牌,商品,得分,供货商,服务承诺,报价,联系人,移动电话,办公电话,更新时间) values('"+PingMu+"','"+PinPai+"','"+ShangPing+"','"+FenShu+"','"+GongHuo+"','"+FuWu+"','"+BaoJia+"','"+LianXiRen+"','"+ShouJi+"','"+DianHua+"','"+GengXinShiJian+"')")
        URL_ShuJvKu.commit()
#商品列表处理
def XiangQingBiao(xhbh,xyghbh):
    QingQiu="http://www.hngp.gov.cn/wsscnew/egp/public/gg_spzsxx/SpxhMainTab,form.sdirect"
    POST_Tou={"formids":"If,sl,jbcsPage,ghsPage,jgqsPage,picPage,spxqPage,Xzsp,Gwc,Xmxx,Dzdd,Ddys,selgys",
            "If":"F",
            "xhbh":xhbh,
            "xyghbh":xyghbh,
            "ghsPage":"供货商",
    }
    POST_Tou=parse.urlencode(POST_Tou).encode(encoding='UTF8')
    Request1=request.Request(url=QingQiu,headers=header1,data=POST_Tou)
    try:
        XiangYing=request.urlopen(Request1)
    except:
        try:
            XiangYing=request.urlopen(Request1)
        except:
            print("POST包响应超时！略过此POST包！")
            RiZhiChuLi(2,url,xhbh,xyghbh,url2)
            return None
    BeautifulSoup1=BeautifulSoup(XiangYing,"html.parser",from_encoding="utf-8")
    return BeautifulSoup1
#错误日志处理
def RiZhiChuLi(CuoWuMa,url=None,xhbh=None,xyghbh=None,url2=None):
    RiZhi=open("ShuJv_RiZhi.log","a+")
    RiZhi.write(str(CuoWuMa)+"|"+str(JiCi)+"|"+url+"|"+xhbh+"|"+xyghbh+"|"+url2+"\n")
    RiZhi.close()
while 1:
    JiCi+=1
    YouBiao.execute("select URL from URL_Ji2 where ID="+str(JiCi))
    url=YouBiao.fetchone()
    if url!=None:
        url=url[0]
    else:
        break
    try:
        if re.search(r"DirectLink_4.sdirect",url)!=None:
            xhbh=re.findall(r"sp=S?(\w+)&",url)[0]
            xyghbh=re.findall(r"sp=S?(\w+)&",url)[2]
            url2="http://www.hngp.gov.cn/wsscnew/egp/public/gg_spzsxx/SpxhMainTab.html?xhbh="+xhbh+"&xmxh=null&area=00390019&xyghbh="+xyghbh+"&lastcgsl=0&cgje=0.0&lastcgje=0.0&cgsl=0&isnwwbz=ww&czy=null&lbbs=null"
            url2=quote(url2,'\/:?=;@&+$,%.#\n')
            Request1=request.Request(url=url2,headers=header1)
            try:
                DaKai_url2=request.urlopen(Request1)
            except:
                try:
                    DaKai_url2=request.urlopen(Request1)
                except:
                    print("打开链接"+url2+"超时！略过此链接！")
                    RiZhiChuLi(1,url,xhbh,xyghbh,url2)
                    continue
            print(str(JiCi)+"|打开链接："+url2)
            BeautifulSoup2=BeautifulSoup(DaKai_url2,"html.parser",from_encoding="utf-8")
            ShuJv(BeautifulSoup2,xhbh,xyghbh)
        time.sleep(0.1)
    except KeyboardInterrupt:
        print("终止运行！")
        break
    except :
        RiZhiChuLi(3,url,xhbh,xyghbh,url2)
        print("|打开链接"+url2+"异常！略过此链接！")
        continue
URL_ShuJvKu.commit()
URL_ShuJvKu.close()
