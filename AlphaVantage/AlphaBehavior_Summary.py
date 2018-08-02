#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  2 12:44:31 2018

@author: sgb
"""
import pandas as pd
from AlphaVantage.AlphaBehavior import AlphaBehavior

class AlphaBehavior_Summary(AlphaBehavior):
    
    def __init__(self):
        super().__init__()
    
    def getStockData(self, baseURL, endpoint, ticker, outputSize, credentials, end_date, start_date):
        lastVolume = []
        lastPrice = []
        percentChange = []
        
        alphaData = super().getStockData(baseURL, endpoint, ticker, 
                         outputSize, credentials, end_date, start_date)
        
        if len(alphaData < 1):
            lastVolume.append(0)
            lastPrice.append(0)
            percentChange.append(0)
        else:
            lastVolume.append(int(float(alphaData[0]['5. volume'])))
            lastPrice.append(float(alphaData[0]['4. close']))
            percentChange.append(self.calc.getPercentChange(float(alphaData[0]), float(alphaData[1])))
        
        alphaVantageResults = pd.DataFrame({'ticker' : ticker,
                                            'lastVolume' : lastVolume,
                                            'lastPrice' : lastPrice,
                                            'percentChange' : percentChange})
        return alphaVantageResults