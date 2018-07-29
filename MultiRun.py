import pandas as pd
from UserInterface import UserInterface

ui = UserInterface()

###The input file must include a column named 'tickers' and a column named 'dates'
        
tickers = ui.readTickerInput('tickers.xlsx')

stockData = pd.DataFrame()
for index, row in tickers.iterrows():
    output = ui.runApplication(isHistoricalMode = True, 
                               userSettingsProfile = 'garethsSettings', 
                               referenceDate = row['dates'], 
                               ticker = row['tickers'])
    stockData = stockData.append(output, ignore_index = True)

ui.printResults(stockData, 'results.xlsx')
