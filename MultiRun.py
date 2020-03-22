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
isHistoricalMode = True

print("Starting program...")

stockData = pd.DataFrame()

try:
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
            
    ui.printToFile(stockData)

except Exception as e:
    print(f'Error: {e}')
    
