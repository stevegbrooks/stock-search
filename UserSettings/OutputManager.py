#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 28 19:19:32 2018

@author: sgb
"""

class OutputManager:
    global isHistoricalMode
    
    def __init__(self):
        pass
    
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