# -*- coding: utf-8 -*-
"""
Created on Fri Jan 29 22:36:36 2021

@author: ZiyaoHe
"""
import matplotlib.pyplot as plt
#import numpy as np
import matplotlib.patches as mpatch
'''
 A Horizontal Distribution of the individual using matplotlib
'''
def plotHorizontal(main,iB,d):
    # find individual list
    IDList=d.individuals
    # timeLists=d.TimeLists
    #heightLists=d.heightLists
    latLists=d.latLists
    lngLists=d.lngLists
    
    # number of individuals
    num=len(IDList)
    
    maxLats=[]
    minLats=[]
    maxLngs=[]
    minLngs=[]
    IDremove=[]
    
    # for each individual
    # we find a pair of min max value for each individual's lat lng
    for i in range(0,num):
        idName=IDList[i]
        latList= latLists[i]
        lngList=lngLists[i]
        
        length=len(latList)
        outLatList=[]
        outLngList=[]
        for j in range(0,length):
            curLat=latList[j]
            curLng=lngList[j]
            #skip the data with missing values in lat and lng
            if(curLat!=''and curLng!=''):
                outLatList.append(float(curLat))
                outLngList.append(float(curLng))

        if(outLatList==[]):
            #delete this ID
            IDremove.append(idName)
        else:
            maxLat=max(outLatList)
            minLat=min(outLatList)
            maxLng=max(outLngList)
            minLng=min(outLngList)
            maxLats.append(maxLat)
            minLats.append(minLat)
            maxLngs.append(maxLng)
            minLngs.append(minLng)
    #remove the ID with empty value
    for i in IDremove:
        IDList.remove(i)
    num = len(IDList)
    #find the largest lat,lng and the smallest lat lng as range of axis
    theMinLat=min(minLats)
    
    theMaxLat=max(maxLats)
    
    
    theMinLng=min(minLngs)
    
    theMaxLng=max(maxLngs)
    xlim_min= theMinLng-(theMaxLng-theMinLng)*0.3
    if(xlim_min<-180):
        xlim_min=-180
        
    xlim_max= theMaxLng+(theMaxLng-theMinLng)*0.3
    if(xlim_max>180):
        xlim_max=180
        
    ylim_min= theMinLat-(theMaxLat-theMinLat)*0.3
    if(ylim_min<-90):
        ylim_min=-90
        
    ylim_max= theMaxLat+(theMaxLat-theMinLat)*0.3
    if(ylim_max>90):
        ylim_max=90
    main.axis(xmin=xlim_min,xmax=xlim_max, ymin=ylim_min, ymax=ylim_max)
    #main.ylim([theMinLat,theMaxLat])
    #generate a colormap that gives distinct color from 0 to num
    colormap=plt.cm.get_cmap('hsv', num)
    # define the rectangle
    for i in range(0,num):
        minLati=minLats[i]
        maxLati=maxLats[i]
        minLngi=minLngs[i]
        maxLngi=maxLngs[i]
        #add id name:
        idName=IDList[i]
        width=maxLngi-minLngi
        height=maxLati-minLati
        color = colormap(i)
        #colors.append(color)
        rect = mpatch.Rectangle((minLngi,minLati),width , height, linewidth=1,edgecolor=color, alpha = 0.3, facecolor=color,label=idName)
        main.add_patch(rect)
    main.legend(loc='best')
def plotDensity(main,iB,d):
    # find individual list
    IDList=d.individuals
    IDList_copy=IDList
    # timeLists=d.TimeLists
    #heightLists=d.heightLists
    latLists=d.latLists
    lngLists=d.lngLists
    #get outliers
    outliers=iB.outlierLists
    #print(outliers)
    # number of individuals
    num=len(IDList)
    
#    maxLats=[]
#    minLats=[]
#    maxLngs=[]
#    minLngs=[]
#    IDremove=[]
    # for each individual
    # we find a pair of min max value for each individual's lat lng
