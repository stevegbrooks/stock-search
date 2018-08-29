#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 27 21:22:18 2018

@author: sgb
"""
from time import sleep
from WebCrawler import WebCrawler

class BriefingBehavior:
    
    def __init__(self):
        pass
    
    def getStockData(self, baseURL, endpoint, ticker, credentials, item):
        sequence = (baseURL, ticker, '&page=', endpoint, '&range=24')
        url = ''.join(map(str, sequence))
        
        wc = WebCrawler()
        
        if wc.connectToURL(url):
            sleep(2)
            html = wc.getDriver().page_source
        else:
            print('Error connecting to Briefing')
        
        return html
