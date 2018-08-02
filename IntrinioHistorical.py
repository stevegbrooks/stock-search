"""
Objects from this class are built when the user specifies 'historical_data'
as their endpoint.

@author: sgb
"""

import pandas as pd
import requests
from StockAPICaller import StockAPICaller

class IntrinioHistorical(StockAPICaller):
    credentials = ''
    item = ''
    end_date = ''
    start_date = ''
    baseURL = 'https://api.intrinio.com/'
    numOfResults = '150'
    endpoint = 'historical_data'    
        
    def __init__(self, credentials, dataRequest):
        self.credentials = credentials
        self.dataRequest = dataRequest
        
    def getStockData(self, ticker):
        self.item = self.dataRequest['item']
        self.end_date = self.dataRequest['end_date']
        self.start_date = self.dataRequest['start_date']
        
        if self.end_date == self.start_date:
            self.numOfResults = '1'
        
        histData = []
        
        sequence = (self.baseURL, self.endpoint, '?', 
                    'page_size=', self.numOfResults, 
                    '&ticker=', ticker, '&item=', self.item, 
                    '&start_date=', self.start_date, 
                    '&end_date=', self.end_date)
        url = ''.join(sequence)
        response = requests.get(url, auth = (self.credentials[0],
                                             self.credentials[1]))
        if response.status_code != 200: 
            raise Exception('Check your Intrinio username or password or URL address') 
        
        jsonData = response.json()['data']
        
        if len(jsonData) == 0:
            print('Unable to retrieve ' + self.endpoint + ': ', 
                  self.item, ' data from Intrinio for ' + ticker)
            histData.append(0)
        else:
            if self.item == 'weightedavebasicsharesos':
                histData.append(int(jsonData[0]['value']))
            else:
                total = 0
                for i in jsonData:
                    total = total + i['value']
                if self.item == 'volume':
                    histData.append(round(total/len(jsonData)))
                else:
                    histData.append(round(total/len(jsonData), 2))
        
        if self.end_date != self.start_date:
            if self.item == 'weightedavebasicsharesos':
                colName = 'outstandingShares'
            else:
                colName = ['avg', self.item.capitalize(), '[', 
                           self.end_date, ':',
                           self.start_date, ']']
                colName = ''.join(colName)
        else:
            colName =  colName = [self.item, '[', 
                       self.end_date, ']']
            colName = ''.join(colName)
        
        intrinioResults = pd.DataFrame({'ticker' : ticker,
                                        colName : histData})
        
        return intrinioResults