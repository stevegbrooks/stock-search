#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 28 11:56:20 2018

@author: sgb
"""
import re
from Controller import Controller
from Utilities.FileWriter import FileWriter
from Utilities.FileReader import FileReader

class UserInterface:
    global c, fw, fr
    isHistoricalMode = False
    referenceDate = ''
    tickerInput = ''
    fileInput = False
    
    def __init__(self):
        self.fw = FileWriter()
        self.fr = FileReader()
    
    def setHistoricalMode(self, isHistoricalMode):
        if type(isHistoricalMode) is not bool:
            raise Exception("Error: the isHistoricalMode arg must be boolean ('True' or 'False')")
        self.isHistoricalMode = isHistoricalMode
    
    def setReferenceDate(self, referenceDate):
        if type(referenceDate) is not str:
            raise Exception("Error: the referenceDate arg must be a text string")
        self.referenceDate = referenceDate
    
    def setTickerInput(self, tickerInput):
        if type(tickerInput) is not str:
            raise Exception("Error: the tickers arg must be a text string")
        self.tickerInput = self.__handleTickerInput(tickerInput)
    
    def handleRequest(self):
        self.c = Controller(self.isHistoricalMode, 
                            self.referenceDate, 
                            self.tickerInput)
        return self.c.researchStocks()
    
    def displayResults(self, dataFrame, fileName):
        if self.fileInput == True:
            self.fw.writeToFile(dataFrame, fileName)
        else:
            print(dataFrame.loc[0])
            
    def __handleTickerInput(self, tickerInput):
        output = []
        match = re.search('\\.[a-zA-Z]*$', tickerInput, flags = 0)
        if match:
            if match.group(0) == '.xlsx' or match.group(0) == '.csv':
                self.fileInput = True
                columnNumber = 0
                output = self.fr.readExcelColumn(tickerInput, columnNumber)
            else:
                raise Exception('Currently only .xlsx and .csv files are supported.')
        else:
            output.append(tickerInput)
        return output