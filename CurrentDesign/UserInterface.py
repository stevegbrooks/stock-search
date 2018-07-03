# -*- coding: utf-8 -*-
import StockAPICaller as sac
from Utilities.FileWriter import FileWriter as fw

gfKey = "b0373bf00e2473ed61fa029e6777ddc4:98e3238704945ab068f05c902f5c4e09"
intrinioUN = "14434456068d3aa67d6d01703c377c5b"
intrinioPW = "d51918023463341a24d85d8e263f3403"

######Enter a file name or a ticker symbol here############
userInput = "testTickers.xlsx"
###########################################################

stockAPICaller = sac.StockAPICaller(gfKey, intrinioUN, intrinioPW)

apiResults = stockAPICaller.getStockData(userInput)

if stockAPICaller.fileInput == True:
    fw.writeToExcel(apiResults, "testResults.xlsx")
else:
    print(apiResults.loc[0])