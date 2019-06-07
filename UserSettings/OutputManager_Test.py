#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  2 10:26:54 2018

@author: sgb
"""

from UserSettings.OutputManager import OutputManager
from Utilities.Calculator import Calculator

class OutputManager_Test(OutputManager):
    
    def __init__(self):
        self.calc = Calculator()

    def calcNewColumns(self, dataFrame):
        return dataFrame
    
    def deleteExtraCols(self, dataFrame):
        return dataFrame
        
    def reindexColumns(self, dataFrame):
        return dataFrame
    
    def renameColumns(self, dataFrame):
        return dataFrame
    
    def identifyColNames(self, dataFrame):
        pass
    
    def setHistoricalMode(self, isHistoricalMode):
        self.isHistoricalMode = isHistoricalMode