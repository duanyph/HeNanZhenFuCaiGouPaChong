import sqlite3,re,time
from openpyxl import *
GongHuoShang=["河南领先未来电子商务有限公司","河南买卖多电子商务有限公司","欧菲斯办公伙伴控股有限公司","郑州网航科技有限公司","上海晨光科力普办公用品有限公司","河南知春商贸有限公司","史泰博（上海）有限公司","河南融纳电子商务有限公司","深圳齐心集团股份有限公司","河南一线达通网络科技有限公司","河南汇众益丰电子商务有限公司"]
NianYueRi=time.strftime('%Y-%m-%d',time.localtime(time.time()))
ShuJvKu=sqlite3.connect("ShuJvJi.db")
YouBiao=ShuJvKu.cursor()
YouBiao.execute("select distinct 品目,品牌,商品 from ShuJvJi")
ShangPingJi=YouBiao.fetchall()
ShangPingJi=set(ShangPingJi)
def ZuHe(JiaGe):
    ZiFu=re.findall("([^￥^,^.]+)",JiaGe)
    LinShi=""
    for c in ZiFu:
        LinShi=LinShi+c
    return int(LinShi)
for DiangShang in GongHuoShang:
    JiCi=0
    WenJian=Workbook()
    Biao=WenJian.active
    Biao.append(["品目","品牌","商品","最低价报价供货商","最低价报价","更新时间","报价","是否最低价"])
    for ShanPing in ShangPingJi:
        try:
            DiangShang2="空"
            JiCi+=1
            YouBiao.execute("select 品目,品牌,商品,电商名称,商品报价,价格更新时间 from ShuJvJi where 品目='"+ShanPing[0]+"' and 品牌='"+ShanPing[1]+"' and 商品='"+ShanPing[2]+"'")
            ShangPingJi2=YouBiao.fetchall()
            DuiBi=ShangPingJi2[0]
            for a in range(len(ShangPingJi2)-1):
                a+=1
                if ZuHe(DuiBi[4])>ZuHe(ShangPingJi2[a][4]):
                    DuiBi=ShangPingJi2[a]
            for b in ShangPingJi2:
                if b[3]==DiangShang:
                    DiangShang2=b[4]
            ShuChu=list(DuiBi)
            ShuChu.append(DiangShang2)
            if DuiBi[4]==DiangShang2:
                ZuiDi="是"
            elif DuiBi[4]<DiangShang2:
                ZuiDi="否"
            else:
                ZuiDi="空"
            ShuChu.append(ZuiDi)
            Biao.append(ShuChu)
            print(str(JiCi)+"|写出数据："+DuiBi[2])
        except:
            pass
    WenJian.save("数据集/"+DiangShang+NianYueRi+".xlsx")
ShuJvKu.close()