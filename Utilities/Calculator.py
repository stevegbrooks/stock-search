
class Calculator:
    
    def __init__(self):
        pass
    
    def PEAD(avgVolume, outstandingShares):
        if outstandingShares == 0 or avgVolume == 0:
            return 0
        else:
            return round(1/(avgVolume/outstandingShares * 100), 3)
        
    def mktCap(lastPrice, outstandingShares):
        return round((lastPrice * outstandingShares)/1000000, 2)
    
    def dollarVol(lastPrice, lastVolume):
        return round((lastPrice * lastVolume)/1000000, 2)
    
    def volRatio(lastVolume, avgVolume):
        if avgVolume == 0:
            return 0
        else:
            return float(round(lastVolume/avgVolume, 1))
    
    def volOverMC(lastVolume, lastPrice, outstandingShares):
        marketCap = lastPrice * outstandingShares
        if marketCap == 0:
            return 0
        else:
            return round(lastVolume * lastPrice / marketCap * 100, 2)
    
    def moveStrength(lastPrice, lastVolume, outstandingShares, avgVolume):
        
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
    
    def getPercentChange(closePrice1, closePrice2):
        diff = closePrice1 - closePrice2
        change = diff/closePrice2 * 100
        return round(change, 2)
