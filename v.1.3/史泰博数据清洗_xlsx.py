import sqlite3,re
from openpyxl import *
JiCi=0
WenJian=Workbook()
Biao=WenJian.active
Biao.append(["品目","品牌","商品","最低价报价供货商","最低价报价","更新时间","史泰博报价","史泰博是否最低价"])
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
for ShanPing in ShangPingJi:
    try:
        ShiTaiBo="空"
        JiCi+=1
        YouBiao.execute("select 品目,品牌,商品,电商名称,商品报价,价格更新时间 from ShuJvJi where 品目='"+ShanPing[0]+"' and 品牌='"+ShanPing[1]+"' and 商品='"+ShanPing[2]+"'")
        ShangPingJi2=YouBiao.fetchall()
        DuiBi=ShangPingJi2[0]
        for a in range(len(ShangPingJi2)-1):
            a+=1
            if ZuHe(DuiBi[4])>ZuHe(ShangPingJi2[a][4]):
                DuiBi=ShangPingJi2[a]
        for b in ShangPingJi2:
            if b[3]=="史泰博（上海）有限公司":
                ShiTaiBo=b[4]
        ShuChu=list(DuiBi)
        ShuChu.append(ShiTaiBo)
        if DuiBi[4]==ShiTaiBo:
            ZuiDi="是"
        elif DuiBi[4]<ShiTaiBo:
            ZuiDi="否"
        else:
            ZuiDi="空"
        ShuChu.append(ZuiDi)
        Biao.append(ShuChu)
        print(str(JiCi)+"|写出数据："+DuiBi[2])
    except:
        pass
WenJian.save("数据集.xlsx")
ShuJvKu.close()