import xlrd
import xlwt
from opencc import OpenCC
colNum = 109
rowNum = 2122
STaiwan = xlwt.Workbook()
Ssheet = STaiwan.add_sheet('Sheet1')

data = xlrd.open_workbook("Taiwan.xls")
table = data.sheets()[0]
for i in range(0,rowNum):
    nowRow = table.row_values(i,start_colx = 0,end_colx = colNum)
    for j in range(0,colNum):
        if(type(nowRow[j]) == str):
            nowRow[j] = OpenCC('t2s').convert(nowRow[j])
            Ssheet.write(i,j,nowRow[j])
        else:
            Ssheet.write(i,j,nowRow[j])
STaiwan.save('STaiwan.xls')