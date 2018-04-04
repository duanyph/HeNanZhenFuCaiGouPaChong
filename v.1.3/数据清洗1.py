import sqlite3,csv,re
JiCi=0
WenJian=open("数据集.csv","w",encoding='gbk',newline='')
xie=csv.writer(WenJian,dialect="excel")
xie.writerow(["品目","品牌","商品","最低价报价供货商","最低价报价","更新时间","史泰博报价","史泰博是否最低价"])
WenJian.close()
WenJian=open("数据集.csv","a+",encoding='gbk',newline='')
xie=csv.writer(WenJian,dialect="excel")
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
    ShiTaiBo="空"
    JiCi+=1
    YouBiao.execute("select 品目,品牌,商品,供货商,报价,更新时间 from ShuJvJi where 品目='"+ShanPing[0]+"' and 品牌='"+ShanPing[1]+"' and 商品='"+ShanPing[2]+"'")
    ShangPingJi2=YouBiao.fetchall()
    DuiBi=ShangPingJi2[0]
    # if DuiBi[3]=="史泰博（上海）有限公司":
    #     ShiTaiBo=DuiBi[4]
    for a in range(len(ShangPingJi2)-1):
        a+=1
        # if ShangPingJi2[a][3]=="史泰博（上海）有限公司":
        #     ShiTaiBo=ShangPingJi2[a][4]
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
    xie.writerow(ShuChu)
    WenJian.flush()
    print(str(JiCi)+"|写出数据：",end="")
    print(ShuChu)
WenJian.flush()
WenJian.close()
ShuJvKu.close()