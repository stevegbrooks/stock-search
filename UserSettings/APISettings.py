#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 28 14:27:39 2018

@author: sgb
"""

class APISettings():
    settings = dict()
    histModeSettings = dict()
    referenceDate = ''
    
    def __init__(self, referenceDate):
        self.referenceDate = referenceDate
        
    def getDefaultSettings(self):
        return self.settings
        
    def getHistoricalSettings(self):
        self.histModeSettings['referenceDate'] = self.referenceDate
        return self.histModeSettings
    