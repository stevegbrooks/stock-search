# -*- coding: utf-8 -*-
import pandas as pd
import re
from datetime import datetime
from StockAPICaller import StockAPIFactory as apiFactory
from Secret import Secret
from Utilities.DateAdjuster import DateAdjuster
from Utilities.FileReader import FileReader as fr
from Utilities.FileWriter import FileWriter as fw
from Utilities.Calculator import Calculator as calc


class UserInterface:
    
    stockAPICallers = dict()
    fileInput = False
    isHistoricalMode = False
    trailingDays = 155
    userSpecifiedDate = ''
    avgVolColName = ''
    secret = Secret()
    dateAdjuster = DateAdjuster()
    
    def __init__(self):
        self.stockAPICallers = dict()
        self.secret = Secret()
        self.dateAdjuster = DateAdjuster()
    
    def specifyAPI(self, api, key, dataRequest):
        apiArgs = dict()
        apiArgs[api] = key
        dataRequest = self.validateDataRequest(api, dataRequest)
        self.stockAPICallers[api] = apiFactory.StockAPIFactory.getAPI(apiFactory, apiArgs, dataRequest)
    
    def researchStocks(self, tickerInput):
        tickerInput = self.__parseTickerInput(tickerInput)
        stockData = pd.DataFrame()
        
        if self.isHistoricalMode == False:
            stockData = self.callAPIs(tickerInput)
        else:
            self.userSpecifiedDate = self.getDateFromUser()
            self.stockAPICallers.clear()
            apiArgs = dict()
            intrinioKey = self.secret.getIntrinioKey()
            apiArgs['intrinio'] = intrinioKey
            histModeRequests = dict()
            #TODO - figure out how to handle 'historical mode'
            histModeRequests[len(histModeRequests)] = {'endpoint' : 'historical_data', 'item' : 'volume'}
            histModeRequests[len(histModeRequests)] = {'endpoint' : 'historical_data', 'item' : 'weightedavebasicsharesos'}
            histModeRequests[len(histModeRequests)] = {'endpoint' : 'historical_data', 'item' : 'close_price'}
            self.stockAPICallers[len(self.stockAPICallers)] = apiFactory.StockAPIFactory.getAPI(apiFactory, apiArgs, )
                
        self.identifyColNames(stockData)        
        stockData = self.calcNewColumns(stockData)
        stockData = self.reindexColumns(stockData)
        return self.renameColumns(stockData)
    
    def callAPIs(self, tickerInput):
        stockData = pd.DataFrame()
        for caller in self.stockAPICallers:
                results = self.stockAPICallers[caller].getStockData(tickerInput)
                if len(stockData != 0):
                    stockData = pd.merge(stockData, 
                                         results, 
                                         on = 'stockSymbol', 
                                         how = 'left')
                else:
                    stockData = results
        return stockData
    
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
    
    def getDateFromUser(self):
        switch = 1
        while switch == 1:
            date = input('Input a date as YYYY-MM-DD\n' 
                     + '--------------------------\n')
            try:
                date = datetime.strptime(date, '%Y-%m-%d')
                switch = 0
            except ValueError:
                print('Unrecognized date format, please try again\n')
        return date
    
    def validateDataRequest(self, api, dataRequest):
        if 'endpoint' not in dataRequest:
            raise Exception('You must provide an endpoint!')
        elif 'item' not in dataRequest and api == 'intrinio':
            raise Exception('You must provide an item when you call the Intrinio API!')
        else:
            if dataRequest['endpoint'] == 'historical_data':
                if 'start_date' in dataRequest and 'end_date' not in dataRequest:
                    raise Exception('If you provide a start_date, then you must also provide an end_date!')
                elif 'end_date' in dataRequest and 'start_date' not in dataRequest:
                    dataRequest['end_date'] = self.dateAdjuster.adjustForDayOfWeek(
                            dataRequest['end_date'], 
                            dataRequest['item']
                            )
                elif 'end_date' not in dataRequest and 'start_date' not in dataRequest:
                    dataRequest['end_date'] = self.dateAdjuster.defineEndDate(dataRequest['item'])
       
                dataRequest['start_date'] = self.dateAdjuster.defineStartDate(dataRequest['end_date'])
            
            elif dataRequest['endpoint'] == 'data_point':
                if 'end_date' in dataRequest or 'start_date' in dataRequest:
                    raise Exception("The 'data_point' endpoint does not take in dates" + 
                                    " - it provides current data!")
        
        return dataRequest

        
        

