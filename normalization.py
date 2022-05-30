import pandas as pd

data = pd.read_excel('STaiwan.xlsx')
data.fillna(value=0.0,inplace=True)
data.drop(['样品编号','食品分类','样品名称','内容物描述','废弃率(%)','P/M/S'],axis=1,inplace=True)

def minMaxNormalization(df):
    return (df-df.min())/(df.max()-df.min())

normalized = minMaxNormalization(data)
normalized.to_excel('Normalized.xlsx')
