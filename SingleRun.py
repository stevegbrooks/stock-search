"""
Use SingleRun when you just want to return a single company's data to the console

@author: sgb
"""

from UserInterface import UserInterface

ui = UserInterface()

stockData = ui.runApplication(isHistoricalMode = True, 
                               userSettingsProfile = 'garethsSettings2', 
                               referenceDate = '2017-02-17', 
                               ticker = 'TRUE')

print(stockData.iloc[0])