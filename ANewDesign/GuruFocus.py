# -*- coding: utf-8 -*-
from ANewDesign.StockAPICaller import StockAPICaller
import pandas as pd
import requests

class GuruFocus(StockAPICaller):
    apiKey = ""
    baseURL = "https://api.gurufocus.com/public/user/"
    endpoint = "summary"
    
    def __init__(self, credentials):
        super.__init__()

    def getStockData(self, tickers):
        companyName = []
        lastVolume = []
        lastPrice = []
        percentChange = []
        outstandingShares = []
        
        for index in tickers:
            sequence = (self.base, self.apiKey, "/stock/", 
                        index, "/", self.endpoint)
            url = "".join(sequence)
            response = requests.get(url)
    
            if response.status_code == 401: 
                errorMessage = "Check your API key" 
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
                percentChange.append(float(self.companyData['p_pct_change']))
                outstandingShares.append(int(float(self.companyData['shares']) * 1000000))
            
        guruFocusResults = pd.DataFrame({'companyName' : companyName,
                                         'lastVolume' : lastVolume, 
                                        'lastPrice' : lastPrice,
                                        'percentChange' : percentChange,
                                        'outstandingShares' : outstandingShares})
        return guruFocusResults


