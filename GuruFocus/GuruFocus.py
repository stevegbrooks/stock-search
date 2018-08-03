#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  2 19:29:14 2018

@author: sgb
"""
from StockAPICaller import StockAPICaller
from GuruFocus.GuruBehavior_Summary import GuruBehavior_Summary

class GuruFocus(StockAPICaller):
    baseURL = 'https://api.gurufocus.com/public/user/'
    
    def __init__(self, credentials, dataRequest):
        self.credentials = credentials
        self.endpoint = dataRequest['endpoint']
        self.item = dataRequest['item']
        
        if self.item == 'summary':
            self._behavior = GuruBehavior_Summary()
    
    def getStockData(self, ticker):
        return self._behavior.getStockData(self.baseURL, self.endpoint, ticker, self.credentials, self.item)