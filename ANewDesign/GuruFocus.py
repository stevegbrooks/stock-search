# -*- coding: utf-8 -*-
import pandas as pd
import requests
from ANewDesign.StockAPICaller import StockAPICaller

class GuruFocus(StockAPICaller):
    credentials = ""
    baseURL = "https://api.gurufocus.com/public/user/"
    endpoint = ""
    
    def __init__(self, credentials, dataRequest):
        super().__init__(credentials, dataRequest)
        self.credentials = credentials
        self.__analyzeRequest(dataRequest)
        
    def __analyzeRequest(self, dataRequest):
        if dataRequest.get("endpoint") != "summary":
            raise Exception("Only the company summary data from GuruFocus are currently supported")
        else:
            self.endpoint = dataRequest.get("endpoint")

    def getStockData(self, tickers):
        stockSymbol = []
        companyName = []
        lastVolume = []
        lastPrice = []
        percentChange = []
        outstandingShares = []
        
        for ticker in tickers:
            stockSymbol.append(ticker)
            sequence = (self.baseURL, self.credentials, "/stock/", ticker, "/", self.endpoint)
            url = "".join(sequence)
            response = requests.get(url)
    
            if response.status_code != 200: 
                errorMessage = "Check your GuruFocus API key, or URL address" 
                raise Exception(errorMessage)
                
            summary = response.json()['summary']
            self.companyData = summary['company_data']
            
            if len(self.companyData) <= 2:
                print("Unable to retrieve company data from GuruFocus for " + ticker)
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
            
        guruFocusResults = pd.DataFrame({'stockSymbol' : stockSymbol,
                                         'companyName' : companyName,
                                         'lastVolume' : lastVolume,
                                         'lastPrice' : lastPrice,
                                         'percentChange' : percentChange,
                                         'outstandingShares' : outstandingShares})
        
        return guruFocusResults