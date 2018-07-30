from UserInterface import UserInterface

ui = UserInterface()

stockData = ui.runApplication(isHistoricalMode = True, 
                               userSettingsProfile = 'garethsSettings', 
                               referenceDate = '2017-01-18', 
                               ticker = 'SHLO')
print(stockData.iloc[0])