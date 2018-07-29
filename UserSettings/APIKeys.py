#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  9 19:49:46 2018

@author: sgb
"""

#holds the api keys/passwords

class APIKeys():
    
    gfKey = ''
    intrinioUN = ''
    intrinioPW = ''
    intrinioKey = []
    
    def __init__(self):
        self.gfKey = ''
        self.intrinioUN = ''
        self.intrinioPW = ''
        self.intrinioKey = [self.intrinioUN, self.intrinioPW]
    
    def getGFKey(self):
        return self.gfKey
    
    def getIntrinioKey(self):
        return self.intrinioKey