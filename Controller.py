# -*- coding: utf-8 -*-
import pandas as pd
import re
from datetime import datetime
from StockAPIFactory import StockAPIFactory as apiFactory
from Utilities.DateAdjuster import DateAdjuster
from Utilities.Calculator import Calculator

class Controller:
    global calc, datAdjuster
    
    tickerInput = []
    stockAPICallers = dict()
    fileInput = False
    isHistoricalMode = False
    
    referenceDate = ''
    trailingDays = 155
    userSpecifiedDate = ''
    
    settings = dict()
    
    avgVolColName = ''
    avgVolEndDate = ''
    avgVolStartDate = ''
    histVolColName = ''
    closePriceColName1 = ''
    closePriceColName2 = ''
    
    def __init__(self, isHistoricalMode, APISettings, tickerInput):
        self.dateAdjuster = DateAdjuster()
        self.calc = Calculator()
        self.isHistoricalMode = isHistoricalMode
        if isHistoricalMode is True:
            self.settings = APISettings.getHistoricalSettings()
            self.referenceDate = self.settings.pop('referenceDate')
        else:
            self.settings = APISettings.getDefaultSettings()
            self.referenceDate = self.dateAdjuster.adjustForDayOfWeek(datetime.today(), 'referenceDate')
        self.tickerInput = tickerInput
        
        for i in self.settings:
            self.specifyAPI(self.settings[i]['api'], 
                            self.settings[i]['key'], 
                            self.settings[i]['dataRequest']) 
        
    def specifyAPI(self, api, key, dataRequest):
        apiArgs = dict()
        apiArgs[api] = key
        dataRequest = self.validateDataRequest(api, dataRequest)
        self.stockAPICallers[len(self.stockAPICallers)] = apiFactory.getAPI(apiFactory, 
                             apiArgs, dataRequest)
    
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
                                          'stockSymbol', 'name', 'marketCap', 'lastPrice', 
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
    
#    def getDateFromUser(self):
#        switch = 1
#        while switch == 1:
#            date = input('Input a date as YYYY-MM-DD\n' 
#                     + '--------------------------\n')
#            try:
#                date = datetime.strptime(date, '%Y-%m-%d')
#                switch = 0
#            except ValueError:
#                print('Unrecognized date format, please try again\n')
#        return date
    
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

        
        

