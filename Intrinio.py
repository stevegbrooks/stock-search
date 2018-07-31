"""
Objects from this class are built when the user specifies 'data_point'
as their endpoint.

@author: sgb
"""
import pandas as pd
import requests
from StockAPICaller import StockAPICaller

class Intrinio(StockAPICaller):
    dataRequest = dict()
    credentials = ''
    baseURL = 'https://api.intrinio.com/'
    endpoint = 'data_point'
    item = ''
        
    def __init__(self, credentials, dataRequest):
        super().__init__(credentials, dataRequest)
        self.credentials = credentials
        self.dataRequest = dataRequest
    
    def getStockData(self, ticker):
        self.item = self.dataRequest['item']
        currentData = []
        sequence = (self.baseURL, self.endpoint, 
                    '?identifier=', ticker, 
                    '&item=', self.item)
        url = ''.join(sequence)
        response = requests.get(url, auth = (self.credentials[0],
                                             self.credentials[1]))
        if response.status_code != 200: 
            errorMessage = 'Check your Intrinio username or password or URL address' 
            raise Exception(errorMessage)
        
        jsonData = response.json()['value']
        
        if jsonData == 'na':
            print('Unable to retrieve ' + self.endpoint + ': ', self.item, 
                  ' data from Intrinio for ' + ticker)
            currentData.append(0)
        else:
            if self.item == 'weightedavebasicsharesos':
                currentData.append(int(jsonData))
            else:
                currentData.append(jsonData)
        
        if self.item == 'weightedavebasicsharesos':
            colName = 'outstandingShares'
        else:
            colName = self.item
    
        return pd.DataFrame({'ticker' : ticker, colName : currentData})
