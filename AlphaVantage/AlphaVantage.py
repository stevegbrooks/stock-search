#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  2 10:54:35 2018

@author: sgb
"""
from StockAPICaller import StockAPICaller
from AlphaVantage.AlphaBehavior_AvgVolume import AlphaBehavior_AvgVolume
from AlphaVantage.AlphaBehavior_MovingAvg import AlphaBehavior_MovingAvg
from AlphaVantage.AlphaBehavior_Summary import AlphaBehavior_Summary

class AlphaVantage(StockAPICaller):
    baseURL = 'https://www.alphavantage.co/query?function='
    outputSize = 'full'
    
    def __init__(self, credentials, dataRequest):
        self.credentials = credentials
        self.endpoint = dataRequest['endpoint']
        self.end_date = dataRequest['end_date']
        self.start_date = dataRequest['start_date']
        self.item = dataRequest['item']
        
        if self.item == 'volume':
            self._behavior = AlphaBehavior_AvgVolume()
        elif self.item == 'summary':
            self._behavior = AlphaBehavior_Summary()
        elif self.item == 'movingavg':
            self._behavior = AlphaBehavior_MovingAvg()

    
    def getStockData(self, ticker):
        return self._behavior.getStockData(self.baseURL, self.endpoint,
                                           ticker, self.outputSize,
                                           self.credentials, self.end_date,
                                           self.start_date)
        