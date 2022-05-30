from dataclasses import dataclass
import xlrd

# 函数 readDataJKMB2YYCF(filepath)
# 返回值为多个dict，可使用此方式获取7种病与对应成份的dict
# 各病dict值定义如下：
## 多吃：1;   无关：0;  少吃：-1
# 例如： tnb['粗脂肪(g)'] 值为 -1，表示 “糖尿病” 少吃 '粗脂肪(g)'
def readDataJKMB2YYCF(filepath):
    wb = xlrd.open_workbook(filepath)
    sh = wb.sheet_by_name('Sheet1')
    print(sh.nrows)   # 有效数据行数
    print(sh.ncols)   # 有效数据列数
       
    title = sh.row_values(1,start_colx = 2,end_colx = sh.ncols)
    
    tnb = {}
    gxy = {}
    tnbgxy = {}
    gxb = {}
    dmyh = {}
    gxz = {}
    fpz = {}

    data = []
    # 糖尿病2
    data = sh.row_values(2,start_colx = 2,end_colx = sh.ncols)
    for i in range(30):
      if data[i] == "+":
        tnb[title[i]] = 1
      elif data[i] == "-":
        tnb[title[i]] = -1
      else:
        tnb[title[i]] = 0
    
    # 高血压3
    data = sh.row_values(3,start_colx = 2,end_colx = sh.ncols)
    for i in range(30):
      if data[i] == "+":
        gxy[title[i]] = 1
      elif data[i] == "-":
        gxy[title[i]] = -1
      else:
        gxy[title[i]] = 0
    
    # 糖尿病高血压4
    data = sh.row_values(4,start_colx = 2,end_colx = sh.ncols)
    for i in range(30):
      if data[i] == "+":
        tnbgxy[title[i]] = 1
      elif data[i] == "-":
        tnbgxy[title[i]] = -1
      else:
        tnbgxy[title[i]] = 0
    
    # 冠心病5
    data = sh.row_values(5,start_colx = 2,end_colx = sh.ncols)
    for i in range(30):
      if data[i] == "+":
        gxb[title[i]] = 1
      elif data[i] == "-":
        gxb[title[i]] = -1
      else:
        gxb[title[i]] = 0
    
    # 冠心病6
    data = sh.row_values(6,start_colx = 2,end_colx = sh.ncols)
    for i in range(30):
      if data[i] == "+":
        dmyh[title[i]] = 1
      elif data[i] == "-":
        dmyh[title[i]] = -1
      else:
        dmyh[title[i]] = 0
    
    # 高血脂7
    data = sh.row_values(7,start_colx = 2,end_colx = sh.ncols)
    for i in range(30):
      if data[i] == "+":
        gxz[title[i]] = 1
      elif data[i] == "-":
        gxz[title[i]] = -1
      else:
        gxz[title[i]] = 0
    
    # 高血脂8
    data = sh.row_values(8,start_colx = 2,end_colx = sh.ncols)
    for i in range(30):
      if data[i] == "+":
        fpz[title[i]] = 1
      elif data[i] == "-":
        fpz[title[i]] = -1
      else:
        fpz[title[i]] = 0

    
    '''print(len(tnb))
    print(len(gxy))
    print(len(tnbgxy))
    print(len(gxb))
    print(len(dmyh))
    print(len(gxz))
    print(len(fpz))'''

    return tnb, gxy, tnbgxy, gxb, dmyh, gxz, fpz




# example
filepath = "健康目标-营养成分（多吃or少吃）20220530.xls"    # 存储“健康目标-营养成分多吃少吃”的文件

tnb, gxy, tnbgxy, gxb, dmyh, gxz, fpz = readDataJKMB2YYCF(filepath)     # 调用函数，存入7种病的dict