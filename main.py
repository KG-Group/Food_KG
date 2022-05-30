import xlrd
from opencc import OpenCC
from py2neo import Graph,Node,Relationship
colNum = 109
rowNum = 2122

data = xlrd.open_workbook("STaiwan.xls")
table = data.sheets()[0]
N_row = table.nrows
FoodList = []


title = table.row_values(1,start_colx = 0,end_colx = colNum)
# print(title)


for i in range(2,rowNum):
    nowRow = table.row_values(i,start_colx = 0,end_colx = colNum)
    # print(nowRow)
    nowDic = {}
    for j in range (0,colNum):
        if nowRow[j] != '' :
            nowDic[title[j]] = nowRow[j]
        else:
            nowDic[title[j]] = 0
    FoodList.append(nowDic)
print(FoodList[1])


Relations = []
diseases = ['糖尿病','高血压','冠心病','动脉硬化','高血脂','肥胖症']
Goals = ['高纤维','低糖','高钙','高硒','高维生素B','高维生素C','高碘','高钾','高胡萝卜素','高维生素','高蛋白质','高矿物质','高热量','低盐','低脂','低胆固醇']

GoalTitle = {}
GoalTend = {}

#GoalTitle[Goals[0]] = title[13] #高纤维
#GoalTend[Goals[0]] = '+'

#GoalTitle[Goals[1]] = title[12] #低糖
#GoalTend[Goals[1]] = '-'

#GoalTitle[Goals[2]] = title[13] #高钙
#GoalTend[Goals[2]] = '+'

#GoalTitle[Goals[3]] = title[13] #高硒
#GoalTend[Goals[3]] = '+'

#GoalTitle[Goals[4]] = title[13] #高维生素B
#GoalTend[Goals[4]] = '+'

#GoalTitle[Goals[5]] = title[13] #高维生素C
#GoalTend[Goals[5]] = '+'

#GoalTitle[Goals[6]] = title[13] #高碘
#GoalTend[Goals[6]] = '+'

#GoalTitle[Goals[7]] = title[13] #高钾
#GoalTend[Goals[7]] = '+'

#GoalTitle[Goals[8]] = title[13] #高胡萝卜素
#GoalTend[Goals[8]] = '+'

#GoalTitle[Goals[9]] = title[13] #高维生素
#GoalTend[Goals[9]] = '+'

#GoalTitle[Goals[10]] = title[8] #高蛋白质
#GoalTend[Goals[10]] = '+'

#GoalTitle[Goals[11]] = title[13] #高矿物质
#GoalTend[Goals[11]] = '+'

#GoalTitle[Goals[12]] = title[6] #高热量
#GoalTend[Goals[12]] = '+'

#GoalTitle[Goals[13]] = title[13] #低盐
#GoalTend[Goals[13]] = '+'

#GoalTitle[Goals[14]] = title[6] #低脂
#GoalTend[Goals[14]] = '-'

#GoalTitle[Goals[15]] = title[6] #低胆固醇
#GoalTend[Goals[15]] = '-'

print (GoalTitle)
print (GoalTend)
# graph = Graph('bolt://nas.boeing773er.site:7687')
# testNode = Node('Food',name = FoodList[56]['样品名称'])
# testNode['蛋白质'] = '0.03'
# graph.create(testNode)
# graph.push(testNode)