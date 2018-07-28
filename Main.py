# -*- coding: utf-8 -*-
from UserInterface import UserInterface
ui = UserInterface()

ui.setHistoricalMode(False)
ui.setReferenceDate('2018-07-23')
ui.setTickerInput('tickers.xlsx')

stockData = ui.handleRequest()

ui.displayResults(stockData, 'results.xlsx')