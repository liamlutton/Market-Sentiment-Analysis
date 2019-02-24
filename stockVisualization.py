#!/usr/bin/env python
# coding: utf-8

# Project: Stock Market Analysis and Prediction

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

#Changes StockName to Stock Symbol
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

# In[50]:


# set up Start and End time for data grab
end = datetime.now()
start = datetime(end.year-1,end.month,end.day)

#For-loop for grabing google finance data and setting as a dataframe
# Set DataFrame as the Stock Ticker

globals()[stockSymbol] = DataReader(stockSymbol,'yahoo',start,end)


# In[51]:


def getDataFrame(stockName):
    return globals()[stockName]



# In[52]:


getDataFrame(stockSymbol).head()


# In[53]:


# Summery stats for Apple Stock
getDataFrame(stockSymbol).describe()


# In[54]:


# General Info
getDataFrame(stockSymbol).info()


# In[55]:


# Let's see a historical view of the closing price
p2 = getDataFrame(stockSymbol)['Close'].plot(legend=True, figsize=(10,4)).figure
p2.savefig('closingprice.png')


# In[56]:


# Now let's plot the total volume of stock being traded each day over the past year

p2 = getDataFrame(stockSymbol)['Volume'].plot(legend=True, figsize=(10,4)).figure
p2.savefig('volumesold.png')


# In[57]:


# Pandas has a built-in rolling mean calculator

# Let's go ahead and plot out several moving averages
MA_day = [10,20,50,100]

for ma in MA_day:
    column_name = 'MA for %s days' %(str(ma))
    getDataFrame(stockSymbol)[column_name] = getDataFrame(stockSymbol)['Close'].rolling(ma).mean()
    #getDataFrame(stockSymbol)[column_name] = getDataFrame(stockSymbol)['Close'].rolling(ma).mean()


# In[58]:



p3 = getDataFrame(stockSymbol)[['Close','MA for 10 days','MA for 20 days','MA for 50 days','MA for 100 days']].plot(subplots=False,figsize=(10,4)).figure
p3.savefig("meanaverage.png")


# In[ ]:


from pandas.plotting import table

ax = plt.subplot(111, frame_on=False) # no visible frame
ax.xaxis.set_visible(False)  # hide the x axis
ax.yaxis.set_visible(False)  # hide the y axis

table(ax, getDataFrame(stockSymbol))  # where df is your data frame
plt.gcf
plt.savefig('mytable.png')


# In[ ]:


#graph = getDataFrame(stockSymbol)[['Close','MA for 10 days','MA for 20 days','MA for 50 days','MA for 100 days']]
#fig = graph.plot(subplots=False,figsize=(10,4))
#graph2 = pd.matplotlib(graph)
#fig2 = graph2.get_figure()
#fig2.savefig("output.png")


# In[ ]:





# In[ ]:


#from subprocess import call
#call(["open", "graph3.png"])
