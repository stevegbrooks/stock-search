#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
The AppSettings class specifies to the Controller what data to grab from which APIs.

All of the user specific stuff should be in here. This class also manages the APIKeys
and creates the OutputManager object for the user.

@author: sgb
"""
from UserSettings.APIKeys import APIKeys
from UserSettings.OutputManager import OutputManager

class AppSettings():
    global outputManager, apiKeys
    settings = dict()
    histModeSettings = dict()
    referenceDate = ''
    
    def __init__(self, isHistoricalMode, referenceDate):
        self.referenceDate = referenceDate
        self.outputManger = OutputManager()
        self.apiKeys = APIKeys()
        
        if isHistoricalMode:
            self.setHistorical()
        
    def setDefault(self):
        pass
    
    def setHistorical(self):
        pass
        
    def getDefaultSettings(self):
        return self.settings
        
    def getHistoricalSettings(self):
        self.histModeSettings['referenceDate'] = self.referenceDate
        return self.histModeSettings
    
    def getOutputManager(self):
        return self.outputManager
    