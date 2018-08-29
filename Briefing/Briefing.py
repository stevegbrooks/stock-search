#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 27 21:22:08 2018

@author: sgb
"""

from StockAPICaller import StockAPICaller
from Briefing.BriefingBehavior_Earnings import BriefingBehavior_Earnings

class Briefing(StockAPICaller):
    baseURL = 'https://www.briefing.com/InPlayEq/Search/ticker.htm?ticker='
    
    def __init__(self, credentials, dataRequest):
        self.credentials = credentials
        self.endpoint = dataRequest['endpoint']
        self.item = dataRequest['item']

        if self.endpoint == 'earnings':
            self._behavior = BriefingBehavior_Earnings()
    
    def getStockData(self, ticker):
        return self._behavior.getStockData(self.baseURL, self.endpoint, 
                                           ticker, self.credentials, self.item)