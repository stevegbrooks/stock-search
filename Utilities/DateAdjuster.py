#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 15 19:15:39 2018

@author: sgb
"""
from datetime import datetime, timedelta, date

class DateAdjuster:
    
    def adjustForDayOfWeek(self, date, item, needToConvert = True):
        dayOfWeek = date.weekday()
        if needToConvert:
            date = self.convertToDate(date)
            
        if item == 'volume':
            if dayOfWeek < 5:#mon-fri
                date = date - timedelta(days = 1)
        if dayOfWeek == 5:#sat
            date = date - timedelta(days = 2)
        elif dayOfWeek == 6:#sun
            date = date - timedelta(days = 3)
        
        return datetime.strftime(date, '%Y-%m-%d')
    
    def defineStartDate(self, end_date):
        end_date = self.convertToDate(end_date)
        start_date = end_date - timedelta(days = 155)
        return datetime.strftime(start_date, '%Y-%m-%d')
    
    def defineEndDate(self, item):
        end_date = date.today()
        return self.adjustForDayOfWeek(end_date, item, needToConvert = False)
        
    
    def convertToDate(self, dateString):
        try:
            date = datetime.strptime(dateString, '%Y-%m-%d')
        except ValueError:
            print(dateString + ' is in an unrecognized date format' + '\n')
           
        return date