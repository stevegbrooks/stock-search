#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  2 19:29:28 2018

@author: sgb
"""
import pandas as pd
from GuruFocus.GuruBehavior import GuruBehavior

class GuruBehavior_Summary(GuruBehavior):
    
    def __init__(self):
        super().__init__()
    
    def getStockData(self, baseURL, endpoint, ticker, credentials, item = ''):
        guruData = super().getStockData(baseURL, endpoint, ticker, credentials, item)
        
        companyName = []
        lastVolume = []
        lastPrice = []
        percentChange = []
        outstandingShares = []
        
        if len(guruData) <= 2:
            print('Unable to retrieve company data from GuruFocus for ' + ticker)
            companyName.append('')
            lastVolume.append(float('nan'))
            lastPrice.append(float('nan'))
            percentChange.append(float('nan'))
            outstandingShares.append(float('nan'))
        else:
            companyName.append(guruData['0'])
            lastVolume.append(int(float(guruData['volumn_day_total'])))
            lastPrice.append(float(guruData['price']))
            percentChange.append(round(float(guruData['p_pct_change'])/100, 4))
            outstandingShares.append(int(float(guruData['shares']) * 1000000))
            
        guruFocusResults = pd.DataFrame({'ticker' : ticker,
                                         'name' : companyName,
                                         'lastVolume' : lastVolume,
                                         'lastPrice' : lastPrice,
                                         'percentChange' : percentChange,
                                         'outstandingShares' : outstandingShares})
        
        return guruFocusResults