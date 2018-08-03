"""
Objects from this class are built when the user specifies 'historical_data'
as their endpoint.

@author: sgb
"""

import pandas as pd
from Intrinio.IntrinioBehavior import IntrinioBehavior

class IntrinioBehavior_Historical(IntrinioBehavior):
    
    def __init__(self):
        super().__init__()
    
    def getStockData(self, baseURL, endpoint, ticker, credentials, item,
                     end_date, start_date):
        
        intrinioData = super().getStockData(baseURL, endpoint, ticker, credentials, item, 
                            end_date, start_date)
        output = []
        
        if len(intrinioData) == 0:
            output.append(0)
        else:
            if item == 'weightedavebasicsharesos':
                output.append(int(intrinioData[0]['value']))
            else:
                total = 0
                for i in intrinioData:
                    total = total + i['value']
                if item == 'volume':
                    output.append(round(total/len(intrinioData)))
                else:
                    output.append(round(total/len(intrinioData), 2))
        
        if end_date != start_date:
            if item == 'weightedavebasicsharesos':
                colName = 'outstandingShares'
            else:
                colName = ['avg', item.capitalize(), '[', 
                           end_date, ':',
                           start_date, ']']
                colName = ''.join(colName)
        else:
            colName =  colName = [item, '[', 
                       end_date, ']']
            colName = ''.join(colName)
        
        intrinioResults = pd.DataFrame({'ticker' : ticker,
                                        colName : output})
        
        return intrinioResults