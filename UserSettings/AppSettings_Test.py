#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  2 10:26:29 2018

@author: sgb
"""

from UserSettings.AppSettings import AppSettings
from UserSettings.APIKeys_Test import APIKeys_Test
from UserSettings.OutputManager_Test import OutputManager_Test
from Utilities.DateAdjuster import DateAdjuster
from datetime import datetime, timedelta, date

class AppSettings_Test(AppSettings):
    
    settings = dict()
    histModeSettings = dict()
    avTrailingDays = 155
    osTrailingDays = 165
    
    def __init__(self, referenceDate, isHistoricalMode):
        self.da = DateAdjuster()
        self.outputManager = OutputManager_Test()
        
        self.myAPIKeys = APIKeys_Test()
        self.aVKey = self.myAPIKeys.getAlphaVantageKey()
        self.gfKey = self.myAPIKeys.getGFKey()
        self.intrinioKey = self.myAPIKeys.getIntrinioKey()
        self.briefingKey = self.myAPIKeys.getBriefingKey()
        
        self.referenceDate = referenceDate
        
        if isHistoricalMode:
            self.isHistoricalMode = isHistoricalMode
            self.userSpecifiedDate = self.da.adjustDate(self.referenceDate, returnAsDate = True)
        else:
            today = date.today()
            self.userSpecifiedDate = self.da.adjustDate(today, returnAsDate = True)
        
        self.userDateAsString = datetime.strftime(self.userSpecifiedDate, '%Y-%m-%d')
        self.dayBeforeAsString = self.da.adjustDate(self.userSpecifiedDate - timedelta(
                days = 1), returnAsDate = False)
        self.avTrailing = self.da.adjustDate(self.userSpecifiedDate - timedelta(
            days = self.avTrailingDays), returnAsDate = False)
        self.osTrailing = self.da.adjustDate(self.userSpecifiedDate - timedelta(
            days = self.osTrailingDays), returnAsDate = False)
        
        self.setDefault()
        self.setHistorical()
    
    def setDefault(self):
        
        self.settings['briefing'] = {'api' : 'briefing',
                     'key' : self.briefingKey,
                     'dataRequest' : {'endpoint' : 'earnings',
                                      'item' : 'summary'}}

#        self.settings['alphaVol'] = {'api' : 'alphavantage', 
#                      'key' : self.aVKey, 
#                      'dataRequest' : {'endpoint' : 'TIME_SERIES_DAILY',
#                                       'item' : 'volume'}}
#        
#        self.settings['alphaSumm'] = {'api' : 'alphavantage', 
#                     'key' : self.aVKey, 
#                     'dataRequest' : {'endpoint' : 'TIME_SERIES_DAILY',
#                                      'item' : 'summary'}}
        
#        self.settings['intrinio'] = {'api' : 'intrinio', 
#                      'key' : self.intrinioKey, 
#                      'dataRequest' : {'endpoint' : 'historical_data', 
#                                       'item' : 'weightedavebasicsharesos',
#                                       'end_date' : self.userDateAsString,
#                                       'start_date' : self.osTrailing}}
#        
#        self.settings['gurufocus'] = {'api' : 'gurufocus', 
#                      'key' : self.gfKey, 
#                      'dataRequest' : {'endpoint' : 'summary',
#                                       'item' : 'summary'}}
    
    def setHistorical(self):
        
        self.histModeSettings['referenceDate'] = self.userDateAsString
        
#        self.histModeSettings['alphaVol'] = {'api' : 'alphavantage', 
#                      'key' : self.aVKey, 
#                      'dataRequest' : {'endpoint' : 'TIME_SERIES_DAILY',
#                                       'item' : 'volume',
#                                       'end_date' : self.userDateAsString,
#                                       'start_date' : self.avTrailing}}
#        
#        self.histModeSettings['alphaSumm'] = {'api' : 'alphavantage', 
#                     'key' : self.aVKey, 
#                     'dataRequest' : {'endpoint' : 'TIME_SERIES_DAILY',
#                                      'item' : 'summary',
#                                      'end_date' : self.userDateAsString,
#                                      'start_date' : self.userDateAsString}}
        
        self.histModeSettings['alphaMovingAvg'] = {'api' : 'alphavantage', 
                     'key' : self.aVKey, 
                     'dataRequest' : {'endpoint' : 'TIME_SERIES_DAILY',
                                      'item' : 'priceOutcome',
                                      'end_date' : self.userDateAsString,
                                      'start_date' : self.avTrailing}}
        
#        self.histModeSettings['intrinio'] = {'api' : 'intrinio', 
#                     'key' : self.intrinioKey, 
#                     'dataRequest' : {'endpoint' : 'historical_data', 
#                                      'item' : 'weightedavebasicsharesos',
#                                      'end_date' : self.userDateAsString,
#                                      'start_date' : self.osTrailing}}
        
    def getDefaultSettings(self):
        return self.settings
        
    def getHistoricalSettings(self):
        return self.histModeSettings
        
    def getOutputManager(self):
        return self.outputManager
        
        