#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 28 14:25:04 2018

@author: sgb
"""

from UserSettings.AppSettings_Gareth import AppSettings_Gareth
from UserSettings.AppSettings_Test import AppSettings_Test

class AppSettingsFactory:
    
    apiSettings = dict()
    
    def getAppSettings(self, desiredSettings, isHistoricalMode, referenceDate):
        if desiredSettings == 'garethsSettings':
            return AppSettings_Gareth(isHistoricalMode, referenceDate)
        elif desiredSettings == 'test':
            return AppSettings_Test(isHistoricalMode, referenceDate)
        else:
            raise Exception('Settings file not found for ' + desiredSettings)