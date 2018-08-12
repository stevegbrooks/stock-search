"""
Use SingleRun when you just want to return a single company's data to the console

@author: sgb
"""

from UserInterface import UserInterface

ui = UserInterface()

stockData = ui.runApplication(isHistoricalMode = False, 
                               userSettingsProfile = 'garethsSettings', 
                               referenceDate = '2017-02-17', 
                               ticker = 'JOE')

print(stockData.iloc[0])