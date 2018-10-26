import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile

# df = pd.read_excel('data/1_1.xlsx', sheetname='Sheet1')
df = pd.read_excel('data/1_1.xlsx')

print("Column headings:")
print(df.columns)