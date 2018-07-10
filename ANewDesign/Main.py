# -*- coding: utf-8 -*-
from ANewDesign.Secret import Secret
from ANewDesign.UserInterface import UserInterface

secret = Secret()
ui = UserInterface()

gfKey = secret.getGFKey()
intrinioKey = secret.getIntrinioKey()

ui.specifyAPI('gurufocus', gfKey, 
              dataRequest = {'endpoint' : 'summary'})

ui.specifyAPI('intrinio', intrinioKey, 
              dataRequest = {'endpoint' : 'historical_data', 
                             'item' : 'close_price',
                             'date' : '2018-06-01'})

ui.specifyAPI('intrinio', intrinioKey, 
              dataRequest = {'endpoint' : 'historical_data', 
                             'item' : 'volume',
                             'end_date' : '2018-06-01'})

tickers = 'testTickers.xlsx'
stockData = ui.researchStocks(tickers)

if ui.fileInput == True:
    ui.writeToFile(stockData, 'testResults.xlsx')
else:
    print(stockData.loc[0])