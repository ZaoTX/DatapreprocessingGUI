# -*- coding: utf-8 -*-
"""
Created on Sat Oct  3 20:52:58 2020

Clean data: Mainly deal with missing value problem
@author: heziy
"""
import os
import pandas as pd
#interpolation of missing value in location information, better performance in high resolution dataset
# pandas interpolate() https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.interpolate.html
def interpolation(d,p,meth):
      base_dir = d.workdir
      #specify the critical headers
#      latHeader=p.latHeaderName
#      lngHeader=p.lngHeaderName
#      heightHeader=p.heightHeaderName
      filePath = d.filepath
      outpath = base_dir+'/'+'clean'
      if not os.path.exists(outpath):
               os.makedirs(outpath)
      #csv_file=open(filePath, encoding='utf-8')
      df = pd.read_csv(filePath)#get dataframe
      idHeader=p.idHeaderName
      IDs = d.individuals
      
      if IDs==[]:
          print("please start preanalysis first, if you already did, the source file could be empty")
      else:
          dfList = []
          for ID in IDs:
              dfi=df[df[idHeader]==ID]
              dfi=dfi.interpolate(method =meth, limit_direction ='forward',limit_area='inside')
              dfi=dfi.dropna()
              dfList.append(dfi)
          result_df = pd.concat(dfList)   
          result_df.to_csv(outpath+'/'+meth+'_interporlation.csv',index=False)

# pandas dropna(): https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.dropna.html
def removeMissing(d,p):
      base_dir = d.workdir
      #specify the critical headers
#      latHeader=p.latHeaderName
#      lngHeader=p.lngHeaderName
#      heightHeader=p.heightHeaderName
      filePath = d.filepath
      outpath = base_dir+'/'+'clean'
      if not os.path.exists(outpath):
               os.makedirs(outpath)
      #csv_file=open(filePath, encoding='utf-8')
      df = pd.read_csv(filePath)#get dataframe
      df=df.dropna()
      df.to_csv(outpath+'/'+'removeMissing.csv',index=False)
# compute DBSCAN algorithm for each individual to detect the outlier      
# return a list of the outlier index        
def Clustering(d,p,eps):
    import numpy as np
    from sklearn.cluster import DBSCAN
    sizeOfoutput=0
    #csv with headers then totalLines=2 without headers totalLines=1
    totalLines=2
    outputLines=np.empty(0)
    outputList=[]
    for i in range(0,len(d.timeLists)):
        latList=d.latLists[i]
        lngList=d.lngLists[i]
        heightList=d.heightLists[i]
        # stack the lists
        position_X=np.column_stack((latList, lngList,heightList))
        position_X = position_X.astype(np.float64)
        clustering = DBSCAN(eps=eps, min_samples=2).fit(position_X)
        labels = clustering.labels_
        
        #index of -1(outliers)
        outlierIndex= np.where(labels==-1)[0]
        outlierIndexList=outlierIndex.tolist()
        outputList.append(outlierIndexList)
        
        sizeOfoutput=sizeOfoutput+len(outlierIndex)
        outlierIndex = outlierIndex+totalLines
        outputLines = np.concatenate((outputLines,outlierIndex))
        totalLines=len(labels)
    return outputLines,outputList
# ST DBSCAN( need an extra normalization for timestamp)
# input: d,p, eps1: eps for location, eps2: eps for timestamp,  reg: regular language for time
def STDBSCAN_Clustering(d,p,eps1,eps2,reg):
    import numpy as np
    from st_dbscan import ST_DBSCAN
    from datetime import datetime
    
    sizeOfoutput=0
    #csv with headers then totalLines=2 without headers totalLines=1
    totalLines=2
    outputLines=np.empty(0)
    outputList=[]
    # iterate through Lists
    for i in range(0,len(d.timeLists)):
        latList=d.latLists[i]
        lngList=d.lngLists[i]
        heightList=d.heightLists[i]
        timeList = d.timeLists[i]
        timeListInDatetime=pd.to_datetime(timeList, format=reg)
        # get first timestamp
        t0=timeListInDatetime[0]
        #timestamp normalization
        nor_timeList=[x-t0 for x in timeListInDatetime]
        nor_timeList=[x.total_seconds() for x in nor_timeList]
        #print(nor_timeList)
        # stack the lists
        position_X=np.column_stack((nor_timeList,latList, lngList,heightList))
        position_X = position_X.astype(np.float64)
        clustering = ST_DBSCAN(eps1=eps1,eps2=eps2, min_samples=2).fit(position_X)
        labels = clustering.labels
        
        #index of -1(outliers)
        outlierIndex= np.where(labels==-1)[0]
        outlierIndexList=outlierIndex.tolist()
        outputList.append(outlierIndexList)
        
        sizeOfoutput=sizeOfoutput+len(outlierIndex)
        outlierIndex = outlierIndex+totalLines
        outputLines = np.concatenate((outputLines,outlierIndex))
        totalLines=len(labels)
    return outputLines,outputList