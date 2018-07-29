#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 28 14:27:39 2018

@author: sgb
"""
from UserSettings.OutputManager import OutputManager
class AppSettings():
    global outputManager
    settings = dict()
    histModeSettings = dict()
    referenceDate = ''
    
    def __init__(self, referenceDate):
        self.referenceDate = referenceDate
        self.outputManger = OutputManager()
        
    def getDefaultSettings(self):
        return self.settings
        
    def getHistoricalSettings(self):
        self.histModeSettings['referenceDate'] = self.referenceDate
        return self.histModeSettings
    
    def getOutputManager(self):
        return self.outputManager
    