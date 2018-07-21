# -*- coding: utf-8 -*-
import pandas as pd
import re
from datetime import datetime, timedelta
from StockAPIFactory import StockAPIFactory as apiFactory
from Secret import Secret
from Utilities.DateAdjuster import DateAdjuster
from Utilities.FileReader import FileReader as fr
from Utilities.FileWriter import FileWriter as fw
from Utilities.Calculator import Calculator as calc

class UserInterface:
    
    stockAPICallers = dict()
    fileInput = False
    isHistoricalMode = False
    historicalDate = ''
    trailingDays = 155
    userSpecifiedDate = ''
    avgVolColName = ''
    lastVolColName = ''
    closePriceColName1 = ''
    closePriceColName2 = ''
    secret = Secret()
    dateAdjuster = DateAdjuster()
    
    def __init__(self):
        self.stockAPICallers = dict()
        self.secret = Secret()
        self.dateAdjuster = DateAdjuster()
        gfKey = self.secret.getGFKey()
        intrinioKey = self.secret.getIntrinioKey()
        self.specifyAPI('gurufocus', gfKey, dataRequest = {'endpoint' : 'summary'})
        self.specifyAPI('intrinio', intrinioKey, dataRequest = {'endpoint' : 'historical_data', 
                                                                'item' : 'volume'})
    def specifyAPI(self, api, key, dataRequest):
        apiArgs = dict()
        apiArgs[api] = key
        dataRequest = self.validateDataRequest(api, dataRequest)
        self.stockAPICallers[len(self.stockAPICallers)] = apiFactory.getAPI(apiFactory, apiArgs, dataRequest)
    
    def researchStocks(self, tickerInput):
        tickerInput = self.__parseTickerInput(tickerInput)
        stockData = pd.DataFrame()
        
        if self.isHistoricalMode == False:
            stockData = self.callAPIs(tickerInput)
        else:
            self.userSpecifiedDate = self.dateAdjuster.convertToDate(self.historicalDate)
            dayBefore = self.userSpecifiedDate - timedelta(days = 1)
            dayBeforeAsString = datetime.strftime(dayBefore, '%Y-%m-%d')
            dateAsString = datetime.strftime(self.userSpecifiedDate, '%Y-%m-%d')
            
            self.stockAPICallers.clear()
            apiArgs = dict()
            intrinioKey = self.secret.getIntrinioKey()
            apiArgs['intrinio'] = intrinioKey
           
            histModeRequests = dict()
            histModeRequests['avgVolume'] = {'endpoint' : 'historical_data', 
                            'item' : 'volume', 
                            'end_date' : dateAsString}
            histModeRequests['outstandingShares'] = {'endpoint' : 'data_point', 
                            'item' : 'weightedavebasicsharesos'}
            histModeRequests['name'] = {'endpoint' : 'data_point', 
                            'item' : 'name'}
            histModeRequests['lastPrice'] = {'endpoint' : 'historical_data', 
                            'item' : 'close_price',
                            'end_date' : dateAsString,
                            'start_date' : dateAsString}
            histModeRequests['lastPriceDayBefore'] = {'endpoint' : 'historical_data', 
                            'item' : 'close_price',
                            'end_date' : dayBeforeAsString,
                            'start_date' : dayBeforeAsString}
            histModeRequests['lastVolume'] = {'endpoint' : 'historical_data', 
                            'item' : 'volume',
                            'end_date' : dateAsString,
                            'start_date' : dateAsString}
            for request in histModeRequests:
                self.specifyAPI('intrinio', intrinioKey, histModeRequests.get(request))
            
            stockData = self.callAPIs(tickerInput)
                
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
        if self.isHistoricalMode:
            dataFrame['lastPrice'] = dataFrame[self.closePriceColName1]
            dataFrame['percentChange'] = dataFrame.apply(
                    lambda row: calc.getPercentChange(row[self.closePriceColName1],
                                                      row[self.closePriceColName2]),
                                                      axis = 1)
            dataFrame['lastVolume'] = dataFrame[self.lastVolColName]
