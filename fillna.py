import pandas as pd
data = pd.read_excel('document/STaiwan.xlsx')
filled = data.fillna(value=0.0)
filled.to_excel('document/STaiwan_filled0.xlsx')