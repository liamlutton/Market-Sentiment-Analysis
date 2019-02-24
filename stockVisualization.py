from __future__ import division
import numpy as np
import pandas as pd
from pandas import Series, DataFrame
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('whitegrid')
from pandas_datareader import DataReader
from datetime import datetime
import json

# change stock name to stock ticker symbol
def findSymbol(stockName):  
    with open('stockData.json') as data_file:    
        data = json.load(data_file)
        for v in data:
            if(stockName.lower() in v['Name'].lower()):
                return v['Symbol']

# sample user input
userInput = "Apple"
stockSymbol = findSymbol(userInput)
print(stockSymbol)

# set up start and end time for data grab
end = datetime.now()
start = datetime(end.year-1,end.month,end.day)

# set DataFrame as the stock ticker
globals()[stockSymbol] = DataReader(stockSymbol,'yahoo',start,end)

def getDataFrame(stockName):
    return globals()[stockName]

getDataFrame(stockSymbol).head()

# summary stats for Apple stock
getDataFrame(stockSymbol).describe()

getDataFrame(stockSymbol).info()

# historical view of the closing price
p2 = getDataFrame(stockSymbol)['Close'].plot(legend=True, figsize=(10,4)).figure
p2.savefig('closingprice.png')

# plot the total volume of stock traded each day over past year
p2 = getDataFrame(stockSymbol)['Volume'].plot(legend=True, figsize=(10,4)).figure
p2.savefig('volumesold.png')

# plot out several moving averages using a rolling mean calculator
MA_day = [10,20,50,100]

for ma in MA_day:
    column_name = 'MA for %s days' %(str(ma))
    getDataFrame(stockSymbol)[column_name] = getDataFrame(stockSymbol)['Close'].rolling(ma).mean()

p3 = getDataFrame(stockSymbol)[['Close','MA for 10 days','MA for 20 days','MA for 50 days','MA for 100 days']].plot(subplots=False,figsize=(10,4)).figure
p3.savefig("meanaverage.png")

from pandas.plotting import table

ax = plt.subplot(111, frame_on=False) # no visible frame
ax.xaxis.set_visible(False)  # hide the x axis
ax.yaxis.set_visible(False)  # hide the y axis

table(ax, getDataFrame(stockSymbol))  # where df is data frame
plt.gcf
plt.savefig('mytable.png')
