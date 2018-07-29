import pandas as pd
from UserInterface import UserInterface

ui = UserInterface()
###It is crucial that the dates in the excel file follow this format:
    ###YYYY-MM-DD
        ###Format the entire column to 'Text', and then enter the dates
tickers = ui.readTickerInput('tickers.xlsx')

stockData = pd.DataFrame()
for index, row in tickers.iterrows():
    output = ui.runApplication(isHistoricalMode = False, 
                               userSettingsProfile = 'garethsSettings', 
                               referenceDate = row['dates'], 
                               ticker = row['tickers'])
    stockData = stockData.append(output, ignore_index = True)

ui.printResults(stockData, 'results.xlsx')
