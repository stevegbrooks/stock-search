from ANewDesign.GuruFocus import GuruFocus
from ANewDesign.IntrinioHistorical import IntrinioHistorical
from ANewDesign.Intrinio import Intrinio

class StockAPIFactory:
    
    apiArgs = dict()
    
    def getAPI(self, apiArgs, dataRequest):
        
        if apiArgs.__contains__('gurufocus'):
            credentials = apiArgs.get('gurufocus')
            return GuruFocus(credentials, dataRequest)
        elif apiArgs.__contains__('intrinio'):
            credentials = apiArgs.get('intrinio')
            if dataRequest['endpoint'] == 'historical_data':
                return IntrinioHistorical(credentials, dataRequest)
            elif dataRequest['endpoint'] == 'data_point':
                return Intrinio(credentials, dataRequest)
        
        else:
            raise Exception('Currently only Intrinio, and GuruFocus APIs are supported.')

    