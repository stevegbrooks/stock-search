class StockAPICaller():
    credentials = ''
    dataRequest = dict()
    tickers = ''
    
    def __init__(self, credentials, dataRequest):
        self.credentials = credentials
        self.dataRequest = dataRequest
    
    def getStockData(self, tickers):
        self.tickers = tickers
    
