from tokenize import group
import pandas as pd
data = pd.read_excel('STaiwan.xlsx')
data.fillna(value=0.0,inplace=True)
data.drop(['样品编号','样品名称','内容物描述','废弃率(%)','P/M/S'],axis=1,inplace=True)
data = data.groupby(data['食品分类']).mean()
data.to_excel('average.xlsx')