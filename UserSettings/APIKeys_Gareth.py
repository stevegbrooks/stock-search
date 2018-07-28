#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  9 19:49:46 2018

@author: sgb
"""

#holds the api keys/passwords

class APIKeys_Gareth():
    
    gfKey = ''
    intrinioUN = ''
    intrinioPW = ''
    intrinioKey = []
    
    def __init__(self):
        self.gfKey = 'b0373bf00e2473ed61fa029e6777ddc4:98e3238704945ab068f05c902f5c4e09'
        self.intrinioUN = '14434456068d3aa67d6d01703c377c5b'
        self.intrinioPW = 'd51918023463341a24d85d8e263f3403'
        self.intrinioKey = [self.intrinioUN, self.intrinioPW]
    
    def getGFKey(self):
        return self.gfKey
    
    def getIntrinioKey(self):
        return self.intrinioKey