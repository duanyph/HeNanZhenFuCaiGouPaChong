#coding:utf-8
from urllib import request
from bs4 import BeautifulSoup
from urllib.parse import quote
from urllib import parse
import csv
import time
import re
header1={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0"}
url_Du=open("url_ji.txt","r")
WenJian=open("数据集.csv","w",encoding='gbk',newline='')
xie=csv.writer(WenJian,dialect="excel")
xie.writerow(["商品","得分","供货商","服务承诺","报价","联系人","移动电话","办公电话","更新时间"])
WenJian.close()
WenJian=open("数据集.csv","a+",encoding='gbk',newline='')
xie=csv.writer(WenJian,dialect="excel")
JiCi=0
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
        FuWu=re.findall(r"\w*",JiLu[3].get_text())[0]
        BaoJia=JiLu[4].get_text()
        LianXiRen=JiLu[5].get_text()
        ShouJi=JiLu[6].get_text()
        DianHua=re.findall(r"\w*",JiLu[7].get_text())[0]
        GengXinShiJian=JiLu[8].get_text()
        print("采集数据:",ShangPing,FenShu,GongHuo,FuWu,BaoJia,LianXiRen,ShouJi,DianHua,GengXinShiJian)
        xie.writerow([ShangPing,FenShu,GongHuo,FuWu,BaoJia,LianXiRen,ShouJi,DianHua,GengXinShiJian])
        WenJian.flush()
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
for url in url_Du:
    JiCi+=1
    try:
        url=quote(url,'\/:?=;@&+$,%.#\n')
        Request1=request.Request(url,headers=header1)
        if re.search(r"DirectLink_4.direct",url)!=None:
            xhbh=re.findall(r"sp=S?(\w+)&",url)[0]
            url2="http://www.hngp.gov.cn/wsscnew/egp/public/gg_spzsxx/SpxhMainTab.html?xhbh="+xhbh+"&xmxh=null&area=00390019&xyghbh=ff80808151561b4701517a41b243602e&lastcgsl=0&cgje=0.0&lastcgje=0.0&cgsl=0&isnwwbz=ww&czy=null&lbbs=null"
            url2=quote(url2,'\/:?=;@&+$,%.#\n')
            Request3=request.Request(url=url2,headers=header1)
            DaKai_url2=request.urlopen(Request3)
            if DaKai_url2.getcode()!=200:
                print(str(JiCi)+"|打开链接"+url2+"失败！略过此链接！")
                continue
            else:
                print(str(JiCi)+"|打开链接"+url2+"成功！")
            BeautifulSoup2=BeautifulSoup(DaKai_url2,"html.parser",from_encoding="utf-8")
            ShuJv(BeautifulSoup2,xhbh)
    except KeyboardInterrupt:
        print("终止运行！")
        break
    except :
        print("|打开链接"+url2+"出现异常！略过此链接！")
        # break
        continue
url_Du.close()
WenJian.close()
