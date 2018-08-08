#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Takes in input from the UserInterface and builds the appropriate StockAPICaller
objects. These objects then send the data requests from the user (see UserSettings) 
to the APIs and returns the raw data.

The controller sends this raw data back to the UserInterface/OutputManager classes
for processing.

Most important function here is 'validateDataRequest()', which makes sure that not only
does the StockAPICaller object only recieve syntacitcally valid input, but also
semantically valid input. Some of the semantic responsibilities are shared with the 
UserSettings.AppSettings class, which is more specific to the user's needs.

@author: sgb
"""
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
        """
        The constructor takes in the historical mode bool, an AppSettings object,
        and a ticker symbol. It then grabs the api specs based on whether
        or not historical mode is true and passes it to the specifyAPI() method.
        """
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
            self._specifyAPI(self.settings[i]['api'], 
                            self.settings[i]['key'], 
                            self.settings[i]['dataRequest']) 
        
    def _specifyAPI(self, api, key, dataRequest):
        """
        Makes sure the api specs are formatted and specified properly with
        'validateDataRequest()', and then retrieves the appropriate StockAPICaller 
        objects from the factory.
        """
        apiArgs = dict()
        apiArgs[api] = key
        dataRequest = self._validateDataRequest(api, dataRequest)
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
    
    def _validateDataRequest(self, api, dataRequest):
        """
        Raises exceptions if there data requests are specified improperly.
        Allows for specifying the historical_data requests incompletely by having 
        default behavior, i.e. it uses today as the end_date if end_date isn't specified.
        
        Adjusts dates based on day of week through the DateAdjuster class.
        """
        
        if 'endpoint' not in dataRequest:
            raise Exception('You must provide an endpoint!')
        elif 'item' not in dataRequest and api == 'intrinio':
            raise Exception('You must provide an item when you call the Intrinio API!')
        else:
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

        
        

