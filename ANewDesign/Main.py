# -*- coding: utf-8 -*-

from ANewDesign.UserInterface import UserInterface 

ui = UserInterface()

gfKey = "b0373bf00e2473ed61fa029e6777ddc4:98e3238704945ab068f05c902f5c4e09"
intrinioUN = "14434456068d3aa67d6d01703c377c5b"
intrinioPW = "d51918023463341a24d85d8e263f3403"
intrinioKey = [intrinioUN, intrinioPW]

ui.specifyAPI("gurufocus", gfKey, 
              dataRequest = {"endpoint" : "summary"})

ui.specifyAPI("intrinio", intrinioKey, 
              dataRequest = {"endpoint" : "historical_data", 
                             "item" : "close_price",
                             "end_date" : "2018-05-01",
                             "start_date" : "2018-05-01"})

ui.specifyAPI("intrinio", intrinioKey, 
              dataRequest = {"endpoint" : "historical_data", 
                             "item" : "volume"})


tickers = "AAPL"
stockData = ui.researchStocks(tickers)

headerList = stockData.columns.tolist()

stockData = stockData.loc[:,:]

