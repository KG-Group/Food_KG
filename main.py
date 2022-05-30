﻿import xlrd
from opencc import OpenCC
from py2neo import Graph,Node,Relationship,NodeMatcher
from Disease2Goal import readDataJKMB2YYCF
colNum = 109
rowNum = 2122

data = xlrd.open_workbook("STaiwan.xls")
table = data.sheets()[0]
N_row = table.nrows
FoodList = []


title = table.row_values(1,start_colx = 0,end_colx = colNum)


for i in range(2,rowNum):
    nowRow = table.row_values(i,start_colx = 0,end_colx = colNum)
    nowDic = {}
    for j in range (0,colNum):
        if nowRow[j] != '' :
            nowDic[title[j]] = nowRow[j]
        else:
            nowDic[title[j]] = 0
    FoodList.append(nowDic)


Relations = []
Diseases = ['糖尿病','高血压','糖尿病和高血压','冠心病','动脉硬化','高血脂','肥胖症']
diseases = readDataJKMB2YYCF()
Goals = []

GoalTitle = {}
GoalTend = {}
DiseasesGoal = {}
print(len(diseases))
for i in range(0,7):
    DGoals = []
    for key in diseases[i].keys():
        if(diseases[i][key] == 1 or diseases[i][key] == -1):
            s = ''
            if(diseases[i][key] == 1):
                s = s + '高'
            elif (diseases[i][key] == -1):
                s = s + '低'
            s = s + key
            s = s.replace(')','')
            s = s.replace('(','')
            s = s.replace('g','')
            s = s.replace('mg','')
            s = s.replace('u','')
            s = s.replace('m','')
            s = s.replace('IU','')
            Goals.append(s)
            GoalTitle[s] = key
            if(diseases[i][key] == 1):
                GoalTend[s] = diseases[i][key]
            else:
                GoalTend[s] = 0
            DGoals.append(s)
    DiseasesGoal[Diseases[i]] = DGoals
Goals = dict.fromkeys(Goals)
Goals = list(Goals.keys())
print(DiseasesGoal)




graph = Graph('bolt://nas.boeing773er.site:7687')
for goal in Goals:
    GNode = Node('Goal',name = goal)
    graph.create(GNode)
    graph.push(GNode)
for key in DiseasesGoal.keys():
    DNode = Node('Disease',name = key)
    graph.create(DNode)
    graph.push(DNode)
    for goal in DiseasesGoal[key]:
        matcher = NodeMatcher(graph)
        GNode = matcher.match("Goal",name = goal).first()
        Edge = Relationship(DNode,"包含",GNode)
        graph.create(Edge)
        graph.push(Edge)