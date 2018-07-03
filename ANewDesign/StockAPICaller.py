class StockAPICaller():
    
    credentials = ''
    apiParameters = ''
    tickers = ''
    
    def __init__(self, credentials):
        self.credentials = credentials
    
    def specifyDataRequest(self, apiParameters):
        self.apiParameters = apiParameters
    
    def getStockData(self, tickers):
        self.tickers = tickers
    
