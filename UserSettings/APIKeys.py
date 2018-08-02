#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  9 19:49:46 2018

@author: sgb
"""

#holds the api keys/passwords


class APIKeys():
    
    def getGFKey(self):
        raise NotImplementedError("Please Implement this method")
    
    def getIntrinioKey(self):
        raise NotImplementedError("Please Implement this method")
    
    def getAlphaVantageKey(self):
        raise NotImplementedError("Please Implement this method")