# -*- coding: utf-8 -*-
"""
Created on Sat Oct  3 16:47:39 2020

@author: heziy
"""
#import csv
import pandas as pd
class dataInfo:
#      workdir=''
#      filepath=''
#      csv_file=csv.DictReader()
      def __init__(self,workdir,filepath,headers,individuals):
            self.workdir=workdir
            self.filepath=filepath
            self.headers=headers
            self.individuals=individuals
            self.originalNumOfLines=0
            #list of lists
            self.timeLists=[]
            self.heightLists=[]
            self.latLists=[]
            self.lngLists=[]