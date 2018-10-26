import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile

# read excel data
df = pd.read_excel('data/1_1.xlsx')

# find timestamp
expTime = df.iloc[0,0]

# find startRow = Time (sec)
startRow = max(df[df.iloc[:,0]=='Time (sec)'].index)
df.columns = df.iloc[startRow,:]
df = df.iloc[startRow+1:,:]

# recalculate ratio


df.iloc[0:3,:]
df.columns