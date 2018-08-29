#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UserInterface is the layer between the Controller and the user. It does basic 
checks on user input to make sure they are syntactically valid.

It handles the raw data output from the Controller according to user specs - OutputManager - 
and returns it to the user.

@author: sgb
"""
import re
from datetime import datetime, date
from Controller import Controller
from UserSettings.AppSettingsFactory import AppSettingsFactory
from Utilities.FileWriter import FileWriter
from Utilities.FileReader import FileReader

class UserInterface:
    isHistoricalMode = False
    
    def __init__(self):
        self.fw = FileWriter()
        self.fr = FileReader()
        self.asf = AppSettingsFactory()
    
    def runApplication(self, userSettingsProfile, isHistoricalMode, referenceDate, ticker):
        """
        This is the method that the user interacts with directly to retrieve stock data.
        """
        self.setAppSettings(userSettingsProfile, isHistoricalMode, referenceDate)
        self.setTickerInput(ticker)
        return self.handleRequest()
    
    def setAppSettings(self, userSettings, isHistoricalMode, referenceDate):
        """
        Sends parameters to the AppSettingsFactory and returns the appropriate 
        AppSettings object.
        """
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
        """
        Builds the Controller object, passes the relevant info, and calls the API with it.
        
        After that its cleaning the data based on UserSettings.OutputManager specs.
        
        It sets the referenceDate here outside of any other process to give the user feedback
        for what they entered, because the dates get shifted based on specs and day of week.
        """
        c = Controller(self.isHistoricalMode, self.appSettings, self.tickerInput)
        stockData = c.callAPIs(self.tickerInput)
                
        outputManager = self.appSettings.getOutputManager()
        outputManager.setHistoricalMode(self.isHistoricalMode)
        
        outputManager.identifyColNames(stockData)        
        stockData = outputManager.calcNewColumns(stockData)
        stockData = outputManager.deleteExtraCols(stockData)
        stockData['referenceDate'] = c.referenceDate
        stockData = outputManager.reindexColumns(stockData)
        stockData = outputManager.renameColumns(stockData)
        return stockData
    
    def printResults(self, dataFrame):
        self.fw.writeToFile(dataFrame, 'results.xlsx')
            
    def readTickerInput(self, userInput):
        output = userInput
        match = re.search('\\.[a-zA-Z]*$', userInput, flags = 0)
        if match:
            if match.group(0) == '.xlsx' or match.group(0) == '.csv':
                output = self.fr.readExcel(userInput)
            else:
                raise Exception('Currently only .xlsx and .csv files are supported.')
        return output
