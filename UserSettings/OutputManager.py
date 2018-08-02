#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OutputManager takes the raw data from the Controller and cleans it up
according to the user specs. Enter those specs here.

The 'identifyColNames()' function is necessary because the APICallers will sometimes return metadata
about the API call in the column name itself (if it is historical data and includes adjusted dates), so the identify function typically uses regex to pull these column names out so they can be refered to by the 
other functions.

@author: sgb
"""

class OutputManager():
    
    def calcNewColumns(self):
        raise NotImplementedError("Please Implement this method")
    
    def deleteExtraCols(self):
        raise NotImplementedError("Please Implement this method")
    
    def reindexColumns(self):
        raise NotImplementedError("Please Implement this method")
    
    def renameColumns(self):
        raise NotImplementedError("Please Implement this method")
    
    def identifyColNames(self):
        raise NotImplementedError("Please Implement this method")
