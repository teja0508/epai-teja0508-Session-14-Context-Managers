# EPAI3-PythonContextManager
## Goal 1

### Business Problem

Your first task is to create iterators for each of the four files that contained cleaned up data, of the correct type (e.g. string, int, date, etc), and represented by a named tuple. For now these four iterators are just separate, independent iterators.

### Solution

Have defined three iterators in __next function and the class DataIterator has become iterator due to this. Have defined three class vehicle_details, updated_status etc and these classes are inherited from namedtuple class.

```
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
```

Have then called the class within a for loop so that can process the iterator.

```
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
```



## Goal 2

### Business Problem

Create a single iterable that combines all the columns from all the iterators. The iterable should yield named tuples containing all the columns. Make sure that the SSN's across the files match!
All the files are guaranteed to be in SSN sort order, and every SSN is unique, and every SSN appears in every file. Make sure the SSN is not repeated 4 times - one time per row is enough!

### Solution

I have three file pointer added into a zip command to send a combined one in __next__ function which returns when the iterator is called.

```
    def __next__(self):
        row_1 = next(self._f_1)
        row_2 = next(self._f_2)
        row_3 = next(self._f_3)
        row_4 = next(self._f_4)
        
        val_1 = row_1.strip('\n').split(',')
        val_2 = row_2.strip('\n').split(',')
        val_3 = row_3.strip('\n').split(',')
        val_4 = row_4.strip('\n').split(',')
        
        self.data_1 = vehicle_details(val_1[0],
                                      val_1[1],
                                      val_1[2],
                                      val_1[3])     
        
        self.data_2 = personal_details(val_2[0],
                                       val_2[1],
                                       val_2[2],
                                       val_2[3],
                                       val_2[4])
        
        self.data_3 = updated_status(val_3[0],
                                     val_3[1],
                                     val_3[2])
            
        self.data_4 = employment_details(val_4[0],
                                         val_4[1],
                                         val_4[2],
                                         val_4[3])
       
        self.data = zip(self.data_1, self.data_2, self.data_3, self.data_4)
        return self.data
```



## Goal 3

### Business Problem

Next, you want to identify any stale records, where stale simply means the record has not been updated since 3/1/2017 (e.g. last update date < 3/1/2017). Create an iterator that only contains current records (i.e. not stale) based on the last_updated field from the status_update file.

### Solution

I have stored input date into class attribute as shared below.

```
self._input_date = datetime.date(2017, 3, 1)
```

Have added following condition to set the flag based on input date.

```
if (datetime.datetime.strptime(val_3[1][0:10],"%Y-%m-%d").date() < self._input_date):
            self._return = False           
        else:
            self._return = True
            # return self.data
```

I have used itertools.dropwhile function to drop the data where to eliminate data which are less than input date.

```
with DataIterator('vehicles.csv', 'personal_info.csv', 'update_status.csv','employment.csv' ) as data_combined:    
    for _, row in itertools.dropwhile(lambda x : x[0] == False , data_combined):
    # for _, row in data_combined:
        print(list(row))
        
```

## Goal 4

### Business Problem

Find the largest group of car makes for each gender.Possibly more than one such group per gender exists (equal sizes).

### Solution

Have developed the following function to do the group by based on gender and car made.

```
    def largest_grp_car_gender(self):
        df_1 = pd.read_csv(self._fname_1)
        df_2 = pd.read_csv(self._fname_2)
        df_3 = pd.read_csv(self._fname_3)
        df_4 = pd.read_csv(self._fname_4)
        self.final_data = pd.merge(df_1, df_2, on='ssn')
        self.final_data = pd.merge(self.final_data, df_3, on='ssn')
        self.final_data = pd.merge(self.final_data, df_4, on='ssn')
        return self.final_data.groupby(['gender','vehicle_make']).size().reset_index(name='counts').sort_values(['counts'], ascending=False)
```

