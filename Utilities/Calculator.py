
class Calculator:
    
    def PEAD(self, avgVolume, outstandingShares):
        if outstandingShares == 0 or avgVolume == 0:
            return 0
        else:
            return round(1/(avgVolume/outstandingShares * 100), 3)
        
    def mktCap(self, lastPrice, outstandingShares):
        return round((lastPrice * outstandingShares)/1000000, 2)
    
    def dollarVol(self, lastPrice, lastVolume):
        return round((lastPrice * lastVolume)/1000000, 2)
    
    def volRatio(self, lastVolume, avgVolume):
        if avgVolume == 0:
            return 0
        else:
            return float(round(lastVolume/avgVolume, 1))
    
    def volOverMC(self, lastVolume, lastPrice, outstandingShares):
        marketCap = lastPrice * outstandingShares
        if marketCap == 0:
            return 0
        else:
            return round(lastVolume * lastPrice / marketCap * 100, 2)
    
    def moveStrength(self, lastPrice, lastVolume, outstandingShares, avgVolume):
        
        if outstandingShares != 0 and lastPrice != 0:
            numerator = (lastPrice * lastVolume) / (lastPrice * outstandingShares)
        else:
            numerator = 0
        
        if outstandingShares != 0 and avgVolume != 0:
            denominator = avgVolume/outstandingShares
        else:
            denominator = 0
        
        if denominator != 0:
            return round(numerator/denominator, 2)
        else:
            return 0
    
    def getPercentChange(self, closePrice1, closePrice2):
        diff = closePrice1 - closePrice2
        if closePrice2 != 0:
            change = diff/closePrice2
        else:
            change = 0
        return round(change, 4)
