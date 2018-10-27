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
df = df.iloc[startRow+1:,:].reset_index(drop=True)

# recalculate ratio
dfW1 = df.loc[:,df.columns.str.contains('W1 Avg')]
dfW2 = df.loc[:,df.columns.str.contains('W2 Avg')]

dfW1.columns = dfW1.columns.str[0:-7]
dfW2.columns = dfW2.columns.str[0:-7]

dfRatio = pd.concat([df.loc[:,'Time (sec)'],dfW1 / dfW2], axis=1)

# drug time
drugs = df.loc[df.iloc[:,3].isna()].iloc[:,0:2]
# dfNum = df.loc[~df.iloc[:,3].isna()]

ctr1 = dfRatio.iloc[30:35,:].mean()

df.iloc[drugs.index[0]-3:drugs.index[0]+4,:]
df.iloc[125-3:125+4,:]

drugRow1 = (df.loc[:,'Time (sec)'] - drug1).abs().argsort().iloc[0]
drugRow1 = (df.loc[:,'Time (sec)'] - drugs).abs().argsort().iloc[0]
min((df.loc[:,'Time (sec)'] - drug1).abs().index)


# plotting
fig, ax = plt.subplots()
ax.plot(dfRatio)
