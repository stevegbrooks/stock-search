"""
Use SingleRun when you just want to return a single company's data to the console

@author: sgb
"""

from UserInterface import UserInterface
from WebCrawler import WebCrawler

ticker = 'FB'
referenceDate = '2017-02-17'
isHistoricalMode = False
settings = 'garethsSettings'

#################################################
#################################################
#################################################
#################################################
#################################################
###DO NOT TOUCH ANYTHING BELOW THIS LINE!!#######

if isHistoricalMode == False:
    wc = WebCrawler()
    wc.setDriverPath('/Users/sgb/Desktop/Stuff/Python/StockAPICaller/chromedriver')
    wc.createDriver()
    wc.briefingLogin(['garethb787@gmail.com', 'Massivecat22'])

ui = UserInterface()

stockData = ui.runApplication(isHistoricalMode = isHistoricalMode, 
                              userSettingsProfile = settings, 
                              referenceDate = referenceDate, 
                              ticker = ticker)

print(stockData.iloc[0])

if isHistoricalMode == False:
    wc.briefingLogout()
    wc.killDriver()
