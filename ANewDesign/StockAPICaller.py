from abc import ABC, abstractmethod

class StockAPICaller(ABC):
    
    @abstractmethod
    def __init__(self, credentials):
        self.credentials = credentials
    
    @abstractmethod
    def specifyDataRequest(self, apiParameters):
        pass
    
    @abstractmethod
    def getStockData(self, tickers):
        pass
    
