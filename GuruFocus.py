# -*- coding: utf-8 -*-
import pandas as pd
import requests
from StockAPICaller import StockAPICaller

class GuruFocus(StockAPICaller):
    credentials = ''
    baseURL = 'https://api.gurufocus.com/public/user/'
    endpoint = ''
    
    def __init__(self, credentials, dataRequest):
        super().__init__(credentials, dataRequest)
        self.credentials = credentials
        self.endpoint = dataRequest['endpoint']
        
    def getStockData(self, ticker):
        companyName = []
        lastVolume = []
        lastPrice = []
        percentChange = []
        outstandingShares = []
        
        sequence = (self.baseURL, self.credentials, '/stock/', ticker, '/', self.endpoint)
        url = ''.join(map(str, sequence))
        response = requests.get(url)

        if response.status_code != 200: 
            errorMessage = 'Check your GuruFocus API key, or URL address' 
            raise Exception(errorMessage)
            
        summary = response.json()['summary']
        self.companyData = summary['company_data']
        
        if len(self.companyData) <= 2:
            print('Unable to retrieve company data from GuruFocus for ' + ticker)
            companyName.append('')
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
            
        guruFocusResults = pd.DataFrame({'ticker' : ticker,
                                         'name' : companyName,
                                         'lastVolume' : lastVolume,
                                         'lastPrice' : lastPrice,
                                         'percentChange' : percentChange,
                                         'outstandingShares' : outstandingShares})
        
        return guruFocusResults