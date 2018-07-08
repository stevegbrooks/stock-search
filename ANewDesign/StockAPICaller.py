class StockAPICaller():
    credentials = ''
    tickers = ''
    
    def __init__(self, credentials, dataRequest):
        self.credentials = credentials
        self.__analyzeRequest(dataRequest)
    
    def __analyzeRequest(self, dataRequest):
        pass
    
    def getStockData(self, tickers):
        self.tickers = tickers
    
