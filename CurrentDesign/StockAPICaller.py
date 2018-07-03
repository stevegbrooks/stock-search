import pandas as pd
import re
import requests
import datetime
from Utilities.Calculator import Calculator as calc
from Utilities.FileReader import FileReader as fr

class StockAPICaller:

    guruFocusKey = ""
    intrinioUserName = ""
    intrinioPassword = ""
    
    def __init__(self, 
                 guruFocusKey, 
                 intrinioUserName, 
                 intrinioPassword):
        
        self.guruFocusKey = guruFocusKey
        self.intrinioUserName = intrinioUserName
        self.intrinioPassword = intrinioPassword
        self.fileInput = False
        self.tickers = []
    
    def parseInput(self, userInput):
        output = []
        match = re.search("\\.[a-zA-Z]*$", userInput, flags = 0)
        if match:
            if match.group(0) == ".xlsx" or match.group(0) == ".csv":
                self.fileInput = True
                columnNumber = 0
                output = fr.readExcelColumn(userInput, columnNumber)
            else:
                raise Exception("Currently only .xlsx and .csv files are supported.")
        else:
            output.append(userInput)
        
        return output
    
    def getStockData(self, stockTickerOrFile):
        
        self.tickers = self.parseInput(stockTickerOrFile)
        self.intrinioResults = self.callIntrinioAPI(self.tickers)
        self.guruFocusResults = self.callGuruFocusAPI(self.tickers)        
        self.ticker = pd.DataFrame({'ticker' : self.tickers})
        
        apiResults = pd.concat([self.ticker.reset_index(drop = True), 
                                self.intrinioResults, 
                                self.guruFocusResults], axis = 1)

        apiResults = self.calcNewColumns(apiResults)
        
        apiResults = apiResults.reindex(['ticker', 
                                         'companyName',
                                         'marketCap',
                                         'lastPrice',
                                         'peadScore',
                                         'percentChange',
                                         'dollarVolume',
                                         'moveStrength',
                                         'volOverMC',
                                         '',
                                         '',
                                         '',
                                         '',
                                         'outstandingShares',
                                         '',
                                         'lastVolume',
                                         'avgVolume',], axis = 1)
        
        return self.renameColumns(apiResults)
    
    def renameColumns(self, apiResults):
        apiResults = apiResults.rename(index = int,
                                       columns = {"marketCap" : "marketCap(M)",
                                                  "lastVolume" : "lastVolume(delayed)",
                                                  "dollarVolume" : "dollarVolume(M)",
                                                  "volOverMC" : "dollarVol/MC(%)",
                                                  "lastPrice" : "lastPrice(delayed)",
                                                  "peadScore" : "PEAD"})
        return apiResults
    
    def calcNewColumns(self, dataFrame):
        
        dataFrame['peadScore'] = dataFrame.apply(
                lambda row: calc.PEAD(row['avgVolume'], 
                                      row['outstandingShares']), 
                                      axis = 1)
        
        dataFrame['marketCap'] = dataFrame.apply(
                lambda row: calc.mktCap(row['lastPrice'], 
                                        row['outstandingShares']), 
                                        axis = 1)
        
        dataFrame['dollarVolume'] = dataFrame.apply(
                lambda row: calc.dollarVol(row['lastPrice'], 
                                           row['lastVolume']), 
                                           axis = 1)
                
        dataFrame['volumeRatio'] = dataFrame.apply(
                lambda row: calc.volRatio(row['lastVolume'], 
                                          row['avgVolume']), 
                                          axis = 1)
                
        dataFrame['volOverMC'] = dataFrame.apply(
                lambda row: calc.volOverMC(row['lastVolume'], row['lastPrice'], 
                                           row['outstandingShares']),
                                           axis = 1)
                
        dataFrame['moveStrength'] = dataFrame.apply(
                lambda row: calc.moveStrength(row['lastPrice'],
                                              row['lastVolume'],
                                              row['outstandingShares'],
                                              row['avgVolume']),
                                              axis = 1)
        return dataFrame
    
   
        
    def callIntrinioAPI(self, tickers):
        base = "https://api.intrinio.com/"
        endpoint = "historical_data"
        numOfResults = "page_size=150"
        dataPoint = "volume"
        
        today = datetime.date.today()
        dayOfWeekOfToday = datetime.date.today().weekday()
        
        if dayOfWeekOfToday < 5:
          endDate = today - datetime.timedelta(days = 1)
        elif dayOfWeekOfToday == 5:
          endDate = today - datetime.timedelta(days = 2)
        elif dayOfWeekOfToday == 6:
          endDate = today - datetime.timedelta(days = 3)
        
        startDate = endDate - datetime.timedelta(days = 155)
        
        avgVolume = []
        
        for index in tickers:
            sequence = (base, endpoint, "?", numOfResults, "&ticker=", 
                        index, "&item=", dataPoint, "&start_date=", 
                        startDate.isoformat()[:10], "&end_date=", 
                        endDate.isoformat()[:10])
            url = "".join(sequence)
            response = requests.get(url, auth = (self.intrinioUserName,
                                                 self.intrinioPassword))
            if response.status_code == 401: 
                errorMessage = "Check your Intrinio username or password" 
                raise Exception(errorMessage)
            
            volumeData = response.json()['data']
            
            if len(volumeData) == 0:
                print("Unable to retrieve avg volume data from Intrinio for " + index)
                avgVolume.append(0)
            else:
                totalVolume = 0
                for item in volumeData:
                    totalVolume = totalVolume + item['value']
                
                avgVolume.append(round(totalVolume/len(volumeData)))
        
        intrinioResults = pd.DataFrame({'avgVolume' : avgVolume})
        return intrinioResults
    
    def callGuruFocusAPI(self, tickers):
        base = "https://api.gurufocus.com/public/user/"
        endpoint = "summary"
        
        companyName = []
        lastVolume = []
        lastPrice = []
        percentChange = []
        outstandingShares = []
        
        for index in tickers:
            sequence = (base, self.guruFocusKey, "/stock/", 
                        index, "/", endpoint)
            url = "".join(sequence)
            response = requests.get(url)
    
            if response.status_code == 401: 
                errorMessage = "Check your username/password or API key" 
                raise Exception(errorMessage)
                
            summary = response.json()['summary']
            self.companyData = summary['company_data']
            
            if len(self.companyData) <= 2:
                print("Unable to retrieve company data from GuruFocus for " + index)
                companyName.append("")
                lastVolume.append(0)
                lastPrice.append(0)
                percentChange.append(0)
                outstandingShares.append(0)
            else:
                companyName.append(self.companyData['0'])
                lastVolume.append(int(float(self.companyData['volumn_day_total'])))
                lastPrice.append(float(self.companyData['price']))
                percentChange.append(round(float(self.companyData['p_pct_change'])/100, 4))
                outstandingShares.append(int(float(self.companyData['shares']) * 1000000))
            
        guruFocusResults = pd.DataFrame({'companyName' : companyName,
                                         'lastVolume' : lastVolume, 
                                        'lastPrice' : lastPrice,
                                        'percentChange' : percentChange,
                                        'outstandingShares' : outstandingShares})
        return guruFocusResults
