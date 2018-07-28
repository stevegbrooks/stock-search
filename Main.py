# -*- coding: utf-8 -*-
from UserInterface import UserInterface

ui = UserInterface()

ui.setHistoricalMode(False)
ui.setAPIs('garethsSettings', '2018-07-23') 
ui.setTickerInput('tickers.xlsx', justTickers = True)

stockData = ui.handleRequest()

ui.displayResults(stockData, 'results.xlsx')