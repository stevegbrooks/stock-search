#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 27 21:22:30 2018

@author: sgb
"""
import re
import pandas as pd
from bs4 import BeautifulSoup
from Briefing.BriefingBehavior import BriefingBehavior
from Utilities.DateAdjuster import DateAdjuster

class BriefingBehavior_Earnings(BriefingBehavior):
    
    def __init__(self):
        super().__init__()
        self.da = DateAdjuster()
    
    def getStockData(self, baseURL, endpoint, ticker, credentials, item = ''):
        rawHTML = super().getStockData(baseURL, endpoint, ticker, credentials, item)
        self.ticker = ticker
        output = self.parseHTML(rawHTML)
        return output
    
    def parseHTML(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        divs = soup.find_all('div', class_ = 'NoInplayDataContent')
        
        hasTable = divs[0].find_all('div', class_ = "noInplayDataDiv DoNotHighlightAnything")
        
        if len(hasTable) is 0:
            table = pd.read_html(str(divs[0].table))[0]
            
            if len(table) <= 5:
                priorYear_s = float('nan')
            else:
                priorYear_s = float(table.iloc[5,16])
            
            if len(table) < 2 or table.iloc[1,20] != table.iloc[1,20]:
                y2YRev = float('nan')
            else:
                y2YRev = float(re.sub('\\s|%', '', table.iloc[1,20]))/100
                
            if len(table) < 2 or table.iloc[1,0] != table.iloc[1,0]:
                date = ''
            else:
                date = self.da.convertToDate(table.iloc[1,0], 
                                             dateStringFormat = '%d-%b-%y')
            
            if len(table) > 1:
                estimate_e = table.iloc[1,12]
                actual_e = table.iloc[1,10]
                estimate_s = table.iloc[1,18]
                actual_s = table.iloc[1,16]
                priorYear_e = table.iloc[1,14]
            else:
                estimate_e = actual_e = estimate_s = actual_s = priorYear_e = float('nan')
                
            table = pd.DataFrame(data = {'ticker' : self.ticker,
                                         'Date' : date,
                                         'Year2YearRev' : y2YRev,
                                         'Estimate_E' : estimate_e,
                                         'Actual_E' : actual_e,
                                         'Estimate_S' : estimate_s,
                                         'Actual_S' : actual_s,
                                         'PriorYear_E' : priorYear_e,
                                         'PriorYear_S' : priorYear_s}, index = [0])
        else:
            table = pd.DataFrame(data = {'ticker' : self.ticker,
                                         'Date' : '',
                                         'Year2YearRev' : float('nan'),
                                         'Estimate_E' : float('nan'),
                                         'Actual_E' : float('nan'),
                                         'Estimate_S' : float('nan'),
                                         'Actual_S' : float('nan'),
                                         'PriorYear_E' : float('nan'),
                                         'PriorYear_S' : float('nan')}, index = [0])

        return table
        
        