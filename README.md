此套程序为河南省政府采购网的爬虫，可以实现商品数据的采集跟踪，价格对比，输出报表等

版本v1.1,v1.2为早期程序代码，已经失效，在此不必细说！

v1.3版本是最新版本（截止至2018.6.8），使用了openpyxl、sqlite3、csv、BeautifulSoup等第三方库，使用前请安装相关库。里面程序文件较多，执行顺序及说明如下(注：前5步一次只能执行一步，不能同时执行)：

1，先执行程序 URL_ChuLi1.py，此程序主要处理商品的分类

2,执行程序 URL_ChuLi2.py，此程序主要处理商品链接

3,执行完上一个程序后，会在目录下面留下名为 URL_RiZhi.log 的日志文件，打开若发现有错误记录，执行程序程序 URL_CuoWuChuLi.py，若没有，忽略直接执行下一步

4,执行程序 ShuJvChuLi.py,此程序主要处理商品信息

5,上一步执行完毕，会在目录下面留下名为 ShuJiRiZhi.log 的日志文件，打开若发现有错误记录，执行程序 ShuJvCuoWuChuLi.py，若没有，忽略执行下一步

6,程序史泰博数据清洗_csv.py，史泰博数据清洗_xlsx.py 可以输出史泰博与其他电商相同商品价格对比的csv或者xlsx格式的,文件名名为数据集的数据报表，程序友商数据清洗_csv.py，友商数据清洗_xlsx.py 可以在目录 数据集 （若没有此文件夹请新建一个名为“数据集”的文件夹，否则可能报错）下生成各家电商与其他电商相同商品价格对比的csv或者xlsx格式的数据报表
