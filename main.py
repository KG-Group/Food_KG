import xlrd
from opencc import OpenCC
from py2neo import Graph,Node,Relationship
colNum = 109
rowNum = 2122
data = xlrd.open_workbook("STaiwan.xls")
table = data.sheets()[0]
N_row = table.nrows
FoodList = []
#test = table.row_values(3,start_colx = 1,end_colx = colNum)
#print(test)
title = table.row_values(1,start_colx = 0,end_colx = colNum)
#print(title)
for i in range(3,rowNum):
    nowRow = table.row_values(i,start_colx = 0,end_colx = colNum)
    #print(nowRow)
    nowDic = {}
    for j in range (0,colNum):
        nowDic[title[j]] = nowRow[j]
    FoodList.append(nowDic)
print(FoodList[56])
links = []

graph = Graph('bolt://nas.boeing773er.site:7687')
