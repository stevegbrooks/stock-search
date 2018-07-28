#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 28 11:56:20 2018

@author: sgb
"""
import re

from Controller import Controller
from UserSettings.APISettingsFactory import APISettingsFactory
from Utilities.FileWriter import FileWriter
from Utilities.FileReader import FileReader

class UserInterface:
    global c, fw, fr, asf
    isHistoricalMode = False
    tickerInput = ''
    fileInput = False
    APISettings = ''
    
    def __init__(self):
        self.fw = FileWriter()
        self.fr = FileReader()
        self.asf = APISettingsFactory()
    
    def setHistoricalMode(self, isHistoricalMode):
        if type(isHistoricalMode) is not bool:
            raise Exception("Error: the isHistoricalMode arg must be boolean ('True' or 'False')")
        self.isHistoricalMode = isHistoricalMode
    
    def setAPIs(self, userSettings, referenceDate):
        if type(referenceDate) is not str:
            raise Exception("Error: the referenceDate arg must be a text string")
        self.referenceDate = referenceDate
        if type(userSettings) is not str:
            raise Exception("Error: the desiredSettings arg must be a text string")
        
        self.APISettings = self.asf.getAPISettings(userSettings, self.referenceDate)
    
    def setTickerInput(self, tickerInput, justTickers = True):
        if type(tickerInput) is not str:
            raise Exception("Error: the tickers arg must be a text string")
        self.tickerInput = self.__handleTickerInput(tickerInput, justTickers)
    
    def handleRequest(self):
        self.c = Controller(self.isHistoricalMode,
                            self.APISettings,
                            self.tickerInput)
        stockData = self.c.callAPIs(self.tickerInput)
        #TODO After this line, all calls should be user-settings specific,
            #i.e. none of these calls should rely on Controller
        self.c.identifyColNames(stockData)        
        stockData = self.c.calcNewColumns(stockData)
        stockData = self.c.deleteExtraCols(stockData)
        stockData['referenceDate'] = self.c.referenceDate
        stockData = self.c.reindexColumns(stockData)
        return self.c.renameColumns(stockData)
    
    def displayResults(self, dataFrame, fileName):
        if self.fileInput == True:
            self.fw.writeToFile(dataFrame, fileName)
        else:
            print(dataFrame.loc[0])
            
    def __handleTickerInput(self, tickerInput, justTickers):
        match = re.search('\\.[a-zA-Z]*$', tickerInput, flags = 0)
        if match:
            if match.group(0) == '.xlsx' or match.group(0) == '.csv':
                self.fileInput = True
                if justTickers is True:
                    output = self.fr.readExcel(tickerInput).iloc[:,0]
                else:
                    output = self.fr.readExcel(tickerInput).iloc[:,0:2]
            else:
                raise Exception('Currently only .xlsx and .csv files are supported.')
        else:
            output.append(tickerInput)
        
        return output