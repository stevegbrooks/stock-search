from UserInterface import UserInterface

ui = UserInterface()

stockData = ui.runApplication(isHistoricalMode = False, 
                               userSettingsProfile = 'garethsSettings', 
                               referenceDate = '2018-07-01', 
                               ticker = 'AAPL')
stockData.iloc[0]