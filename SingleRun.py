"""
Use SingleRun when you just want to return a single company's data to the console

@author: sgb
"""

from UserInterface import UserInterface
from WebCrawler import WebCrawler

ui = UserInterface()

ticker = 'WSC'
referenceDate = '2017-02-17'
isHistoricalMode = False
settings = 'garethsSettings'

try:
    stockData = ui.runApplication(
        isHistoricalMode = isHistoricalMode, 
        userSettingsProfile = settings, 
        referenceDate = referenceDate, 
        ticker = ticker
    )
    print(stockData.iloc[0])
except Exception as e:
    print(f'Error: {e}')

