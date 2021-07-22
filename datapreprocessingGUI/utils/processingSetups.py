# -*- coding: utf-8 -*-
"""
Created on Tue Oct  6 20:08:54 2020

@author: heziy
"""

class processingSetups:
      def __init__(self):
            self.choosenHeaders=[]
            self.idHeaderName=''
            self.latHeaderName=''
            self.lngHeaderName=''
            self.heightHeaderName=''
            self.timestampHeaderName=''
            self.useDefault=False
      def useDefaultInfo(self):
            self.choosenHeaders=list(set(self.choosenHeaders+['individual-local-identifier','location-lat','location-long','height-above-ellipsoid','timestamp']))
            self.idHeaderName= 'individual-local-identifier'
            self.latHeaderName='location-lat'
            self.lngHeaderName='location-long'
            self.heightHeaderName='height-above-ellipsoid'
            self.timestampHeaderName='timestamp'
            self.useDefault=True
      def cleanDefaultInfo(self):
            for ele in ['individual-local-identifier','location-lat','location-long','height-above-ellipsoid','timestamp']:
                self.choosenHeaders.remove(ele)
            self.idHeaderName=self.idHeaderName
            self.latHeaderName=self.latHeaderName
            self.lngHeaderName=self.lngHeaderName
            self.heightHeaderName=self.heightHeaderName
            self.timestampHeaderName=self.timestampHeaderName
            self.useDefault=False
      def cleanLasttInfo(self):
            self.choosenHeaders=[]
            self.idHeaderName=''
            self.latHeaderName=''
            self.lngHeaderName=''
            self.heightHeaderName=''
            self.timestampHeaderName=''
            self.useDefault=False
      def setBasicInfo(self,idHeaderName,latHeaderName,lngHeaderName,heightHeaderName,timestampHeaderName):
            self.idHeaderName= idHeaderName
            self.latHeaderName=latHeaderName
            self.lngHeaderName=lngHeaderName
            self.heightHeaderName=heightHeaderName
            self.timestampHeaderName=timestampHeaderName
      def storeLastInfo(self):
          import os,csv
          loc=os.getcwd()
          outpath=str(loc+'/'+'utils/'+'tmp/')
          if not os.path.exists(outpath):
             os.makedirs(outpath)
          filePath=outpath+'config.csv'
          csv_file=open(filePath,  'w', newline='')
          row = ['choosenHeaders','idHeaderName','latHeaderName','lngHeaderName','heightHeaderName','timestampHeaderName','useDefault']
          writer = csv.DictWriter(csv_file
                              ,fieldnames=row
                              )
          writer.writeheader()
          row2=[self.choosenHeaders,self.idHeaderName,self.latHeaderName,self.lngHeaderName,self.heightHeaderName,self.timestampHeaderName,self.useDefault]
          dictRow=dict(zip(row , row2))
          writer.writerow(dictRow)
      
          
      def updateLastInfo(self):
          import os
          import pandas as pd
          loc=os.getcwd()
          outpath=str(loc+'/'+'utils/'+'tmp/')
          if not os.path.exists(outpath):
             os.makedirs(outpath)
          filePath=outpath+'config.csv'
          if (os.path.isfile(filePath)):#there is already a config file
                #
                df = pd.read_csv(filePath)
                idHeaderName=df['idHeaderName'][0]
                latHeaderName=df['latHeaderName'][0]
                lngHeaderName=df['lngHeaderName'][0]
                heightHeaderName=df['heightHeaderName'][0]
                timestampHeaderName=df['timestampHeaderName'][0]
                self.choosenHeaders=df['choosenHeaders'][0]
                #however we have to convert the string presentation of list to real list
                import ast
                self.choosenHeaders=ast.literal_eval(self.choosenHeaders)
                print(type(self.choosenHeaders))
                self.setBasicInfo(idHeaderName,latHeaderName,lngHeaderName,heightHeaderName,timestampHeaderName)
                self.useDefault=df['useDefault'][0]
          else:
              print('There is no config file.')
              
      
