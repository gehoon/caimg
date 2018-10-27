import pandas as pd
import re
import numpy as np
import matplotlib.pyplot as plt
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

# convert to all numerical dataframe
dfDrug = df.loc[df.iloc[:,3].isna()]
dfNum = df.loc[~df.iloc[:,3].isna()]

# recalculate ratio
dfW1 = df.loc[:,df.columns.str.contains('W1 Avg')]
dfW2 = df.loc[:,df.columns.str.contains('W2 Avg')]

dfW1.columns = dfW1.columns.str[0:-7]
dfW2.columns = dfW2.columns.str[0:-7]

dfRatio = dfW1 / dfW2

# plotting
fig, ax = plt.subplots()
ax.plot(dfRatio)
