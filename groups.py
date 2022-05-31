import pandas as pd
writer = pd.ExcelWriter('document/group.xlsx')
items = ['谷物类','淀粉类','坚果及种子类','水果类','蔬菜类','藻类','菇类','豆类','糕饼点心类','肉类','鱼贝类','蛋类','乳品类','油脂类','糖类','饮料类','调味料及香辛料类','加工调理食品及其他类']

def count(i):
    val = list(to[to.columns[i]])
    bins = [0.05*j for j in range(21)]
    flag = 0
    for k in val:
        if k!=val[0]:
            flag=1
            break
    if flag==1: 
        cats = pd.cut(val,bins)
        temp = pd.value_counts(cats).sort_index().values
        res.insert(loc=i,column=to.columns[i],value=temp)
    else:
        res.insert(loc=i,column=to.columns[i],value=[len(to)]+[i-i for i in range(19)])


for i in items:
    data = pd.read_excel('document/Normalized.xlsx',sheet_name=i)
    to = pd.DataFrame()
    res = pd.DataFrame()
    to = data.drop(data.columns[:4],axis=1)
    for j in range(len(to.columns)):
        count(j)
    res.insert(column='',loc=0,value=range(20))
    res.to_excel(excel_writer=writer,sheet_name=i,index=False)
    writer.save()
writer.close()