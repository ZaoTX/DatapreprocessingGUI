# -*- coding: utf-8 -*-
"""
Created on Sun Dec 13 19:41:46 2020

@author: heziy
"""

class infoBuffer:
      def __init__(self):
          #infor for data report(pre analysis)
            self.missingvalue=0
            self.startTime=''
            self.endTime=''
            self.startPos=''
            self.endPos=''
            self.numOfDatapoints=0
            self.missingLat=0
            self.missingLng=0
            self.missingHeight=0
            self.maxLat=0
            self.minLat=0
            self.maxLng=0
            self.minLng=0
            self.maxHeight=0
            self.minHeight=0
            #possible outliers
            self.outlierLists=[]
            # metrics and information of trajectory sampling
            self.fileLoc=''
            self.compressionratio=0
            self.runtime=0
            self.averageSED=0
            self.frechetDistance=0
            self.ILD=0#information loss degree
            # these are only used to store information after the sampling
            self.individuals=[]
            self.timeLists=[]
            self.heightLists=[]
            self.latLists=[]
            self.lngLists=[]
            # preprocessing settings
            self.idHeaderName=''
            self.latHeaderName=''
            self.lngHeaderName=''
            self.heightHeaderName=''
            self.timestampHeaderName=''
            self.timestampReg=''
      def setMissing(self,num):
            self.missingvalue=num
      def setStartTime(self,startTime):
            self.startTime=startTime
      def setEndTime(self,endTime):
            self.endTime=endTime
      def setStartPos(self,pos):
            self.startPos=pos
      def setEndPos(self,pos):
            self.endPos=pos
      def setDataPoints(self,num):
            self.numOfDatapoints=num
      def cleanBuffer(self):
            self.missingvalue=0
            self.startTime=''
            self.endTime=''
            self.startPos=''
            self.endPos=''
            self.numOfDatapoints=0