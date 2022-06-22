# -*- coding:utf-8 -*-
import xlrd
import xlwt
from py2neo import Graph,Node,Relationship,NodeMatcher
data2 = xlrd.open_workbook("./document/Oly2Menu614.xls")
table2 = data2.sheets()[0]
OlyList = []
OlyNuList = []
colNum = 109
rowNum = 2122

data = xlrd.open_workbook("./document/STaiwan.xls")
table = data.sheets()[0]
FoodList = []
TypeList = ["谷物类"]
            #,"淀粉类"]
            #,"坚果及种子类","水果类","蔬菜类",
            #"藻类","菇类","豆类","肉类","鱼贝类","蛋类","乳品类","油脂类","饮料类","调味料及香辛料类","糕饼点心类","加工调理食品及其他类","糖类"]
title = table.row_values(1,start_colx = 0,end_colx = colNum)

def samechr(s1,s2):
	cnt = 0
	for chr1 in s1:
		for chr2 in s2:
			if(chr1 == chr2):
				cnt +=1
				break
	return cnt

def upload(Dish, Food, graph):
    pass

for i in range(2,rowNum):
    nowRow = table.row_values(i,start_colx = 0,end_colx = colNum)
    nowDic = {}
    for j in range (0,colNum):
        if nowRow[j] != '' :
            nowDic[title[j]] = nowRow[j]
        else:
            nowDic[title[j]] = 0
    FoodList.append(nowDic)

graph = Graph('bolt://nas.boeing773er.site:7687')
matcher = NodeMatcher(graph)
for i in range(0,121):
    nowRow = table2.row_values(i,start_colx = 0,end_colx = 50)
    nowRow = [item for item in nowRow if item != '']
    OlyList.append(nowRow[:])
    NuListItem = []
    NuListItem.append(nowRow[0])
    NuListItem.append(nowRow[2])
    NuListItem.append(nowRow[3])
    NuDic = {}
    for item in nowRow[4:]:
        name = ''
        for chr in item:
            if(not chr.isdigit()):
                name = name + chr
        name = name[:-1]
        best = 0
        good = 0
        for Food in FoodList:
            if(name == Food["样品名称"]):
                #upload(Food["样品名称"],)
                best = 1
                good = 1
                break
        if(best == 0):
            for Food in FoodList:
                if(name in Food["样品名称"]):
                    #upload(Food["样品名称"],)
                    good = 1
                    break
        if(good == 0):
            bestkey = list(FoodList)[0]
            maxsame = samechr(bestkey,name)
            for Food in FoodList:
                if(samechr(Food["样品名称"],name)>maxsame):
                    bestkey = Food
                    maxsame = samechr(Food,name)
            #upload(Food["样品名称"],)


    NuListItem.append(NuDic)
    OlyNuList.append(NuListItem)