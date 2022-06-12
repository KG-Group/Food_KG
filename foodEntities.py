from dataclasses import replace
from tokenize import String
from matplotlib.pyplot import axis
import pandas as pd
from py2neo import Graph,Node
from yaml import ValueToken

graph = Graph('bolt://nas.boeing773er.site:7687')


data = pd.read_excel("document/STaiwan.xlsx")
data.fillna(value=0.0,inplace=True)

def insert(index):
    foodNode = Node(str(data.iloc[index][1]),name=data.iloc[index][2])
    for i in range(len(data.columns)):
        if isinstance (data.iloc[index][i],str):
            foodNode[str(data.columns[i])] = data.iloc[index][i]
        else:
            foodNode[str(data.columns[i])] = float(data.iloc[index][i])
    graph.create(foodNode)
    graph.push(foodNode)

for i in range(2120):
    insert(i)