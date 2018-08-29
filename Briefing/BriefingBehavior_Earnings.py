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

class BriefingBehavior_Earnings(BriefingBehavior):
    
    def __init__(self):
        super().__init__()
    
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
            
            if len(table) <= 4:
                priorYear_S = float('nan')
            else:
                priorYear_S = float(table.iloc[4,16])
                
            table = pd.DataFrame(data = {'ticker' : self.ticker,
                                         'Date' : table.iloc[0,0],
                                         'Year2YearRev' : float(re.sub('\\s|%', '', table.iloc[0,20]))/100,
                                         'Estimate_E' : table.iloc[0,12],
                                         'Actual_E' : table.iloc[0,10],
                                         'Estimate_S' : table.iloc[0,18],
                                         'Actual_S' : table.iloc[0,16],
                                         'PriorYear_E' : table.iloc[0,14],
                                         'PriorYear_S' : priorYear_S}, index = [0])
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
        
        