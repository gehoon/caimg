import pandas as pd
import re
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from pandas import ExcelWriter
from pandas import ExcelFile


def drawpic(dataFile):
    # read excel data
    df = pd.read_excel(dataFile)

    # find timestamp
    expTime = df.iloc[0,0]

    # new Start by 'Clock reset to 0.0'
    if df.iloc[:, 1].str.contains('Clock reset to 0.0').any():
        startRow = max(df[df.iloc[:, 1] == 'Clock reset to 0.0'].index)
        df = df.iloc[startRow+1:,:].reset_index(drop=True)

    # find startRow = Time (sec)
    try:
        startRow = max(df[df.iloc[:,0]=='Time (sec)'].index)
        df.columns = df.iloc[startRow, :]
        df = df.iloc[startRow + 1:, :].reset_index(drop=True)
    except ValueError:
        startRow = 1
        return

    # recalculate ratio
    dfW1 = df.loc[:,df.columns.str.contains('W1 Avg')]
    dfW2 = df.loc[:,df.columns.str.contains('W2 Avg')]

    dfW1.columns = dfW1.columns.str[0:-7]
    dfW2.columns = dfW2.columns.str[0:-7]

    dfRatio = pd.concat([df.loc[:,'Time (sec)'],dfW1 / dfW2], axis=1)

    # drug time
    drugs = df.loc[df.iloc[:,3].isna()].iloc[:,0:2].reset_index(drop=True)
    i = 0
    while i < len(drugs):
        if drugs.iloc[i, 1] == drugs.iloc[i + 1, 1] and drugs.iloc[i+1, 0] - drugs.iloc[i, 0] < 30:
            i = i + 2
        else:
            drugs.loc['9999'] = [drugs.iloc[i, 0] + 15, drugs.iloc[i, 1]]
            drugs = drugs.sort_values('Time (sec)').reset_index(drop=True)
            i = i + 2

    # filter by thresRatio
    drug1ONidx = abs(dfRatio['Time (sec)'] - drugs['Time (sec)'][0]).astype('float64').idxmin()
    drug1OFFidx = abs(dfRatio['Time (sec)'] - drugs['Time (sec)'][1]).astype('float64').idxmin()

    ctr1 = dfRatio.iloc[0:drug1ONidx,:].mean()
    drug1 = dfRatio.iloc[drug1ONidx:drug1OFFidx,:].max()

    thresRatio = 1.05
    good = (drug1 / ctr1) > thresRatio
    dfPlot = dfRatio.loc[:,good]

    # plotting
    fig, ax = plt.subplots()

    prop_cycle = plt.rcParams['axes.prop_cycle']
    colors = prop_cycle.by_key()['color']

    for data, color, group in zip(dfPlot.iloc[:,1:], colors, list(dfPlot.columns[1:])):
        ax.plot(dfRatio['Time (sec)'], dfPlot[data], c=color, label=group)

    ax.legend()
    plt.title(expTime)

    # plot drug time
    drugON = drugs[0::2].reset_index(drop=True)
    drugOFF = drugs[1::2].reset_index(drop=True)
    drugPlotYPos = (min(dfPlot.iloc[:,1:].min()) + ax.get_ylim()[0]) / 2
    drugNameOffset = max(0.03,drugPlotYPos - ax.get_ylim()[0])
    drugNameYPos = ax.get_ylim()[0] - drugNameOffset
    ax.set_ylim(drugNameYPos, ax.get_ylim()[1])
    for i in range(len(drugON)):
        ax.hlines(drugPlotYPos,drugON['Time (sec)'][i],drugOFF['Time (sec)'][i],lw=5,label='DRUG')
        ax.text(drugON['Time (sec)'][i], drugNameYPos, drugON['R1 W1 Avg'][i], ha='center', va='bottom')

    # visualize
    plt.show()
    plt.close()

    fig.savefig(dataFile.replace('.xlsx','.png'))


dataFile = [
    'AITC_Dex_20181024_1_1', 'AITC_Dex_20181024_1_2', 'AITC_Dex_20181024_2_1', 'AITC_Dex_20181024_2_2', 'AITC_Dex_20181024_3_1',
    'AITC_Dex_20181026_1_1', 'AITC_Dex_20181026_1_2', 'AITC_Dex_20181026_2_1']

# dataFile = 'data/AITC_Dex_20181026_2_1.xlsx'
# dataFile = ['AITC_Dex_20181026_2_1']
for thisFile in dataFile: drawpic('data/' + thisFile + '.xlsx')


