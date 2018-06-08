#coding:utf-8
from urllib import request,parse
from urllib.parse import quote
from bs4 import BeautifulSoup
import sqlite3,re,socket,time
socket.setdefaulttimeout(10)
RiZhi=open("ShuJvRiZhi.log","r+")
RiZhi.readline()
header1={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0",
        # "Cookie":open("Cookie.txt","r").read()
        }
URL_ShuJvKu=sqlite3.connect("ShuJvJi.db")
YouBiao=URL_ShuJvKu.cursor()
#数据提取
def ShuJv(BeautifulSoup1):
    FenLei=BeautifulSoup1.find_all("a",class_="crumbs-title")
    PingMu=re.findall("\S+",FenLei[0].get_text())[0]
    PinPai=re.findall("\S+",FenLei[1].get_text())[0]
    ShangPing=BeautifulSoup1.find("span",class_="last").get_text()[1:]
    #供货商列表处理
    tr_Ji=BeautifulSoup1.find("tbody").find_all("tr")
    tr_Ji=tr_Ji[1:]
    for tr in tr_Ji:
        td_Ji=tr.find_all("td")
        print("采集数据:",ShangPing)
        YouBiao.execute("insert into ShuJvJi (品目,品牌,商品,综合评价,电商名称,服务承诺,授权信息,商品报价,配件信息,联系人,移动电话,上架时间,价格更新时间) values('"+PingMu+"','"+PinPai+"','"+ShangPing+"','"+td_Ji[0].get_text()+"','"+td_Ji[1].get_text()[2:-2]+"','"+td_Ji[2].get_text()+"','"+td_Ji[3].get_text()+"','"+td_Ji[4].get_text()+"','"+td_Ji[5].get_text()+"','"+td_Ji[6].get_text()+"','"+td_Ji[7].get_text()+"','"+td_Ji[8].get_text()+"','"+td_Ji[9].get_text()+"')")
        URL_ShuJvKu.commit()
for DuHang in RiZhi.readlines():
    try:
        url=DuHang.split("|")[1]
        Request1=request.Request(url=url,headers=header1)
        try:
            DaKai_url=request.urlopen(Request1)
        except:
            try:
                DaKai_url=request.urlopen(Request1)
            except:
                print("打开链接"+url+"超时，略过！")
                continue
        print("打开链接："+url)
        BeautifulSoup2=BeautifulSoup(DaKai_url,"html.parser",from_encoding="utf-8")
        ShuJv(BeautifulSoup2)
        time.sleep(0.2)
    except:
        print("打开链接"+url+"异常，略过！")
RiZhi.close()
URL_ShuJvKu.commit()
URL_ShuJvKu.close()