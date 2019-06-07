#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  2 10:26:45 2018

@author: sgb
"""

from UserSettings.APIKeys import APIKeys

class APIKeys_Test(APIKeys):
    
    def __init__(self):
        
        self.alphaVantageKey = '0RWW633ATTF3QFOL'
        
        self.gfKey = 'b0373bf00e2473ed61fa029e6777ddc4:98e3238704945ab068f05c902f5c4e09'
        
        self.intrinioUN = '14434456068d3aa67d6d01703c377c5b'
        self.intrinioPW = 'd51918023463341a24d85d8e263f3403'
        self.intrinioKey = [self.intrinioUN, self.intrinioPW]
        
        self.briefingUN = 'garethb787@gmail.com'
        self.briefingPW = 'Massivecat22'
        self.briefingKey = [self.briefingUN, self.briefingPW]
    
    def getGFKey(self):
        return self.gfKey
    
    def getIntrinioKey(self):
        return self.intrinioKey
    
    def getAlphaVantageKey(self):
        return self.alphaVantageKey
    
    def getBriefingKey(self):
        return self.briefingKey