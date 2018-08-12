#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  2 12:44:31 2018

@author: sgb
"""
import pandas as pd
from datetime import datetime
from AlphaVantage.AlphaBehavior import AlphaBehavior
from Utilities.DateAdjuster import DateAdjuster

class AlphaBehavior_20DayAvg(AlphaBehavior):
    
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
                date.append(datetime.strftime(key, '%Y-%m-%d'))
            output = pd.DataFrame({'ticker' : ticker,
                                   'close_price' : close_price,
                                   '20Day_Avg_Date' : date})
            
            output['20Day_Avg'] = output['close_price'].rolling(20, min_periods = 1).mean()
            
            output = pd.DataFrame(output[['ticker', 
                                          '20Day_Avg', 
                                          '20Day_Avg_Date']].iloc[len(output)-1]).T
        else:
            print('Unable to retrieve 20-day moving average from AlphaVantage for ' + ticker)
    
        return output