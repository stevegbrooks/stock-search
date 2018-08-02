#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  2 12:44:31 2018

@author: sgb
"""
import pandas as pd
from AlphaVantage.AlphaBehavior import AlphaBehavior

class AlphaBehavior_MovingAvg(AlphaBehavior):
    
    def __init__(self):
        super().__init__()
    
    def getStockData(self, baseURL, endpoint, ticker, outputSize, 
                     credentials, end_date, start_date):
        
        alphaData = super().getStockData(baseURL, endpoint, ticker, 
                         outputSize, credentials, end_date, start_date)
        
        if len(alphaData < 1):
            pass
        
        for i in alphaData:
            pass
        
        alphaVantageResults = pd.DataFrame()
        return alphaVantageResults