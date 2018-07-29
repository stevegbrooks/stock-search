#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 28 19:12:16 2018

@author: sgb
"""
import pandas as pd
import re
from UserSettings.OutputManager import OutputManager
from Utilities.Calculator import Calculator

class OutputManager_Gareth(OutputManager):
    
    global calc, isHistoricalMode
    
    avgVolColName = ''
    avgVolEndDate = ''
    avgVolStartDate = ''
    closePriceColName1 = ''
    closePriceColName2 = ''
    histVolColName = ''
    
    
    def __init__(self):
        self.calc = Calculator()

    def calcNewColumns(self, dataFrame):
        if self.isHistoricalMode:
            dataFrame['lastPrice'] = dataFrame[self.closePriceColName1]
            dataFrame['percentChange'] = dataFrame.apply(
                    lambda row: self.calc.getPercentChange(row[self.closePriceColName1],
                                                           row[self.closePriceColName2]),
                                                           axis = 1)
            dataFrame['lastVolume'] = dataFrame[self.histVolColName]

        dataFrame['peadScore'] = dataFrame.apply(
                lambda row: self.calc.PEAD(row[self.avgVolColName], 
                                           row['outstandingShares']), 
                                           axis = 1)
        dataFrame['marketCap'] = dataFrame.apply(
                lambda row: self.calc.mktCap(row['lastPrice'], 
                                             row['outstandingShares']), 
                                             axis = 1)
        dataFrame['dollarVolume'] = dataFrame.apply(
                lambda row: self.calc.dollarVol(row['lastPrice'], 
                                                row['lastVolume']), 
                                                axis = 1)
        dataFrame['moveStrength'] = dataFrame.apply(
                lambda row: self.calc.moveStrength(row['lastPrice'],
                                                   row['lastVolume'],
                                                   row['outstandingShares'],
                                                   row[self.avgVolColName]),
                                                   axis = 1)
        dataFrame['avgVolEndDate'] = self.avgVolEndDate
        dataFrame['avgVolStartDate'] = self.avgVolStartDate
        return dataFrame
    
    def deleteExtraCols(self, dataFrame):
        if self.isHistoricalMode == True:
            dataFrame.drop([self.histVolColName, 
                            self.closePriceColName1, 
                            self.closePriceColName2], axis = 1, inplace = True)
        return dataFrame
        
    def reindexColumns(self, dataFrame):
        newDataFrame = dataFrame.reindex(['referenceDate', 'blank1', 'blank2', 'blank3',
                                          'ticker', 'name', 'marketCap', 'lastPrice', 
                                          'peadScore', 'percentChange', 'dollarVolume', 
                                          'moveStrength', 'blank4', 'blank5', 
                                          'outstandingShares', 'blank6',
                                          'lastVolume',], axis = 1, copy = True)  
        regex = re.compile("blank[0-9]{1}")
        withoutBlanks = filter(lambda i: not regex.search(i), 
                               newDataFrame.columns.tolist())
        dataFrame = pd.merge(newDataFrame, 
                             dataFrame, 
                             on = list(filter(None, withoutBlanks)), 
                             how = 'left')
        return dataFrame
    
    def renameColumns(self, dataFrame):
        dataFrame = dataFrame.rename(index = int, 
                                     columns = {"marketCap" : "marketCap(M)", 
                                                "lastVolume" : "lastVolume(delayed)", 
                                                "dollarVolume" : "dollarVolume(M)", 
                                                "lastPrice" : "lastPrice(delayed)",
                                                "peadScore" : "PEAD",
                                                self.avgVolColName : 'avgVolume'})
        return dataFrame
    
    def identifyColNames(self, dataFrame):
        colNames = dataFrame.columns.tolist()
        r = re.compile("(avgVolume[\\w\\W]*)")
        self.avgVolColName = list(filter(r.match, colNames))[0]
        s = pd.Series([self.avgVolColName])
        self.avgVolEndDate = s.str.extract('avgVolume\\[([\\w\\W]{10})', expand = False)[0]
        self.avgVolStartDate = s.str.extract('avgVolume\\[[\\w\\W]{10}\\:([\\w\\W]{10})', expand = False)[0]
        if self.isHistoricalMode:
            r = re.compile("([\\w\\W]*close_price[\\w\\W]*)")
            self.closePriceColName1 = list(filter(r.match, colNames))[0]
            self.closePriceColName2 = list(filter(r.match, colNames))[1]
            r = re.compile("(volume[\\w\\W]*)")
            self.histVolColName = list(filter(r.match, colNames))[0]
    
    def setHistoricalMode(self, isHistoricalMode):
        self.isHistoricalMode = isHistoricalMode