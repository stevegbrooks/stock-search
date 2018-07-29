#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 15 19:15:39 2018

@author: sgb
"""
from datetime import datetime, timedelta, date

class DateAdjuster:
    
    def adjustDate(self, date, item = 'refDate', returnAsDate = False):
        if type(date) == str:
            date = self.convertToDate(date)
        dayOfWeek = date.weekday()
        if item == 'volume':
            if dayOfWeek < 5:#mon-fri
                date = date - timedelta(days = 1)
            elif dayOfWeek == 5:#sat
                date = date - timedelta(days = 2)
            elif dayOfWeek == 6:#sun
                date = date - timedelta(days = 3)
        else:
            if dayOfWeek == 5:#sat
                date = date - timedelta(days = 1)
            elif dayOfWeek == 6:#sun
                date = date - timedelta(days = 2)
        if returnAsDate == True:
            return date
        else:
            return datetime.strftime(date, '%Y-%m-%d')
    
    def defineStartDate(self, end_date):
        end_date = self.convertToDate(end_date)
        start_date = end_date - timedelta(days = 155)
        return datetime.strftime(start_date, '%Y-%m-%d')
    
    def defineEndDate(self, item):
        end_date = date.today()
        return self.adjustDate(end_date, item)
        
    
    def convertToDate(self, dateString):
        try:
            date = datetime.strptime(dateString, '%Y-%m-%d')
            return date
        except ValueError:
            print(dateString + ' is in an unrecognized date format' + '\n')
           
        