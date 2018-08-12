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

ui = UserInterface()
        
tickers = ui.readTickerInput('tickers.xlsx')
isHistoricalMode = False

####DONT CHANGE ANYTHING BELOW THIS LINE
stockData = pd.DataFrame()
print("Starting program...")
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
