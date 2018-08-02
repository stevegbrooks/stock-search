#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  2 12:44:31 2018

@author: sgb
"""
import pandas as pd
from AlphaVantage.AlphaBehavior import AlphaBehavior

class AlphaBehavior_AvgVolume(AlphaBehavior):
    
    def __init__(self):
        super().__init__()
    
    def getStockData(self, baseURL, endpoint, ticker, outputSize, 
                     credentials, end_date, start_date):
        
        avgVolume = []
        alphaData = super().getStockData(baseURL, endpoint, ticker, 
                         outputSize, credentials, end_date, start_date)
        
        if len(alphaData < 1):
            avgVolume.append(0)
        
        totalVol = 0
        for i in alphaData:
            totalVol = totalVol + int(alphaData[i]['5. volume'])
        
        avgVolume.append(round(totalVol/len(alphaData)))
        
        colName = ['avgVolume', '[', end_date, ':', start_date, ']']
        colName = ''.join(colName)
        alphaVantageResults = pd.DataFrame({'ticker' : ticker,
                                            colName : avgVolume})
        return alphaVantageResults