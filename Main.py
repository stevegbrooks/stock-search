# -*- coding: utf-8 -*-
from UserInterface import UserInterface

ui = UserInterface()

ui.isHistoricalMode = True

tickers = 'AAPL'
stockData = ui.researchStocks(tickers)

if ui.fileInput == True:
    ui.writeToFile(stockData, 'testResults.xlsx')
else:
    print(stockData.loc[0])