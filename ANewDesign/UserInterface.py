# -*- coding: utf-8 -*-
import pandas as pd
import re
from ANewDesign import StockAPIFactory as apiFactory
from ANewDesign.Utilities.FileReader import FileReader as fr
from ANewDesign.Utilities.FileWriter import FileWriter as fw
from ANewDesign.Utilities.Calculator import Calculator as calc

class UserInterface:
    
    stockAPICallers = []
    fileInput = False
    avgVolColName = ''
    histPriceColName = ''
    
    def __init__(self):
        self.stockAPICallers = []
    
    def specifyAPI(self, api, key, dataRequest):
        apiArgs = dict()
        apiArgs.__setitem__(api, key)
        self.stockAPICallers.append(
                apiFactory.StockAPIFactory.getAPI(apiFactory, 
                                                  apiArgs, 
                                                  dataRequest))
    
    def researchStocks(self, tickerInput):
        tickerInput = self.__parseTickerInput(tickerInput)
        stockData = pd.DataFrame()
        
        for caller in self.stockAPICallers:
            results = caller.getStockData(tickerInput)
            if len(stockData != 0):
                stockData = pd.merge(stockData, 
                                     results, 
                                     on = 'stockSymbol', 
                                     how = 'left')
            else:
                stockData = results
        
        symbolCol = stockData['stockSymbol']
        stockData.drop(labels = ['stockSymbol'], 
                       axis = 1, 
                       inplace = True)
        stockData.insert(0, 'stockSymbol', symbolCol)
        
        
        self.identifyColNames(stockData)        
        stockData = self.calcNewColumns(stockData)
        stockData = self.reindexColumns(stockData)
        return self.renameColumns(stockData)
    
    def calcNewColumns(self, dataFrame):
        dataFrame['peadScore'] = dataFrame.apply(
                lambda row: calc.PEAD(row[self.avgVolColName], 
                                      row['outstandingShares']), 
                                      axis = 1)
        dataFrame['marketCap'] = dataFrame.apply(
                lambda row: calc.mktCap(row['lastPrice'], 
                                        row['outstandingShares']), 
                                        axis = 1)
        dataFrame['dollarVolume'] = dataFrame.apply(
                lambda row: calc.dollarVol(row['lastPrice'], 
                                           row['lastVolume']), 
                                           axis = 1)
        dataFrame['volOverMC'] = dataFrame.apply(
                lambda row: calc.volOverMC(row['lastVolume'], row['lastPrice'], 
                                           row['outstandingShares']),
                                           axis = 1)
        dataFrame['moveStrength'] = dataFrame.apply(
                lambda row: calc.moveStrength(row['lastPrice'],
                                              row['lastVolume'],
                                              row['outstandingShares'],
                                              row[self.avgVolColName]),
                                              axis = 1)
        return dataFrame 
        
    def renameColumns(self, dataFrame):
        dataFrame = dataFrame.rename(index = int, 
                                     columns = {"marketCap" : "marketCap(M)", 
                                                "lastVolume" : "lastVolume(delayed)", 
                                                "dollarVolume" : "dollarVolume(M)", 
                                                "volOverMC" : "dollarVol/MC(%)", 
                                                "lastPrice" : "lastPrice(delayed)",
                                                "peadScore" : "PEAD"})
        return dataFrame
    
    def reindexColumns(self, dataFrame):
        newDataFrame = dataFrame.reindex(['stockSymbol', 'companyName', 'marketCap',
                                       'lastPrice', 'peadScore', 'percentChange',
                                       'dollarVolume', 'moveStrength', 'volOverMC',
                                       '', '', '', '', 'outstandingShares', '',
                                       'lastVolume',], axis = 1, copy = True)
    
        dataFrame = pd.merge(newDataFrame, 
                             dataFrame, 
                             on = list(filter(None, newDataFrame.columns.tolist())), 
                             how = 'left')
        
        return dataFrame
    
    def identifyColNames(self, dataFrame):
        colNames = dataFrame.columns.tolist()
        r = re.compile("(avgVolume[\\w\\W]*)")
        self.avgVolColName = list(filter(r.match, colNames))[0]
        r = re.compile("(close_price[\\w\\W]*)")
        self.histPriceColName = list(filter(r.match, colNames))[0]
    
    def writeToFile(self, dataFrame, fileName):
        match = re.search('\\.[a-zA-Z]*$', fileName, flags = 0)
        if match:
            if match.group(0) == '.xlsx':
                fw.writeToExcel(dataFrame, fileName)
            else:
                raise Exception('Currently only writing to .xlsx and .csv files is supported.')
        else:
            raise Exception('You did not provide a file extension - ' + 
                            'I dont know what kind of file to write to!')
    
    def __parseTickerInput(self, userInput):
        output = []
        match = re.search('\\.[a-zA-Z]*$', userInput, flags = 0)
        if match:
            if match.group(0) == '.xlsx' or match.group(0) == '.csv':
                self.fileInput = True
                columnNumber = 0
                output = fr.readExcelColumn(userInput, columnNumber)
            else:
                raise Exception('Currently only .xlsx and .csv files are supported.')
        else:
            output.append(userInput)
        
        return output
    

