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
title = table.row_values(1,start_colx = 0,end_colx = colNum)

def samechr(s1,s2):
	cnt = 0
	for chr1 in s1:
		for chr2 in s2:
			if(chr1 == chr2):
				cnt +=1
				break
	return cnt

for i in range(2,rowNum):
    nowRow = table.row_values(i,start_colx = 0,end_colx = colNum)
    nowDic = {}
    for j in range (0,colNum):
        if nowRow[j] != '' :
            nowDic[title[j]] = nowRow[j]
        else:
            nowDic[title[j]] = 0
    FoodList.append(nowDic)

Compareresult = ''
for i in range(0,121):
    nowRow = table2.row_values(i,start_colx = 0,end_colx = 50)
    nowRow = [item for item in nowRow if item != '']
    OlyList.append(nowRow[:])
    NuListItem = []
    NuListItem.append(nowRow[0])
    NuListItem.append(nowRow[2])
    NuListItem.append(nowRow[3])
    NuDic = {}
    for key in title[5:86] + title[87:]:
        NuDic[key] = 0
    totalnum = 0
    for item in nowRow[4:]:
        num = ''
        for chr in item:
            if(chr.isdigit()):
                num = num+chr
        totalnum += int(num)
    for item in nowRow[4:]:
        name = ''
        num = ''
        for chr in item:
            if(chr.isdigit()):
                num = num+chr
            else:
                name = name + chr
        name = name[:-1]
        best = 0
        good = 0
        for Food in FoodList:
            if(name == Food["样品名称"]):
                Compareresult = Compareresult + name + " " + Food["样品名称"] + '\n'
                for key in title[5:86] + title[87:]:
                    NuDic[key] = NuDic[key] + Food[key]*(300/totalnum)*(int(num)/100)
                best = 1
                good = 1
                break
        if(best == 0):
            for Food in FoodList:
                if(name in Food["样品名称"]):
                    Compareresult = Compareresult + name + " " + Food["样品名称"] + '\n'
                    for key in title[5:86] + title[87:]:
                        NuDic[key] = NuDic[key] + Food[key]*(300/totalnum)*(int(num)/100)
                    good = 1
                    break
        if(good == 0):
            bestkey = list(FoodList)[0]
            maxsame = samechr(bestkey,name)
            for Food in FoodList:
                if(samechr(Food["样品名称"],name)>maxsame):
                    bestkey = Food
                    maxsame = samechr(Food,name)
            Compareresult = Compareresult + name + " " + bestkey["样品名称"] + '\n'
            for key in title[5:86] + title[87:]:
                NuDic[key] = NuDic[key] + bestkey[key]*(300/totalnum)*(int(num)/100)


    NuListItem.append(NuDic)
    OlyNuList.append(NuListItem)
    #print(i)
    #print(NuListItem)
#print(OlyNuList[0:3])

xl = xlwt.Workbook(encoding = 'utf-8')
sheet = xl.add_sheet("sheet1")

sheet.write(0,0,"菜名")
sheet.write(0,1,"类型")
sheet.write(0,2,"价格")
i = 3
for key in OlyNuList[3][3].keys():
    sheet.write(0,i,key)
    i += 1
i = 1

for item in OlyNuList:
    j = 3
    sheet.write(i,0,item[0])
    sheet.write(i,1,item[1])
    sheet.write(i,2,item[2])
    for key in OlyNuList[3][3].keys():
        sheet.write(i,j,item[3][key])
        j+=1
    i+=1
xl.save('./document/OlyNu.xls')

graph = Graph('bolt://nas.boeing773er.site:7687')

matcher = NodeMatcher(graph)
for OlyNu in OlyNuList:
    ONode = Node("Dish",name = OlyNu[0])
    ONode["类型"] = OlyNu[1]
    ONode["价格"] = OlyNu[2]
    for key in OlyNu[3].keys():
        ONode[key] = OlyNu[3][key]
    graph.create(ONode)
    graph.push(ONode)
Compareresult = Compareresult.split('\n')
Compareresult = list(set(Compareresult))
print(Compareresult)
f = open("./document/CResult.txt",'w')
a = 0
for item in Compareresult:
    f.write(str(a) + ' ')
    f.write(item)
    f.write('\n')
    a+=1
f.close()