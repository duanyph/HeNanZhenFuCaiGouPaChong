from urllib import request
from bs4 import BeautifulSoup
from urllib import parse
import re
QingQiu="http://www.hngp.gov.cn/wsscnew/egp/public/gg_spzsxx/SpxhMainTab,form.direct"
QingQiuTou={
"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:55.0) Gecko/20100101 Firefox/55.0",
}
POST_tou={
"formids":"If,sl,jbcsPage,ghsPage,jgqsPage,picPage,spxqPage,Xzsp,Gwc,Xmxx,Dzdd,Ddys,selgys",
"If":"F",
"xhbh":"ff8080815c04a864015cb548971f6b90",
"area":"00390019",
"ghsPage":"供货商",
}
POST_tou=parse.urlencode(POST_tou).encode(encoding='UTF8')
Request2=request.Request(url=QingQiu,headers=QingQiuTou,data=POST_tou)
XiangYing=request.urlopen(Request2)
BeautifulSoup2=BeautifulSoup(XiangYing,"html.parser",from_encoding="utf-8")
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
    DianHua=JiLu[7].get_text()
    GengXinShiJian=JiLu[8].get_text()
    print(FenShu,GongHuo,FuWu,BaoJia,LianXiRen,ShouJi,DianHua,GengXinShiJian)