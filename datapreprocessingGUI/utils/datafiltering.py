# -*- coding: utf-8 -*-
"""
Created on Sat Oct  3 20:56:23 2020

@author: heziy
"""
import pandas as pd
import os
def filtering(headers,d):
      df=pd.read_csv(d.filepath)
      #find the columns we want to drop
      import numpy as np
      droplist = np.setdiff1d(d.headers,headers)
      workdir=d.workdir
      resultCSV=workdir+'/filtered.csv'
      for col in droplist:
            #print(col)
            df.drop(columns=[col], axis = 1, inplace = True)
      
      
      if(not os.path.exists(resultCSV)):
          # detele repetition
          df=df.drop_duplicates(keep='first')
          df.to_csv(resultCSV,index=False,header=True,mode='w')
      else:
                
          df=df.drop_duplicates(keep='first')
          df.to_csv(resultCSV,index=False,header=False,mode='a')
      #dataFrame.to_csv(path, index = False, header=True)
      print(resultCSV)
            
            