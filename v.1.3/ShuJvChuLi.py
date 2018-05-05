#coding:utf-8
from urllib import request,parse
from urllib.parse import quote
from bs4 import BeautifulSoup
import sqlite3,re,socket,time
socket.setdefaulttimeout(10)
RiZhi=open("ShuJv_RiZhi.log","w+")
RiZhi.write("错误码|错误链接\n")
RiZhi.close()
header1={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0",
        # "Cookie":open("Cookie.txt","r").read()
        }
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
        综合评价 TEXT,
        电商名称 TEXT,
        服务承诺 TEXT,
        授权信息 TEXT,
        商品报价 TEXT,
        配件信息 TEXT,
        联系人 TEXT,
        移动电话 TEXT,
        上架时间 TEXT,
        价格更新时间 TEXT)
    """)
URL_ShuJvKu.commit()
#数据提取
def ShuJv(BeautifulSoup1):
    FenLei=BeautifulSoup1.find_all("a",class_="crumbs-title")
    PingMu=re.findall("\S+",FenLei[0].get_text())[0]
    PinPai=re.findall("\S+",FenLei[1].get_text())[0]
    ShangPin=BeautifulSoup1.find("span",class_="last").get_text()[1:]
    #供货商列表处理
    tr_Ji=BeautifulSoup1.find("tbody").find_all("tr")
    tr_Ji=tr_Ji[1:]
    for tr in tr_Ji:
        td_Ji=tr.find_all("td")
        print("采集数据:",ShangPin)
        YouBiao.execute("insert into ShuJvJi (品目,品牌,商品,综合评价,电商名称,服务承诺,授权信息,商品报价,配件信息,联系人,移动电话,上架时间,价格更新时间) values('"+PingMu+"','"+PinPai+"','"+ShangPin+"','"+td_Ji[0].get_text()+"','"+td_Ji[1].get_text()[2:-2]+"','"+td_Ji[2].get_text()+"','"+td_Ji[3].get_text()+"','"+td_Ji[4].get_text()+"','"+td_Ji[5].get_text()+"','"+td_Ji[6].get_text()+"','"+td_Ji[7].get_text()+"','"+td_Ji[8].get_text()+"','"+td_Ji[9].get_text()+"')")
        URL_ShuJvKu.commit() 
#错误日志处理
def RiZhiChuLi(CuoWuMa,url="None"):
    RiZhi=open("ShuJv_RiZhi.log","a+")
    RiZhi.write(str(CuoWuMa)+"|"+url+"\n")
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
        Request1=request.Request(url=url,headers=header1)
        try:
            DaKai_url=request.urlopen(Request1)
        except:
            try:
                DaKai_url=request.urlopen(Request1)
            except:
                print(str(JiCi)+"|打开链接"+url+"超时，略过！")
                RiZhiChuLi(1,url)
                continue
        print(str(JiCi)+"|打开链接："+url)
        BeautifulSoup2=BeautifulSoup(DaKai_url,"html.parser",from_encoding="utf-8")
        ShuJv(BeautifulSoup2)
        time.sleep(0.2)
    except KeyboardInterrupt:
        print("终止运行！")
        break
    except :
        RiZhiChuLi(2,url)
        print(str(JiCi)+"|打开链接"+url+"异常，已记录到日志！")
        continue
URL_ShuJvKu.commit()
URL_ShuJvKu.close()