import xlrd
import xlwt

#data = xlrd.open_workbook("./document/RowMenu60000.xls")
#data2 = xlrd.open_workbook("./document/RowMenu35000.xls")
#table = data.sheets()[0]
#table2 = data2.sheets()[0]
#MenuList = {}

def countnum(List):
    num = 0
    for item in List:
        if(any(chr.isdigit() for chr in item)):
            num +=1
    return num
def isgoodMenu(List):
    
    total = len(List)
    if(total == 0):return False
    num = countnum(List)
    if(num*1.0/total>=0.5):
        return True
    return False

#for i in range(0,60000):
#    nowRow = table.row_values(i,start_colx = 0,end_colx = 50)
#    nowList = []
#    for j in range (1,len(nowRow)):
#        if(nowRow[j] != ''):
#            nowList.append(nowRow[j])
#    if not nowRow[0] in MenuList.keys():
#        MenuList[nowRow[0]] = nowList
#    else:
#        if(countnum(nowList)>countnum(MenuList[nowRow[0]])):
#            MenuList[nowRow[0]] = nowList
#for i in range(0,23327):
#    nowRow = table2.row_values(i,start_colx = 0,end_colx = 50)
#    nowList = []
#    for j in range (1,len(nowRow)):
#        if(nowRow[j] != ''):
#            nowList.append(nowRow[j])
#    if not nowRow[0] in MenuList.keys():
#        MenuList[nowRow[0]] = nowList
#    else:
#        if(countnum(nowList)>countnum(MenuList[nowRow[0]])):
#            MenuList[nowRow[0]] = nowList 
#xl = xlwt.Workbook(encoding = 'utf-8')
#sheet = xl.add_sheet("sheet1")
#i = 0
#for key in MenuList.keys():
#    j = 1
#    sheet.write(i,0,key)
#    for Mat in MenuList[key]:
#        sheet.write(i,j,Mat)
#        j+=1
#    i+=1
#xl.save('./document/HalfRowMenu.xls')
#MenuList = {}
#data = xlrd.open_workbook("./document/HalfRowMenu.xls")
#table = data.sheets()[0]

#for i in range(0,58156):
#    nowRow = table.row_values(i,start_colx = 0,end_colx = 50)
#    nowRow = [item for item in nowRow if item != '']
#    MenuList[nowRow[0]] = nowRow[1:]

#GoodMenuList = {}

#for key in MenuList.keys():
#    if(countnum(MenuList[key])>=4 or isgoodMenu(MenuList[key])):
#        GoodMenuList[key] = MenuList[key]
#print(len(GoodMenuList))

#xl = xlwt.Workbook(encoding = 'utf-8')
#sheet = xl.add_sheet("sheet1")
#i = 0
#for key in GoodMenuList.keys():
#    j = 1
#    sheet.write(i,0,key)
#    for Mat in GoodMenuList[key]:
#        sheet.write(i,j,Mat)
#        j+=1
#    i+=1
#xl.save('./document/QuarterRowMenu.xls')

