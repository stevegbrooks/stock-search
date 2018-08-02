#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  2 12:33:29 2018

@author: sgb
"""
import requests
from datetime import timedelta
from Utilities.DateAdjuster import DateAdjuster

class AlphaBehavior:
    
    def __init__(self):
        self.da = DateAdjuster()
    
    def getStockData(self, baseURL, endpoint, ticker, outputSize, 
                     credentials, end_date, start_date):
        
        sequence = (self.baseURL, self.endpoint, '&symbol=', ticker, 
                    '&outputsize=', self.outputSize,
                    '&apikey=', self.credentials)
        url = ''.join(map(str, sequence))
        response = requests.get(url)
        
        if response.status_code != 200: 
            errorMessage = 'Check your AlphaVantage API key, or URL address' 
            raise Exception(errorMessage)
            
        timeSeries = list(response.json().values())[1]
        values = list(timeSeries.values())
         
        endDateAsDate = self.da.convertToDate(self.end_date)
        startDateAsDate = self.da.convertToDate(self.start_date)
        
        output = []
       
        if len(self.timeSeries) < 1:
            print('Unable to retrieve company data from AlphaVantage for ' + ticker)
        else:
            data = dict()
            if end_date == start_date:
                for index, date in enumerate(map(self.da.convertToDate, timeSeries.keys())):
                    if date <= endDateAsDate and date >= endDateAsDate - timedelta(days = 20):
                        data[date] = values[index]
                        output = sorted(data.values())
            else:
                for index, date in enumerate(map(self.da.convertToDate, timeSeries.keys())):
                    if date <= endDateAsDate and date >= startDateAsDate:
                        data[date] = values[index]
                        output = sorted(data.values())
        
        return output
