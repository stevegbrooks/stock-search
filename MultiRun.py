"""
Use MultiRun when you want to do research on a series of ticker symbols with or
without reference dates.

The input must be an .xlsx file with a column titled 'tickers' and a column titled 'dates'.
The 'dates' column should be in the Excel "Date" format, and not text. 

If the 'dates' column is left empty, it just uses today as the reference date, even if 
historical mode is set to 'True'.

@author: sgb
"""
import pandas as pd
from UserInterface import UserInterface
from WebCrawler import WebCrawler

ui = UserInterface()
tickers = ui.readTickerInput('tickers.xlsx')
isHistoricalMode = False

#################################################
#################################################
#################################################
#################################################
#################################################
###DO NOT TOUCH ANYTHING BETWEEN THESE BLOCKS!!##

print("Starting program...")

if isHistoricalMode == False:
    wc = WebCrawler()
    wc.setDriverPath('/Users/sgb/Desktop/Stuff/Python/StockAPICaller/chromedriver')
    wc.createDriver()
    wc.briefingLogin(['garethb787@gmail.com', 'Massivecat22'])

stockData = pd.DataFrame()

for index, row in tickers.iterrows():
    output = ui.runApplication(isHistoricalMode = isHistoricalMode, 
                               userSettingsProfile = 'garethsSettings', 
                               referenceDate = row['dates'], 
                               ticker = row['tickers'])
    stockData = stockData.append(output, ignore_index = True)
    if index+1 < len(tickers):
        print("{}% complete...".format(round((index+1)/len(tickers)*100)))
    else:
        print("Program finished")
        
ui.printResults(stockData)

###DO NOT TOUCH ANYTHING BETWEEN THESE BLOCKS!!##
#################################################
#################################################
#################################################
#################################################
#################################################

if isHistoricalMode == False:
    wc.briefingLogout() #highlight and run just this line if the program halts midway through due before trying again
    wc.killDriver()