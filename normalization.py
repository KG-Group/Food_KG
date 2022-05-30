import pandas as pd
writer = pd.ExcelWriter('Normalized.xlsx')
items = ['谷物类','淀粉类','坚果及种子类','水果类','蔬菜类','藻类','菇类','豆类','糕饼点心类','肉类','鱼贝类','蛋类','乳品类','油脂类','糖类','饮料类','调味料及香辛料类','加工调理食品及其他类']

def minMaxNormalization(df):
    return (df-df.min())/(df.max()-df.min())

data = pd.read_excel('STaiwan.xlsx')
data.fillna(value=0.0,inplace=True)
for i in items:
    to = data[data['食品分类']==i]
    to_= data[data['食品分类']==i]
    to.drop(['样品编号','食品分类','样品名称','内容物描述','废弃率(%)','P/M/S'],axis=1,inplace=True)
    normalized = minMaxNormalization(to)
    normalized.insert(column='样品名称',loc=0,value=to_['样品名称'])
    normalized.insert(column='食品分类',loc=0,value=to_['食品分类'])
    normalized.insert(column='样品编号',loc=0,value=to_['样品编号'])
    normalized.to_excel(writer,sheet_name=i)
    writer.save()
writer.close()





