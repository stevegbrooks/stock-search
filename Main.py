# -*- coding: utf-8 -*-
from Secret import Secret
from UserInterface import UserInterface

secret = Secret()
ui = UserInterface()

gfKey = secret.getGFKey()
intrinioKey = secret.getIntrinioKey()

ui.isHistoricalMode = False

ui.specifyAPI('gurufocus', gfKey, dataRequest = {'endpoint' : 'summary'})
ui.specifyAPI('intrinio', intrinioKey, dataRequest = {'endpoint' : 'historical_data', 
                                                      'item' : 'volume'})

tickers = 'AAPL'
stockData = ui.researchStocks(tickers)

if ui.fileInput == True:
    ui.writeToFile(stockData, 'testResults.xlsx')
else:
    print(stockData.loc[0])