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


Goal 4
    Find the largest group of car makes for each gender.
    Possibly more than one such group per gender exists (equal sizes).

"""

import math
from decimal import *
import collections
# "regular" namedtuples
from collections import namedtuple
from typing import List, NamedTuple
import datetime
from datetime import date
import pandas as pd
import vehicle_details
import personal_details
import updated_status
import  employment
from vehicle_details import *
from datetime import datetime


from personal_details import *
from updated_status import *
from employment import *
import itertools


class DataIterator:
    def __init__(self, 
                 fname_1,
                 fname_2,
                 fname_3,
                 fname_4):
        self._fname_1 = fname_1
        self._fname_2 = fname_2
        self._fname_3 = fname_3
        self._fname_4 = fname_4
        self._input_date = datetime.date(2017, 3, 1)
        self._new_format = "%Y-%m-%d"
        self._return = True
        self._csv_file_list = [self._fname_1, self._fname_2, self._fname_3, self._fname_4 ]
        self._list_of_dataframes = []

        
        self._f = None
        
        self._f_1 = None
        self._f_2 = None
        self._f_3 = None
        self._f_4 = None
        
        self.data_1 = ""
        self.data_2 = ""
        self.data_3 = ""
        self.data_4 = ""
        self.final_data = ""
    
    def __iter__(self):
        return self
    
    def __getitem__(self):
          return self._return
    
    def __next__(self):
        row_1 = next(self._f_1)
        row_2 = next(self._f_2)
        row_3 = next(self._f_3)
        row_4 = next(self._f_4)
        
        val_1 = row_1.strip('\n').split(',')
        val_2 = row_2.strip('\n').split(',')
        val_3 = row_3.strip('\n').split(',')
        val_4 = row_4.strip('\n').split(',')
        
        self.data_3 = updated_status(val_3[0], 
                                     val_3[1],
                                     val_3[2])
       
       
        # print(val_3[1][0:10])
        
        self.data_1 = vehicle_details(val_1[0],
                                      val_1[1],
                                      val_1[2],
                                      val_1[3])     
        
        self.data_2 = personal_details(val_2[0],
                                       val_2[1],
                                       val_2[2],
                                       val_2[3],
                                       val_2[4])
        
         
        self.data_4 = employment_details(val_4[0],
                                         val_4[1],
                                         val_4[2],
                                         val_4[3])
       
        self.data = zip(self.data_1, self.data_2, self.data_3, self.data_4)
        
        if (datetime.datetime.strptime(val_3[1][0:10],"%Y-%m-%d").date() < self._input_date):
            self._return = False           
        else:
            self._return = True
            # return self.data
            
        return self._return, self.data
    
   
    def __enter__(self):
        self._f_1 = open(self._fname_1)
        self._f_2 = open(self._fname_2)
        self._f_3 = open(self._fname_3)
        self._f_4 = open(self._fname_4)
        next(self._f_1)
        next(self._f_2)
        next(self._f_3)
        next(self._f_4)
        
        # next(self._f)
        return self
    
    def __exit__(self, exc_type, exc_value, exc_tb):
        if not self._f_1.closed:
            self._f_1.close()
            
        if not self._f_2.closed:
            self._f_2.close()

        if not self._f_3.closed:
            self._f_3.close()

        if not self._f_4.closed:
            self._f_4.close()
            
        return False
    
    def largest_grp_car_gender(self):
        df_1 = pd.read_csv(self._fname_1)
        df_2 = pd.read_csv(self._fname_2)
        df_3 = pd.read_csv(self._fname_3)
        df_4 = pd.read_csv(self._fname_4)
        self.final_data = pd.merge(df_1, df_2, on='ssn')
        self.final_data = pd.merge(self.final_data, df_3, on='ssn')
        self.final_data = pd.merge(self.final_data, df_4, on='ssn')
        return self.final_data.groupby(['gender','vehicle_make']).size().reset_index(name='counts').sort_values(['counts'], ascending=False)
        
        # for filename in self._csv_file_list:
        #     self._list_of_dataframes.append(pd.read_csv(filename))
        # self._merged_df = pd.concat(self._list_of_dataframes)
        # return self._list_of_dataframes


# with DataIterator('vehicles.csv', 'personal_info.csv', 'update_status.csv','employment.csv' ) as data_combined:    
#     for _, row in itertools.dropwhile(lambda x : x[0] == False , data_combined):
#     # for _, row in data_combined:
#         print(list(row))
        
data_combined = DataIterator('vehicles.csv', 'personal_info.csv', 'update_status.csv','employment.csv' )
largest_grp_car_gender = data_combined.largest_grp_car_gender()
print(largest_grp_car_gender.head)
