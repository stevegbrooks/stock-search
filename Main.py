# -*- coding: utf-8 -*-
from UserInterface import UserInterface
ui = UserInterface()
#Toggle this to True to activate 'Historical Mode'
ui.isHistoricalMode = True
#make sure to use YYYY-MM-DD format
    #this will be ignored if the line above is 'False'
ui.historicalDate = '2018-07-20'

tickers = 'testTickers.xlsx'
stockData = ui.researchStocks(tickers)

if ui.fileInput == True:
    ui.writeToFile(stockData, 'testResults.xlsx')
else:
    print(stockData.loc[0])