#    for i in range(0,num):
#        idName=IDList[i]
#        latList= latLists[i]
#        lngList=lngLists[i]
#        
#        length=len(latList)
#        outLatList=[]
#        outLngList=[]
#        for j in range(0,length):
#            curLat=latList[j]
#            curLng=lngList[j]
#            #skip the data with missing values in lat and lng
#            if(curLat!=''and curLng!=''):
#                outLatList.append(float(curLat))
#                outLngList.append(float(curLng))
#
#        if(outLatList==[]):
#            #delete this ID
#            IDremove.append(idName)
#        else:
#            maxLat=max(outLatList)
#            minLat=min(outLatList)
#            maxLng=max(outLngList)
#            minLng=min(outLngList)
#            maxLats.append(maxLat)
#            minLats.append(minLat)
#            maxLngs.append(maxLng)
#            minLngs.append(minLng)
#    #remove the ID with empty value
#    for i in IDremove:
#        IDList.remove(i)
#    num = len(IDList)

    if(outliers==[]):
        for i in range(0,num):
            #add id name:
            idName=IDList[i]
            #find a color to represent
            #color = colormap(i)
            ind=IDList_copy.index(idName)
            latList= latLists[ind]
            lngList=lngLists[ind]
            #save a list for each individual and plot them
            length=len(latList)
            outLatList=[]
            outLngList=[]
            for j in range(0,length):
                curLat=latList[j]
                curLng=lngList[j]
                #skip the data with missing values in lat and lng
                if(curLat!=''and curLng!=''):
                    outLatList.append(float(curLat))
                    outLngList.append(float(curLng))
            #plot the points
            main.scatter(outLngList,outLatList,
                   marker='s', label=idName, s=[5]*len(outLngList))
    else:
        o_latList=[]
        o_lngList=[]
        for i in range(0,num):
            #add id name:
            idName=IDList[i]
            #find a color to represent
            #color = colormap(i)
            ind=IDList_copy.index(idName)
            latList= latLists[ind]
            lngList=lngLists[ind]
            #save a list for each individual and plot them
            length=len(latList)
            outLatList=[]
            outLngList=[]
            for j in range(0,length):
                curLat=latList[j]
                curLng=lngList[j]
                #skip the data with missing values in lat and lng
                if(curLat!=''and curLng!=''):
                    outLatList.append(float(curLat))
                    outLngList.append(float(curLng))
            #plot the points
            main.scatter(outLngList,outLatList,
                   marker='s', label=idName, s=[5]*len(outLngList))
            #plot outliers
            outlierIndices=outliers[i]
            for o_id in outlierIndices:
                o_lat=latList[o_id]
                o_lng=lngList[o_id]
                print(o_lat)
                print(o_lng)
                o_latList.append(float(o_lat))
                o_lngList.append(float(o_lng))
            
        main.scatter(o_lngList,o_latList,marker='o',label='Outliers')
                
        
    main.legend(loc='best')
def plotDensity3D(main,iB,d):
    #get Height list
    heightLists=d.heightLists
    # find individual list
    IDList=d.individuals
#    IDList_copy=IDList
    # timeLists=d.TimeLists
    #heightLists=d.heightLists
    latLists=d.latLists
    lngLists=d.lngLists
    
    # number of individuals
    num=len(IDList)
    
    maxLats=[]
    minLats=[]
    maxLngs=[]
    minLngs=[]
    IDremove=[]
    # for each individual
    # we find a pair of min max value for each individual's lat lng
    for i in range(0,num):
        idName=IDList[i]
        latList= latLists[i]
        lngList=lngLists[i]
        heightList=heightLists[i]
        
        length=len(latList)
        outLatList=[]
        outLngList=[]
        outheightList=[]
        for j in range(0,length):
            curLat=latList[j]
            curLng=lngList[j]
            curheight=heightList[j]
            #skip the data with missing values in lat and lng
            if(curLat!=''and curLng!='' and curheight!=''):
                outLatList.append(float(curLat))
                outLngList.append(float(curLng))
                outheightList.append(float(curheight))

        if(outLatList==[]):
            #delete this ID
            IDremove.append(idName)
        else:
            #plot the points
            main.scatter(outLngList,outLatList,outheightList,
               marker='s', label=idName)
            maxLat=max(outLatList)
            minLat=min(outLatList)
            maxLng=max(outLngList)
            minLng=min(outLngList)
            maxLats.append(maxLat)
            minLats.append(minLat)
            maxLngs.append(maxLng)
            minLngs.append(minLng)
    #remove the ID with empty value
    for i in IDremove:
        IDList.remove(i)
    num = len(IDList)
