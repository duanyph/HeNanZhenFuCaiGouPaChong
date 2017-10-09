import sqlite3
import csv
WenJian=open("数据集.csv","w",encoding='gbk',newline='')
xie=csv.writer(WenJian,dialect="excel")
xie.writerow(["品目","品种","商品","最低价报价供货商","最低价报价","史泰博报价","史泰博是否最低价"])
WenJian.close()
WenJian=open("数据集.csv","a+",encoding='gbk',newline='')
xie=csv.writer(WenJian,dialect="excel")
ShuJvKu=sqlite3.connect("ShuJvJi.db")
YouBiao=ShuJvKu.cursor()
YouBiao.execute("select 品目,品种,商品,供货商,报价 from ShuJvJi")
JiCi=0
ZuiDi=YouBiao.fetchone()
ShiTaiBo=None
while 1:
    JiCi+=1
    ShanPing=YouBiao.fetchone()
    if ZuiDi==None or ShanPing==None:
        break
    if ZuiDi[3]=="史泰博（上海）有限公司":
        ShiTaiBo=ZuiDi
    elif ShanPing[3]=="史泰博（上海）有限公司":
        ShiTaiBo=ShanPing
    if ZuiDi[2]==ShanPing[2]:
        if ZuiDi[4]>ShanPing[4]:
            ZuiDi=ShanPing
    else:
        ShuChu=list(ZuiDi)
        if ShiTaiBo==None:
            DuiBi="无"
            ShuChu.append("无")
        elif ZuiDi[4]>=ShiTaiBo[4]:
            DuiBi="是"
            ShuChu.append(ShiTaiBo[4])
        else:
            DuiBi="否"
            ShuChu.append(ShiTaiBo[4])
        ShuChu.append(DuiBi)
        xie.writerow(ShuChu)
        WenJian.flush()
        print(str(JiCi)+"|写出数据：",end="")
        print(ShuChu)
        ZuiDi=ShanPing
WenJian.flush()
WenJian.close()
ShuJvKu.close()