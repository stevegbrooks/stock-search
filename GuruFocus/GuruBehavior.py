#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  2 19:29:04 2018

@author: sgb
"""
import requests

class GuruBehavior:
    
    def __init__(self):
        pass
    
    def getStockData(self, baseURL, endpoint, ticker, credentials, item):
        
        sequence = (baseURL, credentials, '/stock/', ticker, '/', endpoint)
        url = ''.join(map(str, sequence))
        response = requests.get(url)

        if response.status_code != 200: 
            errorMessage = 'Check your GuruFocus API key, or URL address' 
            raise Exception(errorMessage)
            
        summary = response.json()['summary']
        data = summary['company_data']
        
        if len(data) <= 2:
            print('Unable to retrieve company data from GuruFocus for ' + ticker)
        
        return data