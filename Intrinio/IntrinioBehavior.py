#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  2 18:19:58 2018

@author: sgb
"""

import requests

class IntrinioBehavior:
    
    def __init__(self):
        pass
    
    def getStockData(self, baseURL, endpoint, ticker, credentials, 
                     item, end_date, start_date):
        
        if end_date == start_date:
            self.numOfResults = '1'
        else:
            self.numOfResults = '150'
        
        sequence = (baseURL, endpoint, '?', 
                    'page_size=', self.numOfResults, 
                    '&ticker=', ticker, '&item=', item, 
                    '&start_date=', start_date, 
                    '&end_date=', end_date)
        url = ''.join(sequence)
        response = requests.get(url, auth = (credentials[0],
                                             credentials[1]))
        if response.status_code != 200: 
            errorMessage = 'Check your Intrinio username or password or URL address' 
            raise Exception(errorMessage)
        
        if endpoint == 'historical_data':
            data = response.json()['data']
        elif endpoint == 'data_point':
            data = response.json()['value']
        
        if (type(data) == str and data == 'na') or len(data) < 1:
            print('Unable to retrieve ' + endpoint + ': ', item, 
                  ' data from Intrinio for ' + ticker)
        
        return data