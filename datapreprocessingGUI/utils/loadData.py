# -*- coding: utf-8 -*-
"""
Created on Sat Oct  3 14:44:55 2020

@author: heziy
"""
#Corresponding to the function of Tab1
#load data 
#import pandas as pd
import csv
import tkinter as tk


def setupWorkdir(dirPath,d):
      d.workdir=dirPath
      print(d.workdir)
def setupData(filePath,d):
      if(filePath.endswith('.csv')):
            #from utils.DataTransferStation import d
            csv_file=open(filePath,encoding='utf-8')
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            d.csv_reader=csv_reader
            d.filepath=filePath
            d.headers = list(d.csv_reader.fieldnames)
            #csv_file.close()
                  
      else:
            tk.messagebox.showinfo("Error in loadData","Please give a csv file.")
      
            
