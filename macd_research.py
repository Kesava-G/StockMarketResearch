# -*- coding: utf-8 -*-
"""MACD Research

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/19iiwW5nI76dCPVN1_7lFF0PNYGFOq8h1
"""

#Package installations
!pip install yfinance
!pip install yahoo-finance

#Import Statements
import pandas as pd
import numpy as np
import yahoo_finance
import yfinance as yf2

#for Graphical representation
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

#Companies in snp500
payload=pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
snp500 = payload[0]['Symbol'].values.tolist()

companies =[] #list of dataframes of stock info
for ticker in snp500:
  companies.append(yf2.download(ticker)) #web scraping

#Function to indicate close price to buy and sell
def buy_sell(signal):
  Buy= []
  Sell = []
  flag = -1
  for i in range(0, len(signal)):
    if signal['MACD'][i]>signal['Signal Line'][i]:
      Sell.append(np.nan)
      if flag != 1:
        Buy.append(signal['Close'][i])
        flag = 1
      else:
        Buy.append(np.nan)
    elif signal['MACD'][i]<signal['Signal Line'][i]:
      Buy.append(np.nan)
      if flag != 0:
        Sell.append(signal['Close'][i])
        flag = 0
      else:
        Sell.append(np.nan)
    else:
      Buy.append(np.nan)
      Sell.append(np.nan)
  return (Buy, Sell)

profitsPerCompany= {'Ticker Symbol': [], 'Probability of Success': [],'Total Profit ($)': []}
companyindex=0
for i in companies:
  #Edit dataframes with MACD and Signal lines columns
  ShortEMA = i.Close.ewm(span=12, adjust=False).mean() 
  LongEMA = i.Close.ewm(span=26, adjust=False).mean()
  MACD = ShortEMA - LongEMA
  Signal = MACD.ewm(span=9, adjust=False).mean()
  i['MACD'] = MACD
  i['Signal Line'] = Signal
  #Buy or Sell indicator colums
  b = buy_sell(i)
  i['Buy'] = b[0]
  i['Sell'] = b[1]
  #Filter for sell and buy indicator closing prices
  BuyFilter = list(filter(lambda x: not pd.isna(x), i['Buy']))
  SellFilter = list(filter(lambda x: not pd.isna(x), i['Sell']))
  #Calculate Profit per trade
  if len(BuyFilter) > len(SellFilter):
    del BuyFilter[-1]
  if len(SellFilter) > len(BuyFilter):
    del SellFilter[-1]
  profitfortrade =[]
  for trade in range(len(SellFilter)): 
    profitfortrade.append(SellFilter[trade]-BuyFilter[trade])
  #Calculate occurances of profit earning trades
  positives = 0
  for i in profitfortrade:
    if i > 0:
      positives+=1
  profitsPerCompany['Ticker Symbol'].append(str(snp500[companyindex])) 
  try:
    profitsPerCompany['Probability of Success'].append(positives/len(profitfortrade))
  except:
    profitsPerCompany['Probability of Success'].append(np.nan)
  try:
    profitsPerCompany['Total Profit ($)'].append(sum(profitfortrade))
  except:
    profitsPerCompany['Total Profit ($)'].append(np.nan)
  companyindex = companyindex + 1
  print(str(companyindex) + " / 505 Completed")

#Create a dataframe of probabiites of success for each stock

profits = pd.DataFrame(data=profitsPerCompany)
pd.set_option('display.max_rows',505)
plt.hist(profits['Probability of Success'])
profits

for i in range(len(profits['Probability of Success'])):
  if profits['Probability of Success'][i]==0.75:
    print(profits['Ticker Symbol'][i])
    print(i)

ogn = companies[358]
plt.figure(figsize=(20,10))
plt.scatter(ogn.index, ogn['Buy'], color='green',label='Buy', marker='^', alpha=1)
plt.scatter(ogn.index, ogn['Sell'], color='red',label='Sell', marker='v', alpha=1)
plt.plot(ogn['Close'], label='Close Price', alpha =0.35)
plt.title('Close Price Buy and Sell Signals')
plt.xlabel('Date')
plt.ylabel('Close Price')
plt.show

successes = profits['Probability of Success']
ProbabilityFilter = list(filter(lambda x: not pd.isna(x), successes))
print(sum(ProbabilityFilter)/len(successes))
print(max(ProbabilityFilter))

plt.boxplot(ProbabilityFilter)