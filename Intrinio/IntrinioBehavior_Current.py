#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  2 18:41:06 2018

@author: sgb
"""

import pandas as pd
from Intrinio.IntrinioBehavior import IntrinioBehavior

class IntrinioBehavior_Current(IntrinioBehavior):
    
    def __init__(self):
        super().__init__()
    
    def getStockData(self, baseURL, endpoint, ticker, credentials, item,
                     end_date, start_date):
        
        intrinioData = super().getStockData(baseURL, endpoint, ticker, 
                         credentials, item, end_date, start_date)
        
        output = []
        
        if intrinioData == 'na':
            print('Unable to retrieve ' + endpoint + ': ', item, 
                  ' data from Intrinio for ' + ticker)
            output.append(float('nan'))
        else:
            if item == 'weightedavebasicsharesos':
                output.append(int(intrinioData))
            else:
                output.append(intrinioData)
        
        if item == 'weightedavebasicsharesos':
            colName = 'outstandingShares'
        else:
            colName = item
    
        return pd.DataFrame({'ticker' : ticker, colName : output})