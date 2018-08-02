"""
Builds the appropriate StockAPICallers based on input from the Controller.

@author: sgb
"""

from GuruFocus import GuruFocus
from IntrinioHistorical import IntrinioHistorical
from Intrinio import Intrinio
from AlphaVantage.AlphaVantage import AlphaVantage

class StockAPIFactory:
    
    apiArgs = dict()
    
    def getAPI(self, apiArgs, dataRequest):
        
        if apiArgs.__contains__('gurufocus'):
            return GuruFocus(credentials = apiArgs.get('gurufocus'), 
                             dataRequest = dataRequest)
        elif apiArgs.__contains__('intrinio'):
            if dataRequest['endpoint'] == 'historical_data':
                return IntrinioHistorical(credentials = apiArgs.get('intrinio'), 
                                          dataRequest = dataRequest)
            elif dataRequest['endpoint'] == 'data_point':
                return Intrinio(credentials = apiArgs.get('intrinio'), 
                                dataRequest = dataRequest)
        elif apiArgs.__contains__('alphavantage'):
            return AlphaVantage(credentials = apiArgs.get('alphavantage'), 
                                dataRequest = dataRequest)
        
        else:
            raise Exception('Currently only Intrinio, AlphaVantage, and GuruFocus APIs are supported.')

    