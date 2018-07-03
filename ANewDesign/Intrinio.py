import StockAPICaller
import pandas as pd
import requests
import datetime

class Intrinio(StockAPICaller):
    base = "https://api.intrinio.com/"
    endpoint = ""
    numOfResults = ""
    dataPoint = ""
    
    username = ""
    password = ""
    
    def __init__(self, apiArgs):
        super.__init__()
    
    def specifyDataRequest(self, apiParameters):
        if apiParameters == "historical volume":
            self.endpoint = "historical_data"
            self.numOfResults = 150
            self.dataPoint = "volume"
        else:
            raise Exception("Only historical volume calls from Intrinio currently supported")
    
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
        
        avgVolume = []
        
        for index in tickers:
            sequence = (self.base, self.endpoint, "?", "page_size=", 
                        self.numOfResults, "&ticker=", index, "&item=", 
                        self.dataPoint, "&start_date=", 
                        startDate.isoformat()[:10], "&end_date=", 
                        endDate.isoformat()[:10])
            url = "".join(sequence)
            response = requests.get(url, auth = (self.username,
                                                 self.password))
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