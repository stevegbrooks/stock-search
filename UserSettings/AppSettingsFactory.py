#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 28 14:25:04 2018

@author: sgb
"""

from UserSettings.AppSettings_Gareth import AppSettings_Gareth

class AppSettingsFactory:
    
    apiSettings = dict()
    
    def getAppSettings(self, desiredSettings, isHistoricalMode, referenceDate):
        if desiredSettings == 'garethsSettings':
            return AppSettings_Gareth(isHistoricalMode, referenceDate)
        else:
            raise Exception('Settings file not found for ' + desiredSettings)