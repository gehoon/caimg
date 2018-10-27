import pandas as pd
import re
import numpy as np
from scipy import stats
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

# filter by thresRatio
ctr1 = dfRatio.iloc[0:drugs.index[0],:].mean()
drug1 = dfRatio.iloc[drugs.index[0]:drugs.index[1],:].max()

thresRatio = 1.05
good = (drug1 / ctr1) > thresRatio
dfPlot = dfRatio.loc[:,good]

# plotting
fig, ax = plt.subplots()
ax.plot(dfRatio['Time (sec)'], dfPlot.iloc[:,1:])
plt.show()