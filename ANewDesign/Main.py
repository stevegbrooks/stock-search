# -*- coding: utf-8 -*-

from ANewDesign.UserInterface import UserInterface 

ui = UserInterface()

gfKey = "b0373bf00e2473ed61fa029e6777ddc4:98e3238704945ab068f05c902f5c4e09"
intrinioUN = "14434456068d3aa67d6d01703c377c5b"
intrinioPW = "d51918023463341a24d85d8e263f3403"
intrinioKey = [intrinioUN, intrinioPW]

ui.specifyAPI("gurufocus", gfKey, "company data")
ui.specifyAPI("intrinio", intrinioKey, "historical volume")

ticker = "AAPL"
stockData = ui.researchStocks(ticker)

desiredColumnOrder = ['stockSymbol', 'companyName', 'lastPrice', 'lastVolume', 
                      'outstandingShares', 'avgVolume', 'percentChange']

stockData = stockData[desiredColumnOrder]