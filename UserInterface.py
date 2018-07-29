#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 28 11:56:20 2018

@author: sgb
"""
import re
from datetime import datetime, date
from Controller import Controller
from UserSettings.AppSettingsFactory import AppSettingsFactory
from Utilities.FileWriter import FileWriter
from Utilities.FileReader import FileReader

class UserInterface:
    global c, fw, fr, asf, appSettings
    isHistoricalMode = False
    tickerInput = ''
    
    def __init__(self):
        self.fw = FileWriter()
        self.fr = FileReader()
        self.asf = AppSettingsFactory()
    
    def runApplication(self, userSettingsProfile, isHistoricalMode, referenceDate, ticker):
        self.setAppSettings(userSettingsProfile, isHistoricalMode, referenceDate)
        self.setTickerInput(ticker)
        return self.handleRequest()
    
    def setAppSettings(self, userSettings, isHistoricalMode, referenceDate):
        if type(referenceDate) is not str:
            raise Exception("Error: the referenceDate arg must be a text string")
        elif referenceDate == '':
            referenceDate = datetime.strftime(date.today(), '%Y-%m-%d')
        if type(isHistoricalMode) is not bool:
            raise Exception("Error: the isHistoricalMode arg must be boolean ('True' or 'False')")
        if type(userSettings) is not str:
            raise Exception("Error: the desiredSettings arg must be a text string")
        
        self.referenceDate = referenceDate
        self.isHistoricalMode = isHistoricalMode
        self.appSettings = self.asf.getAppSettings(userSettings, 
                                                   self.referenceDate, 
                                                   self.isHistoricalMode)
    
    def setTickerInput(self, tickerInput):
        if type(tickerInput) is not str:
            raise Exception("Error: the tickers arg must be a text string")
        self.tickerInput = tickerInput
    
    def handleRequest(self):
        self.c = Controller(self.isHistoricalMode, self.appSettings, self.tickerInput)
        stockData = self.c.callAPIs(self.tickerInput)
                
        outputManager = self.appSettings.getOutputManager()
        
        outputManager.setHistoricalMode(self.isHistoricalMode)
        outputManager.identifyColNames(stockData)        
        stockData = outputManager.calcNewColumns(stockData)
        stockData = outputManager.deleteExtraCols(stockData)
        
        stockData['referenceDate'] = self.c.referenceDate
        
        stockData = outputManager.reindexColumns(stockData)
        return outputManager.renameColumns(stockData)
    
    def printResults(self, dataFrame, fileName):
        self.fw.writeToFile(dataFrame, fileName)
            
    def readTickerInput(self, userInput):
        match = re.search('\\.[a-zA-Z]*$', userInput, flags = 0)
        if match:
            if match.group(0) == '.xlsx' or match.group(0) == '.csv':
                output = self.fr.readExcel(userInput)
            else:
                raise Exception('Currently only .xlsx and .csv files are supported.')
        return output
