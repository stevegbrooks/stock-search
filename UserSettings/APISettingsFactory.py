#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 28 14:25:04 2018

@author: sgb
"""

from UserSettings.APISettings_Gareth import APISettings_Gareth

class APISettingsFactory:
    
    apiSettings = dict()
    
    def getAPISettings(self, desiredSettings, referenceDate):
        if desiredSettings == 'garethsSettings':
            return APISettings_Gareth(referenceDate)
        else:
            raise Exception('Settings file not found for ' + desiredSettings)