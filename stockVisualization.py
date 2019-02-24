# For division
from __future__ import division
# For Data Processing
import numpy as np
import pandas as pd
from pandas import Series, DataFrame

# Data Visualization
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('whitegrid')
#get_ipython().magic(u'matplotlib inline')

# For reading stock data from yahoo
from pandas_datareader import DataReader

# For time stamps
from datetime import datetime

# Changes stockName to Stock Symbol
import json
def findSymbol(stockName):
    with open('stockData.json') as data_file:
        data = json.load(data_file)
        for v in data:
            if(stockName.lower() in v['Name'].lower()):
                return v['Symbol']

#Stores Stock Symbol
#Sample User Input
userInput = "amazon"
stockSymbol = findSymbol(userInput)
print(stockSymbol)

# set up Start and End time for data grab
end = datetime.now()
start = datetime(end.year-1,end.month,end.day)

# Set DataFrame as the Stock Ticker

globals()[stockSymbol] = DataReader(stockSymbol,'yahoo',start,end)

def getDataFrame(stockName):
    return globals()[stockName]

###getDataFrame(stockSymbol).head()

# Summary stats for Apple Stock
###getDataFrame(stockSymbol).describe()

# General Info
###getDataFrame(stockSymbol).info()

# Let's see a historical view of the closing price
###p2 = getDataFrame(stockSymbol)['Close'].plot(legend=True, figsize=(10,4)).figure
###p2.savefig('closingprice.png')

# Now let's plot the total volume of stock being traded each day over the past year

###p2 = getDataFrame(stockSymbol)['Volume'].plot(legend=True, figsize=(10,4)).figure
###p2.savefig('volumesold.png')

# Pandas has a built-in rolling mean calculator

# Let's go ahead and plot out several moving averages
MA_day = [10,20,50,100]

for ma in MA_day:
    column_name = 'MA for %s days' %(str(ma))
    getDataFrame(stockSymbol)[column_name] = getDataFrame(stockSymbol)['Close'].rolling(ma).mean()
    #getDataFrame(stockSymbol)[column_name] = getDataFrame(stockSymbol)['Close'].rolling(ma).mean()

p3 = getDataFrame(stockSymbol)[['Close','MA for 10 days','MA for 20 days','MA for 50 days','MA for 100 days']].plot(subplots=False,figsize=(10,4)).figure
p3.savefig("public/assets/js/meanaverage.png")

from pandas.plotting import table

###ax = plt.subplot(111, frame_on=False) # no visible frame
###ax.xaxis.set_visible(False)  # hide the x axis
###ax.yaxis.set_visible(False)  # hide the y axis

table(ax, getDataFrame(stockSymbol))  # where df is your data frame
plt.gcf
plt.savefig('mytable.png')
