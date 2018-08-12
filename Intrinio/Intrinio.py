"""
@author: sgb
"""

from StockAPICaller import StockAPICaller
from Intrinio.IntrinioBehavior_Historical import IntrinioBehavior_Historical
from Intrinio.IntrinioBehavior_20DayAvg import IntrinioBehavior_20DayAvg
from Intrinio.IntrinioBehavior_Current import IntrinioBehavior_Current

class Intrinio(StockAPICaller):
    baseURL = 'https://api.intrinio.com/'
        
    def __init__(self, credentials, dataRequest):
        self.credentials = credentials
        self.endpoint = dataRequest['endpoint']
        self.end_date = dataRequest['end_date']
        self.start_date = dataRequest['start_date']
        self.item = dataRequest['item']
        
        if self.endpoint == 'historical_data':
            if self.item == '20DayAvg':
                self._behavior = IntrinioBehavior_20DayAvg()
            else:
                self._behavior = IntrinioBehavior_Historical()
        elif self.endpoint == 'data_point':
            self._behavior = IntrinioBehavior_Current()
    
    def getStockData(self, ticker):
        return self._behavior.getStockData(self.baseURL, self.endpoint, ticker, 
                                           self.credentials, self.item, 
                                           self.end_date, self.start_date)
        