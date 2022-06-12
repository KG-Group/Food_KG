import xlrd
from opencc import OpenCC
from py2neo import Graph,Node,Relationship,NodeMatcher
from Disease2Goal import readDataJKMB2YYCF
from eva_algorithm import get_food
colNum = 109
rowNum = 2122

data = xlrd.open_workbook("./document/STaiwan.xls")
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
#print(len(diseases))
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




graph = Graph('bolt://nas.boeing773er.site:7687')
#for goal in Goals:
#    if(goal.startswith('高')):
#        GNode = Node('HigherGoal',name = goal)
#        graph.create(GNode)
#        graph.push(GNode)
#    else:
#        GNode = Node('LowerGoal',name = goal)
#        graph.create(GNode)
#        graph.push(GNode)
#for key in DiseasesGoal.keys():
#    DNode = Node('Disease',name = key)
#    graph.create(DNode)
#    graph.push(DNode)
#    for goal in DiseasesGoal[key]:
#        matcher = NodeMatcher(graph)
#        HGNode = matcher.match("HigherGoal",name = goal).first()
#        LGNode = matcher.match("LowerGoal",name = goal).first()
#        GNode
#        if(HGNode):
#            GNode = HGNode
#        elif(LGNode):
#            GNode = LGNode
#        Edge = Relationship(DNode,"应食用",GNode)
#        graph.create(Edge)
#        graph.push(Edge)
DiseaseFood = get_food()
#print(DiseaseFood)
matcher = NodeMatcher(graph)
for Disease in DiseaseFood.keys():
    for category in DiseaseFood[Disease].keys():
        DNode = matcher.match("Disease",name = Disease).first()
        FNode = matcher.match(category,name = DiseaseFood[Disease][category]).first()
        Edge = Relationship(DNode,"应选择",FNode)
        graph.create(Edge)
        graph.push(Edge)