from UserInterface import UserInterface

ui = UserInterface()

stockData = ui.runApplication(isHistoricalMode = True, 
                               userSettingsProfile = 'garethsSettings', 
                               referenceDate = '2018-07-01', 
                               ticker = 'AAPL')
print(stockData.iloc[0])