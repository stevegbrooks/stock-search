import pandas as pd
import requests
from ANewDesign.StockAPICaller import StockAPICaller

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
    
    def getStockData(self, tickers):
        
        stockSymbol = []
        currentData = []
        for ticker in tickers:
            stockSymbol.append(ticker)
            sequence = (self.baseURL, self.endpoint, 
                        '?identifier=', ticker, 
                        '&item=', self.item)
            url = ''.join(sequence)
            response = requests.get(url, auth = (self.credentials[0],
                                                 self.credentials[1]))
            if response.status_code != 200: 
                errorMessage = 'Check your Intrinio username or password or URL address' 
                raise Exception(errorMessage)
            
            jsonData = response.json()['data']
            
            if len(jsonData) == 0:
                print('Unable to retrieve ' + self.endpoint + ': ', self.item, 
                      ' data from Intrinio for ' + ticker)
                currentData.append(0)
            else:
                #TODO - figure out how to get data from intrinio when 'data_point' is passed 
                pass
        
        return pd.DataFrame({'stockSymbol' : stockSymbol, self.item : currentData})
