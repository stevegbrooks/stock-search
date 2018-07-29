from UserInterface import UserInterface

ui = UserInterface()

stockData = ui.runApplication(isHistoricalMode = True, 
                               userSettingsProfile = 'garethsSettings', 
                               referenceDate = '2018-02-21', 
                               ticker = 'CNDT')
print(stockData.iloc[0])