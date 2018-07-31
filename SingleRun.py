"""
Use SingleRun when you just want to return a single company's data to the console

@author: sgb
"""

from UserInterface import UserInterface

ui = UserInterface()

stockData = ui.runApplication(isHistoricalMode = True, 
                               userSettingsProfile = 'garethsSettings', 
                               referenceDate = '2017-01-18', 
                               ticker = 'SHLO')
print(stockData.iloc[0])