"""
Objects from this class are built when the user specifies 'historical_data'
as their endpoint and '20DayAvg' as their item.

@author: sgb
"""

import pandas as pd
from Intrinio.IntrinioBehavior import IntrinioBehavior
from Utilities.DateAdjuster import DateAdjuster

class IntrinioBehavior_20DayAvg(IntrinioBehavior):
    
    def __init__(self):
        super().__init__()
        self.item = 'close_price'
        self.da = DateAdjuster()
        
    def getStockData(self, baseURL, endpoint, ticker, credentials, item,
                     end_date, start_date):
        
        intrinioData = super().getStockData(baseURL, endpoint, ticker, credentials, self.item, 
                            end_date, start_date)
        
        output = pd.DataFrame()
        close_price = []
        date = []
        if len(intrinioData) == 0:
            close_price.append(float('nan'))
            date.append(float('nan'))
            output = pd.DataFrame({'ticker' : ticker,
                                   '20Day_Avg' : close_price,
                                   '20Day_Avg_EndDate' : ''})
            print('Unable to retrieve 20-day moving average from Intrinio for ' + ticker)
        else:
            for i in reversed(intrinioData):
                close_price.append(float(i['value']))
                date.append(self.da.convertToDate(i['date']))
            
            output = pd.DataFrame({'ticker' : ticker,
                                   'close_price' : close_price,
                                   '20Day_Avg_EndDate' : date})
    
            output['20Day_Avg'] = output['close_price'].rolling(20, min_periods = 1).mean()
            
            output = pd.DataFrame(output[['ticker', 
                                          '20Day_Avg', 
                                          '20Day_Avg_EndDate']].iloc[len(output)-1]).T
        return output