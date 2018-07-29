# -*- coding: utf-8 -*-
import pandas as pd
from datetime import datetime
from StockAPIFactory import StockAPIFactory as apiFactory
from Utilities.DateAdjuster import DateAdjuster

class Controller:
    global da
    
    tickerInput = []
    stockAPICallers = dict()
    fileInput = False
    isHistoricalMode = False
    
    referenceDate = ''
    trailingDays = 155
    userSpecifiedDate = ''
    
    settings = dict()
    
    def __init__(self, isHistoricalMode, appSettings, tickerInput):
        self.stockAPICallers = dict()
        self.da = DateAdjuster()
        self.isHistoricalMode = isHistoricalMode
        if isHistoricalMode is True:
            self.settings = appSettings.getHistoricalSettings()
            self.referenceDate = self.settings.pop('referenceDate')
        else:
            self.settings = appSettings.getDefaultSettings()
            self.referenceDate = self.da.adjustDate(datetime.today(), 'referenceDate')
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
        apiData = pd.DataFrame()
        for caller in self.stockAPICallers:
                results = self.stockAPICallers[caller].getStockData(tickerInput)
                if len(apiData) != 0:
                    apiData = pd.merge(apiData, 
                                       results, on = 'ticker', how = 'left')
                else:
                    apiData = results
        return apiData
    
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
                    dataRequest['end_date'] = self.da.adjustDate(
                            dataRequest['end_date'], 
                            dataRequest['item']
                            )
                    dataRequest['start_date'] = self.da.defineStartDate(dataRequest['end_date'])
                elif 'end_date' not in dataRequest and 'start_date' not in dataRequest:
                    dataRequest['end_date'] = self.da.defineEndDate(dataRequest['item'])
                    dataRequest['start_date'] = self.da.defineStartDate(dataRequest['end_date'])
                elif 'end_date' in dataRequest and 'start_date' in dataRequest:
                    if dataRequest['end_date'] == dataRequest['start_date']:
                        dataRequest['end_date'] = self.da.adjustDate(
                                dataRequest['end_date'], 
                                'pointVolume')
                        dataRequest['start_date'] = self.da.adjustDate(
                                dataRequest['start_date'], 
                                'pointVolume')
                    else:
                        dataRequest['end_date'] = self.da.adjustDate(
                                dataRequest['end_date'], 
                                dataRequest['item'])
                        dataRequest['start_date'] = self.da.adjustDate(
                                dataRequest['start_date'], 
                                dataRequest['item'])
            elif dataRequest['endpoint'] == 'data_point':
                if 'end_date' in dataRequest or 'start_date' in dataRequest:
                    raise Exception("The 'data_point' endpoint does not take in dates" + 
                                    " - it provides current data!")
        
        return dataRequest

        
        

