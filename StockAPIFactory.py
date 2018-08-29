"""
Builds the appropriate StockAPICallers based on input from the Controller.

@author: sgb
"""
from AlphaVantage.AlphaVantage import AlphaVantage
from Briefing.Briefing import Briefing
from GuruFocus.GuruFocus import GuruFocus
from Intrinio.Intrinio import Intrinio
from Zacks.Zacks import Zacks


class StockAPIFactory:
    
    def getAPI(self, apiArgs, dataRequest):
        
        if apiArgs.__contains__('gurufocus'):
            return GuruFocus(credentials = apiArgs.get('gurufocus'), 
                             dataRequest = dataRequest)
        elif apiArgs.__contains__('intrinio'):
            return Intrinio(credentials = apiArgs.get('intrinio'),
                            dataRequest = dataRequest)
        elif apiArgs.__contains__('alphavantage'):
            return AlphaVantage(credentials = apiArgs.get('alphavantage'), 
                                dataRequest = dataRequest)
        elif apiArgs.__contains__('zacks'):
            return Zacks(dataRequest = dataRequest)
        elif apiArgs.__contains__('briefing'):
            return Briefing(credentials = apiArgs.get('briefing'),
                            dataRequest = dataRequest)
        else:
            raise Exception('Currently only ' + 
                            'Intrinio, AlphaVantage, GuruFocus, and Zacks ' +
                            'APIs are supported.')

    