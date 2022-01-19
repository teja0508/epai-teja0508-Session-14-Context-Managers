# -*- coding: utf-8 -*-
"""
Created on Mon Aug  9 23:58:12 2021

@author: AKayal
"""
from collections import namedtuple
from typing import List, NamedTuple
import datetime
from datetime import date

class personal_details(NamedTuple):
    """
    Using the typing module, we can be even more explicit about our data structures.
    
    https://realpython.com/python-namedtuple/

    """
    ssn: str
    first_name: str
    last_name: str
    gender: str
    language: str
