from dataclasses import replace
from matplotlib.pyplot import axis
import pandas as pd
from py2neo import Graph,Node
from yaml import ValueToken

graph = Graph('bolt://nas.boeing773er.site:7687')


data = pd.read_excel("STaiwan.xlsx")
data.fillna(value=0.0,inplace=True)
print(data.iloc[1]) 
