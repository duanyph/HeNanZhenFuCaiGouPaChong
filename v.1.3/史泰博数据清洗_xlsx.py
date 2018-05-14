import sqlite3,re
from openpyxl import *
JiCi=0
WenJian=Workbook()
Biao=WenJian.active
Biao.append(["分类","一级品目","二级品目","品牌","商品","最低价报价供货商","最低价报价","更新时间","史泰博报价","史泰博是否最低价"])
ShuJvKu=sqlite3.connect("ShuJvJi.db")
YouBiao=ShuJvKu.cursor()
YouBiao.execute("select distinct 品目,品牌,商品 from ShuJvJi")
ShangPingJi=YouBiao.fetchall()
ShangPingJi=set(ShangPingJi)
def WeiZhi(PingMu):
    LieBiao={"计算机设备":
        {"计算机":{1:"台式计算机",2:"笔记本计算机",3:"平板电脑",4:"服务器",5:"工作站",6:"一体机"},
        "显示设备":{1:"液晶显示器",2:"等离子显示器"},
        "打印设备":{1:"喷墨打印机",2:"激光打印机",3:"针式打印机",4:"打印机配件"},
        "网络设备":{1:"路由器",2:"交换机",3:"负载均衡设备",4:"UPS电源",5:"UPS电池",6:"机柜"},
        "信息安全设备":{1:"防火墙",2:"入侵检测/防御设备",3:"漏洞扫描设备",4:"容灾备份设备",5:"网络隔离设备",6:"安全审计设备",7:"网上行为管理设备",8:"VPN设备"},
        "存储设备":{1:"磁盘阵列",2:"磁盘机"},
        "配件":{1:"显示器支架",2:"隔离卡",3:"U盘",4:"键盘/鼠标",5:"内存条",6:"光盘",7:"移动硬盘",8:"硬盘盒",9:"手写板",10:"转接口",11:"数据线",12:"排插",13:"网卡"},},
    "办公设备":
        {"传真/通讯":{1:"传真机",2:"电话机",3:"其他通信设备及配件"},
        "复印设备":{1:"多功能一体机",2:"复印机",3:"复合机",4:"复印机配件"},
        "扫描/投影":{1:"扫描仪",2:"投影仪",3:"电子白板",4:"高拍仪",5:"幕布",6:"扫描/投影配件"},
        "LED显示屏":{1:"LED显示屏"},
        "触控一体机":{1:"触控一体机"},
        "碎纸机":{1:"碎纸机"},
        "点/验钞机（点/验钞/收款机）":{1:"点钞机 验钞笔/机"},
        "文印设备":{1:"速印机",2:"装订机"},
        "摄影/摄像及配件":{1:"摄像机",2:"照相机",3:"记录仪",4:"镜头及配件"},},
    "电器设备":
        {"电视机":{1:"液晶电视机",2:"等离子电视机"},
        "空调":{1:"壁挂式空调",2:"柜式空调"},
        "其他电器":{1:"电冰箱",2:"冷藏柜",3:"风扇",4:"取暖器",5:"洗衣机",6:"吸尘器",7:"洗碗机",8:"饮水机",9:"电热水器",10:"加湿器",11:"空气净化设备"},},
    "办公家具":
        {"家具用具":{1:"桌/椅/柜套装",2:"床类",3:"台/桌类",4:"椅凳类",5:"沙发类",6:"柜类",7:"架类",8:"屏风类"},},
    "办公用品":
        {"笔":{1:"中性笔",2:"圆珠笔",3:"荧光笔",4:"记号笔",5:"铅笔",6:"白板笔",7:"笔芯"},
        "本册/便签":{1:"纸面笔记本",2:"商务仿皮/皮面本",3:"奖状/证书",4:"便签本/便贴纸"},
        "刀剪/胶水/计算器/橡皮":{1:"计算器",2:"美工刀",3:"剪刀",4:"胶水/胶棒",5:"卷笔刀",6:"橡皮"},
        "收纳用品":{1:"笔筒",2:"名片册/名片盒",3:"档案盒",4:"风琴包",5:"文件栏",6:"抽杆夹/拉杆夹",7:"拉链袋",8:"文件袋",9:"报告夹"},
        "装订用品":{1:"订书机",2:"打孔机",3:"胶带座/封箱器",4:"长尾夹",5:"订书针/起订器",6:"图钉/大头针/回形针",7:"板夹",8:"过塑机",9:"橡皮圈"},
        "白板/配件":{1:"白版",2:"白板配件"},
        "其他用品":{1:"标牌/席",2:"胸卡吊绳及配件",3:"印台/印泥/印油"},},
    "办公消耗用品":
        {"办公耗材":{1:"硒鼓",2:"墨盒",3:"粉盒",4:"色带/碳带"},
        "办公用纸":{1:"打印纸",2:"复印纸"},},
    "软件产品":
        {"基础软件":{1:"操作系统",2:"数据库软件",3:"办公软件",4:"杀毒软件中间件"},
        "应用软件":{1:"图像软件",2:"编程软件",3:"财务软件",4:"多媒体软件",5:"安全软件",6:"管理软件",7:"网络软件"},},
    }
    def DiGui(ZiDian, WeiZhi):
        if isinstance(ZiDian, dict):
            for Jian,Zhi in ZiDian.items():
                FanHui = DiGui(Zhi, WeiZhi + [Jian])
                if FanHui is not None:
                    return FanHui
        elif ZiDian==PingMu:
            return WeiZhi
        else:
            return None
    return DiGui(LieBiao,[])
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
        CaiDan=WeiZhi(ShanPing[0])
        ShuChu=CaiDan[:-1]+ShuChu
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