#    #find the largest lat,lng and the smallest lat lng as range of axis
#    theMinLat=min(minLats)
#    theMaxLat=max(maxLats)
#    theMinLng=min(minLngs)
#    theMaxLng=max(maxLngs)
#    xlim_min= theMinLng-(theMaxLng-theMinLng)*0.3
#    if(xlim_min<-180):
#        xlim_min=-180
#        
#    xlim_max= theMaxLng+(theMaxLng-theMinLng)*0.3
#    if(xlim_max>180):
#        xlim_max=180
#        
#    ylim_min= theMinLat-(theMaxLat-theMinLat)*0.3
#    if(ylim_min<-90):
#        ylim_min=-90
#        
#    ylim_max= theMaxLat+(theMaxLat-theMinLat)*0.3
#    if(ylim_max>90):
#        ylim_max=90
#    # define the limitation of axis
#    main.axis(xmin=xlim_min,xmax=xlim_max, ymin=ylim_min, ymax=ylim_max)
   
    
        
    main.legend(loc='best')
'''
 Assumption: for each individual it starts from first timestamp and end at the last timestamp 
'''
def plotTimeline(fig,main,iB,d,reg):
    #import matplotlib.dates as md
    import pandas as pd
    # See https://github.com/facebook/prophet/issues/999
    #register_matplotlib_converters()
    #warnings.warn(msg, FutureWarning)
    #pd.plotting.register_matplotlib_converters()
    # find individual list
    IDList=d.individuals
    timeLists=d.timeLists
    latLists=d.latLists
    lngLists=d.lngLists
    # number of individuals
    num=len(IDList)
    
    minTimestamps=[]
    maxTimestamps=[]
    #IDremove=[]
    # for each individual
    # we find a pair of min max value for timestamp
    count=1
    for i in range(0,num):
        latList= latLists[i]
        lngList=lngLists[i]
        idName=IDList[i]
        timeList=timeLists[i]
        #skip the data with missing values in lat and lng
        length=len(latList)
        outTimeList=[]
        for j in range(0,length):
            curLat=latList[j]
            curLng=lngList[j]
            curTime=timeList[j]
            if(curLat!=''and curLng!=''):
               
                outTimeList.append(curTime)

        if(outTimeList!=[]):
            #plot this ID
            outTimeList=pd.to_datetime(outTimeList,format=reg)
        
            minTimestamps.append(outTimeList[0])
            maxTimestamps.append(outTimeList[-1])
            #get new index
            
            main.scatter(outTimeList, [count]*len(outTimeList),
               marker='s', label=idName)
            count=count+1
        
    maxTimestamp=max(maxTimestamps)
    minTimestamp=min(minTimestamps)
    diff = maxTimestamp-minTimestamp
    xlim_max=maxTimestamp+0.05*diff
    xlim_min=minTimestamp-0.05*diff
    main.axis(xmax=xlim_max)
    main.axis(xmin=xlim_min)
#    #main.get_xaxis().set_major_locator()
#    xfmt = md.DateFormatter('%Y-%m-%d %H:%M:%S')
#    main.xaxis.set_major_formatter(xfmt)
#    fig.autofmt_xdate()
#    if(7>float(diff.days)>1):
#        main.get_xaxis().set_major_locator(md.DayLocator(interval=1))
#    elif(30>float(diff.days)>=7):
#        main.get_xaxis().set_major_locator(md.WeekdayLocator(interval=1))
#    elif(float(diff.days)>=30):
#        main.get_xaxis().set_major_locator(md.MonthLocator(interval=1))
#    else:
#        main.get_xaxis().set_major_locator(md.HourLocator(interval=1))
    main.legend(loc='best')
