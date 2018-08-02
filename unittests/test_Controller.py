#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  1 08:33:43 2018

@author: sgb
"""
import pytest
from Controller import Controller
from UserSettings.AppSettings_Test import AppSettings_Test

class TestController:
    
    @pytest.fixture(scope = "function")
    def intrinio_dataPoint1(cls):
        c = Controller(isHistoricalMode = False,
                       appSettings = ,
                       tickerInput = "AAPL")
        api1 = 'intrinio'
        api2 = 'gurufocus'
        dataRequest1 = {'endpoint' = 'data_point',
                        'item' = }
    
    def test__validateDataRequest1():
        
        
