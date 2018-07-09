import pandas as pd
import requests
from datetime import datetime, timedelta, date
from ANewDesign.StockAPICaller import StockAPICaller

class Intrinio(StockAPICaller):
    credentials = ""
    baseURL = "https://api.intrinio.com/"
    numOfResults = "150"
    endpoint = ""
    item = ""
    end_date = ""
    start_date = ""
        
    def __init__(self, credentials, dataRequest):
        super().__init__(credentials, dataRequest)
        self.credentials = credentials
        self.__analyzeRequest(dataRequest)
    
    def __analyzeRequest(self, dataRequest):
        if dataRequest.get("endpoint") != "historical_data":
            raise Exception("Only historical data from Intrinio currently supported")
        else:
            self.endpoint = dataRequest.get("endpoint")
            self.item = dataRequest.get("item")
            if self.endpoint == 'historical_data':
                if "end_date" in dataRequest:
                    self.end_date = dataRequest.get('end_date')
                else:
                    self.end_date = ""
                if "start_date" in dataRequest:
                    self.start_date = dataRequest.get('start_date')
                else:
                    self.start_date = ""
    
    def __determineStartDate(self):
        if len(self.start_date) == 0:
            self.start_date = self.end_date - timedelta(days = 155)
        else:
            self.start_date = datetime.strptime(self.start_date, '%Y-%m-%d')
    
    def __determineEndDate(self):
        if len(self.end_date) == 0:
            self.end_date = date.today()
        else:
            self.end_date = datetime.strptime(self.end_date, '%Y-%m-%d')
        
        if self.item == "volume":
            dayOfWeek = self.end_date.weekday()
            if dayOfWeek < 5:#mon-fri
                self.end_date = self.end_date - timedelta(days = 1)
            elif dayOfWeek == 5:#sat
                self.end_date = self.end_date - timedelta(days = 2)
            elif dayOfWeek == 6:#sun
                self.end_date = self.end_date - timedelta(days = 3)
    
    def getStockData(self, tickers):
        
        Intrinio.__determineEndDate(self)
        Intrinio.__determineStartDate(self)
        
        stockSymbol = []
        histData = []
        
        for ticker in tickers:
            stockSymbol.append(ticker)
            sequence = (self.baseURL, self.endpoint, "?", "page_size=", 
                        self.numOfResults, "&ticker=", ticker, "&item=", 
                        self.item, "&start_date=", 
                        self.start_date.isoformat()[:10], "&end_date=", 
                        self.end_date.isoformat()[:10])
            url = "".join(sequence)
            response = requests.get(url, auth = (self.credentials[0],
                                                 self.credentials[1]))
            if response.status_code != 200: 
                errorMessage = "Check your Intrinio username or password or URL address" 
                raise Exception(errorMessage)
            
            jsonData = response.json()['data']
            
            if len(jsonData) == 0:
                print("Unable to retrieve historical", self.item, "data from Intrinio for " + ticker)
                histData.append(0)
            else:
                total = 0
                for i in jsonData:
                    total = total + i['value']
                if self.item == "volume":
                    histData.append(round(total/len(jsonData)))
                else:
                    histData.append(round(total/len(jsonData), 2))
                
        colName = ['avg', self.item.capitalize(), "[", 
                   self.end_date.isoformat()[:10], ":",
                   self.start_date.isoformat()[:10], "]"]
        colName = "".join(colName)
        
        intrinioResults = pd.DataFrame({'stockSymbol' : stockSymbol,
                                        colName : histData})
        
        return intrinioResults