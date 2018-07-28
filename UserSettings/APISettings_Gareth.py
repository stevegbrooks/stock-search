#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 28 13:12:20 2018

@author: sgb
"""
from UserSettings.APISettings import APISettings
from UserSettings.APIKeys_Gareth import APIKeys_Gareth
from Utilities.DateAdjuster import DateAdjuster
from datetime import datetime, timedelta

class APISettings_Gareth(APISettings):
    
    global myAPIKeys, dateAdjuster
    settings = dict()
    histModeSettings = dict()
    gfKey = ''
    intrinioKey = ''
    
    referenceDate = ''
    trailingDays = 155
    
    def __init__(self, referenceDate):
        super().__init__(referenceDate)
        self.dateAdjuster = DateAdjuster()
        self.myAPIKeys = APIKeys_Gareth()
        self.gfKey = self.myAPIKeys.getGFKey()
        self.intrinioKey = self.myAPIKeys.getIntrinioKey()
        
        self.referenceDate = referenceDate
        
        self.setDefault()
        self.setHistorical()
    
    def setDefault(self):
        self.settings['gurufocus'] = {'api' : 'gurufocus', 
                      'key' : self.gfKey, 
                      'dataRequest' : {'endpoint' : 'summary'}}
        self.settings['intrinio'] = {'api' : 'intrinio', 
                      'key' : self.intrinioKey, 
                      'dataRequest' : {'endpoint' : 'historical_data', 
                                       'item' : 'volume'}}
    
    def setHistorical(self):
        userSpecifiedDate = self.dateAdjuster.convertToDate(self.referenceDate)
        dateAsString = datetime.strftime(userSpecifiedDate, '%Y-%m-%d')
        
        dayBefore = userSpecifiedDate - timedelta(days = 1)
        dayBeforeAsString = datetime.strftime(dayBefore, '%Y-%m-%d')
        
        dayTrailing = userSpecifiedDate - timedelta(days = self.trailingDays)
        dayTrailingAsString = datetime.strftime(dayTrailing, '%Y-%m-%d')

        self.histModeSettings['referenceDate'] = dateAsString
        self.histModeSettings['avgVolume'] = {'api' : 'intrinio', 
                      'key' : self.intrinioKey, 
                      'dataRequest' : {'endpoint' : 'historical_data', 
                                       'item' : 'volume', 
                                       'end_date' : dateAsString,
                                       'start_date' : dayTrailingAsString}}
        
        self.histModeSettings['outstandingShares'] = {'api' : 'intrinio', 
                      'key' : self.intrinioKey, 
                      'dataRequest' : {'endpoint' : 'data_point', 
                                       'item' : 'weightedavebasicsharesos'}}
        
        self.histModeSettings['name'] = {'api' : 'intrinio', 
                      'key' : self.intrinioKey, 
                      'dataRequest' : {'endpoint' : 'data_point', 
                                       'item' : 'name'}}
        
        self.histModeSettings['lastPrice'] = {'api' : 'intrinio', 
                      'key' : self.intrinioKey, 
                      'dataRequest' : {'endpoint' : 'historical_data', 
                                       'item' : 'close_price', 
                                       'end_date' : dateAsString,
                                       'start_date' : dateAsString}}
        
        self.histModeSettings['lastPriceDayBefore'] = {'api' : 'intrinio', 
                      'key' : self.intrinioKey, 
                      'dataRequest' : {'endpoint' : 'historical_data', 
                                       'item' : 'close_price',
                                       'end_date' : dayBeforeAsString,
                                       'start_date' : dayBeforeAsString}}
        
        self.histModeSettings['lastVolume'] = {'api' : 'intrinio', 
                      'key' : self.intrinioKey, 
                      'dataRequest' : {'endpoint' : 'historical_data', 
                                       'item' : 'volume',
                                       'end_date' : dateAsString,
                                       'start_date' : dateAsString}}
        
        def getDefaultSettings(self):
            return self.settings
        
        def getHistoricalSettings(self):
            return self.histModeSettings
        
        def setTrailingDays(self, trailingDays):
            if type(trailingDays) is not int:
                raise Exception("trailingDays must be an integer greater than 0")
            else:
                self.trailingDays = trailingDays
        