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
        wc.setDriverPath('chromedriver')
        wc.createDriver()
        wc.briefingLogin([credentials[0], credentials[1]])

        if wc.connectToURL(url):
            sleep(2)
            html = wc.getDriver().page_source
        else:
            raise Exception('Unable to connect to Briefing.com')
        
        wc.briefingLogout()
        wc.killDriver()
        
        return html
