#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
The AppSettings class specifies to the Controller what data to grab from which APIs.

All of the user specific stuff should be in here. This class also manages the APIKeys
and creates the OutputManager object for the user.

@author: sgb
"""

class AppSettings():
    
    def setDefault(self):
        raise NotImplementedError("Please Implement this method")
    
    def setHistorical(self):
        raise NotImplementedError("Please Implement this method")
    
    def getDefaultSettings(self):
        raise NotImplementedError("Please Implement this method")
    
    def getHistoricalSettings(self):
        raise NotImplementedError("Please Implement this method")
    
    def getOutputManager(self):
        raise NotImplementedError("Please Implement this method")