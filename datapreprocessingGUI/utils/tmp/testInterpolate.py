# -*- coding: utf-8 -*-
"""
Created on Mon Jan 11 16:45:59 2021

@author: ZiyaoHe
"""

import pandas as pd 
  
# Creating the dataframe  
df = pd.DataFrame({"A":[12, 4, 5, None, 1], 
                   "B":[None, 2, 54, 3, None], 
                   "C":[20, 16, None, 3, 8], 
                   "D":[14, 3, None, None, 6]}) 
print(df)
# to interpolate the missing values 
df=df.interpolate(method ='linear', limit_direction ='forward', limit = 1) 
print(df)
df=df.interpolate(method ='linear', limit_direction ='forward', limit = 1) 
print(df)