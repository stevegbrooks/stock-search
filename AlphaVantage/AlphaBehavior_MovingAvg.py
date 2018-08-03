#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  2 12:44:31 2018

@author: sgb
"""
import pandas as pd
from AlphaVantage.AlphaBehavior import AlphaBehavior
from Utilities.DateAdjuster import DateAdjuster

class AlphaBehavior_MovingAvg(AlphaBehavior):
    
    def __init__(self):
        super().__init__()
        self.da = DateAdjuster()
    
    def getStockData(self, baseURL, endpoint, ticker, outputSize, 
                     credentials, end_date, start_date):
        
        alphaData = super().getStockData(baseURL, endpoint, ticker, 
                         outputSize, credentials, end_date, start_date)
        
        output = pd.DataFrame()
        if len(alphaData) > 0:
            close_price = []
            date = []
            for key, value in sorted(alphaData.items()):
                close_price.append(float(alphaData[key]['4. close']))
                date.append(key)
            output = pd.DataFrame({'ticker' : ticker,
                                      'close_price' : close_price,
                                      'date' : date})
        output['movingAvg'] = output['close_price'].rolling(10).mean()
    
        return output