#            dataFrame.drop(columns = [self.closePriceColName1,
#                                      self.closePriceColName2,
#                                      self.lastVolColName], inplace = True)
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
                lambda row: calc.volOverMC(row['lastVolume'], 
                                           row['lastPrice'], 
                                           row['outstandingShares']),
                                           axis = 1)
        dataFrame['moveStrength'] = dataFrame.apply(
                lambda row: calc.moveStrength(row['lastPrice'],
                                              row['lastVolume'],
                                              row['outstandingShares'],
                                              row[self.avgVolColName]),
                                              axis = 1)
        return dataFrame 
        
    def reindexColumns(self, dataFrame):
        newDataFrame = dataFrame.reindex(['stockSymbol', 'name', 'marketCap',
                                       'lastPrice', 'peadScore', 'percentChange',
                                       'dollarVolume', 'moveStrength', 'volOverMC',
                                       '', '', '', '', 'outstandingShares', '',
                                       'lastVolume',], axis = 1, copy = True)
    
        dataFrame = pd.merge(newDataFrame, 
                             dataFrame, 
                             on = list(filter(None, newDataFrame.columns.tolist())), 
                             how = 'left')
        
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
    
    
    
    def identifyColNames(self, dataFrame):
        colNames = dataFrame.columns.tolist()
        r = re.compile("(avgVolume[\\w\\W]*)")
        self.avgVolColName = list(filter(r.match, colNames))[0]
        if self.isHistoricalMode:
            r = re.compile("([\\w\\W]*close_price[\\w\\W]*)")
            self.closePriceColName1 = list(filter(r.match, colNames))[0]
            self.closePriceColName2 = list(filter(r.match, colNames))[1]
            r = re.compile("(volume[\\w\\W]*)")
            self.lastVolColName = list(filter(r.match, colNames))[0]
    
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
                dayOfWeek = date.weekday()
                if dayOfWeek > 4: print('The date you entered falls on a weekend - percentChange will be 0.')
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
                    raise Exception('If you provide a start_date,' + 
                                    ' then you must also provide an end_date!')
                elif 'end_date' in dataRequest and 'start_date' not in dataRequest:
                    dataRequest['end_date'] = self.dateAdjuster.adjustForDayOfWeek(
                            dataRequest['end_date'], 
                            dataRequest['item']
                            )
                    dataRequest['start_date'] = self.dateAdjuster.defineStartDate(dataRequest['end_date'])
                elif 'end_date' not in dataRequest and 'start_date' not in dataRequest:
                    dataRequest['end_date'] = self.dateAdjuster.defineEndDate(dataRequest['item'])
                    dataRequest['start_date'] = self.dateAdjuster.defineStartDate(dataRequest['end_date'])
                elif 'end_date' in dataRequest and 'start_date' in dataRequest:
                    if dataRequest['end_date'] == dataRequest['start_date']:
                        dataRequest['end_date'] = self.dateAdjuster.adjustForDayOfWeek(
                                dataRequest['end_date'], 
                                'pointVolume')
                        dataRequest['start_date'] = self.dateAdjuster.adjustForDayOfWeek(
                                dataRequest['start_date'], 
                                'pointVolume')
                    else:
                        dataRequest['end_date'] = self.dateAdjuster.adjustForDayOfWeek(
                                dataRequest['end_date'], 
                                dataRequest['item'])
                        dataRequest['start_date'] = self.dateAdjuster.adjustForDayOfWeek(
                                dataRequest['start_date'], 
                                dataRequest['item'])
            elif dataRequest['endpoint'] == 'data_point':
                if 'end_date' in dataRequest or 'start_date' in dataRequest:
                    raise Exception("The 'data_point' endpoint does not take in dates" + 
                                    " - it provides current data!")
        
        return dataRequest

        
        

