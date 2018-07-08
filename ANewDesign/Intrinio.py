import pandas as pd
import requests
import datetime
from ANewDesign.StockAPICaller import StockAPICaller

class Intrinio(StockAPICaller):
    credentials = ""
    baseURL = ""
    endpoint = ""
    numOfResults = ""
    dataPoint = ""
        
    def __init__(self, credentials, dataRequest):
        super().__init__(credentials, dataRequest)
        self.credentials = credentials
        self.__analyzeRequest(dataRequest)
    
    def __analyzeRequest(self, dataRequest):
        if dataRequest != "historical volume":
            raise Exception("Only historical volume calls from Intrinio currently supported")
        else:
            self.endpoint = "historical_data"
            self.numOfResults = "150"
            self.dataPoint = "volume"
            
        self.baseURL = "https://api.intrinio.com/"
    
    def getStockData(self, tickers):
        
        today = datetime.date.today()
        dayOfWeekOfToday = datetime.date.today().weekday()
        
        if dayOfWeekOfToday < 5:
          endDate = today - datetime.timedelta(days = 1)
        elif dayOfWeekOfToday == 5:
          endDate = today - datetime.timedelta(days = 2)
        elif dayOfWeekOfToday == 6:
          endDate = today - datetime.timedelta(days = 3)
        
        startDate = endDate - datetime.timedelta(days = 155)
        
        stockSymbol = []
        avgVolume = []
        
        for ticker in tickers:
            stockSymbol.append(ticker)
            sequence = (self.baseURL, self.endpoint, "?", "page_size=", 
                        self.numOfResults, "&ticker=", ticker, "&item=", 
                        self.dataPoint, "&start_date=", 
                        startDate.isoformat()[:10], "&end_date=", 
                        endDate.isoformat()[:10])
            url = "".join(sequence)
            response = requests.get(url, auth = (self.credentials[0],
                                                 self.credentials[1]))
            if response.status_code != 200: 
                errorMessage = "Check your Intrinio username or password or URL address" 
                raise Exception(errorMessage)
            
            volumeData = response.json()['data']
            
            if len(volumeData) == 0:
                print("Unable to retrieve avg volume data from Intrinio for " + ticker)
                avgVolume.append(0)
            else:
                totalVolume = 0
                for item in volumeData:
                    totalVolume = totalVolume + item['value']
                
                avgVolume.append(round(totalVolume/len(volumeData)))
        
        intrinioResults = pd.DataFrame({'stockSymbol' : stockSymbol,
                                        'avgVolume' : avgVolume})
        
        return intrinioResults