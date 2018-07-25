# -*- coding: utf-8 -*-
from UserInterface import UserInterface
#make sure to use YYYY-MM-DD format for the date
    #the date will be ignored if 'isHistoricalMode' is 'False'
ui = UserInterface(isHistoricalMode = False, 
                   referenceDate = '2018-07-23')

tickers = 'AAPL'
stockData = ui.researchStocks(tickers)

if ui.fileInput == True:
    ui.writeToFile(stockData, 'testResults.xlsx')
else:
    print(stockData.loc[0])