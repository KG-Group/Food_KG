import pandas as pd

data = pd.read_excel('STaiwan.xlsx')
data.fillna(value=0.0,inplace=True)
data.drop(['样品编号','食品分类','样品名称','内容物描述','废弃率(%)','P/M/S'],axis=1,inplace=True)

def minMaxNormalization(df):
    return (df-df.min())/(df.max()-df.min())

normalized = minMaxNormalization(data)
data = pd.read_excel('STaiwan.xlsx')
normalized.insert(column='样品名称',loc=0,value=data['样品名称'])
normalized.insert(column='食品分类',loc=0,value=data['食品分类'])
normalized.insert(column='样品编号',loc=0,value=data['样品编号'])


normalized.to_excel('Normalized.xlsx')

