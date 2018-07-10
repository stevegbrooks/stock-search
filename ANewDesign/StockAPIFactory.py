from ANewDesign.GuruFocus import GuruFocus
from ANewDesign.Intrinio import Intrinio

class StockAPIFactory:
    
    apiArgs = dict()
    
    def getAPI(self, apiArgs, dataRequest):
        
        if apiArgs.__contains__('gurufocus'):
            credentials = apiArgs.get('gurufocus')
            return GuruFocus(credentials, dataRequest)
        
        elif apiArgs.__contains__('intrinio'):
            credentials = apiArgs.get('intrinio')
            return Intrinio(credentials, dataRequest)
        
        else:
            raise Exception('Currently only Intrinio and GuruFocus APIs are supported.')

    