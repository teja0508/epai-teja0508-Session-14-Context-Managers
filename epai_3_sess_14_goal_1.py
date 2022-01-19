# -*- coding: utf-8 -*-
"""
Created on Mon Aug  9 23:46:19 2021

@author: AKayal

Project
For this project you have 4 files containing information about persons.

The files are:

    personal_info.csv - personal information such as name, gender, etc. (one row per person)
    vehicles.csv - what vehicle people own (one row per person)
    employment.csv - where a person is employed (one row per person)
    update_status.csv - when the person's data was created and last updated
    Each file contains a key, SSN, which uniquely identifies a person.

    This key is present in all four files.

    You are guaranteed that the same SSN value is present in every file, and that it only appears once per file.

    In addition, the files are all sorted by SSN, i.e. the SSN values appear in the same order in each file.

Goal 1

    Your first task is to create iterators for each of the four files that contained cleaned up data, of the correct type (e.g. string, int, date, etc), and represented by a named tuple.
    For now these four iterators are just separate, independent iterators.

"""

import math
from decimal import *
import collections
# "regular" namedtuples
from collections import namedtuple
from typing import List, NamedTuple
from datetime import date
import pandas as pd
import vehicle_details
import personal_details
import updated_status
import  employment
from vehicle_details import *

from personal_details import *
from updated_status import *
from employment import *


class DataIterator:
    def __init__(self, fname):
        self._fname = fname
        self._f = None
        self.data = ""
    
    def __iter__(self):
        return self
    
    def __next__(self):
        row = next(self._f)
        val = row.strip('\n').split(',')
        # print(val[0])
        if (self._fname == 'vehicles.csv'):
            self.data = vehicle_details(val[0],
                                        val[1],
                                        val[2],
                                        val[3])
            return self.data
            
        elif (self._fname == 'personal_info.csv'):
            self.data = personal_details(val[0],
                                         val[1],
                                         val[2],
                                         val[3],
                                         val[4])
            return self.data
            
        elif (self._fname == 'update_status.csv'):
            self.data = updated_status(val[0],
                                        val[1],
                                        val[2])
            return self.data
        
        elif (self._fname == 'employment.csv'):
            self.data = employment_details(val[0],
                                           val[1],
                                           val[2],
                                           val[3])    
            return self.data
        
        else:
            return val
        
    
    def __enter__(self):
        self._f = open(self._fname)
        # next(self._f)
        return self
    
    def __exit__(self, exc_type, exc_value, exc_tb):
        if not self._f.closed:
            self._f.close()
        return False
    

with DataIterator('vehicles.csv') as data_vehicle:
    for row in data_vehicle:
        print(row)
        

with DataIterator('personal_info.csv') as personal_info:
    for row in personal_info:
        print(row)


with DataIterator('update_status.csv') as update_status:
    for row in update_status:
        print(row)
        

with DataIterator('employment.csv') as employment:
    for row in employment:
        print(row)
        
