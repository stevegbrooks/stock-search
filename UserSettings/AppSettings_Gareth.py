#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 28 13:12:20 2018

@author: sgb
"""
from UserSettings.AppSettings import AppSettings
from UserSettings.APIKeys_Gareth import APIKeys_Gareth
from UserSettings.OutputManager_Gareth import OutputManager_Gareth
from Utilities.DateAdjuster import DateAdjuster
from datetime import datetime, timedelta

class AppSettings_Gareth(AppSettings):
    
    global myAPIKeys, da, outputManager
    settings = dict()
    histModeSettings = dict()
    gfKey = ''
    intrinioKey = ''
    referenceDate = ''
    trailingDays = 155
    
    def __init__(self, referenceDate, isHistoricalMode):
        super().__init__(referenceDate)
        self.da = DateAdjuster()
        self.outputManager = OutputManager_Gareth()
        self.myAPIKeys = APIKeys_Gareth()
        self.gfKey = self.myAPIKeys.getGFKey()
        self.intrinioKey = self.myAPIKeys.getIntrinioKey()
        
        self.referenceDate = referenceDate
        
        self.setDefault()
        if isHistoricalMode:
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
        userSpecifiedDate = self.da.adjustDate(self.referenceDate, returnAsDate = True)
        dateAsString = datetime.strftime(userSpecifiedDate, '%Y-%m-%d')
        
        dayBeforeAsString = self.da.adjustDate(userSpecifiedDate - timedelta(days = 1), 
                                               returnAsDate = False)
        
        dayTrailingAsString = self.da.adjustDate(userSpecifiedDate - timedelta(days = self.trailingDays),
                                                 returnAsDate = False)

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
        
        def getOutputManager(self):
            return self.outputManager
        
        def setTrailingDays(self, trailingDays):
            if type(trailingDays) is not int:
                raise Exception("trailingDays must be an integer greater than 0")
            else:
                self.trailingDays = trailingDays
        