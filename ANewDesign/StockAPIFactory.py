import GuruFocus
import Intrinio

class StockAPIFactory:
    
    apiArgs = dict()
    
    def __init__(self, apiArgs):
        
        if apiArgs.__contains__("gurufocus"):
            
            credentials = apiArgs.get("gurufocus")
            
            return GuruFocus(credentials)
        
        elif apiArgs.__contains__("intrinio"):
            
            credentials = apiArgs.get("intrinio")
            
            return Intrinio(credentials)
        
        else:
            
            raise Exception("Currently only Intrinio and GuruFocus APIs are supported.")

    