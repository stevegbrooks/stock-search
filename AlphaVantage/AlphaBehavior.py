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
        
        sequence = (baseURL, endpoint, '&symbol=', ticker, 
                    '&outputsize=', outputSize,
                    '&apikey=', credentials)
        url = ''.join(map(str, sequence))
        response = requests.get(url)
        
        if response.status_code != 200: 
            errorMessage = 'Check your AlphaVantage API key, or URL address' 
            raise Exception(errorMessage)
        
        for key in response.json():
            if key != 'Meta Data':
                timeSeries = response.json()[key]
        if type(timeSeries) is str:
        	raise Exception('calling alphaVantage too quickly, slow your roll bro')   
        values = list(timeSeries.values())
         
        endDateAsDate = self.da.convertToDate(end_date)
        startDateAsDate = self.da.convertToDate(start_date)
        
        data = dict()
        if len(timeSeries) < 1:
            print('Unable to retrieve company data from AlphaVantage for ' + ticker)
        else:
            if end_date == start_date:
                for index, date in enumerate(map(self.da.convertToDate, timeSeries.keys())):
                    if date <= endDateAsDate and date >= endDateAsDate - timedelta(days = 28):
                        data[date] = values[index]
            else:
                for index, date in enumerate(map(self.da.convertToDate, timeSeries.keys())):
                    if date <= endDateAsDate and date >= startDateAsDate:
                        data[date] = values[index]
        
        return data
