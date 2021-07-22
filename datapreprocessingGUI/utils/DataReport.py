# -*- coding: utf-8 -*-
"""
Created on Mon Dec  7 20:40:34 2020

@author: ZiyaoHe
"""

#split for each individual to get different IDs
#return different ids and it's coordinates
def getIndividualNum(d,p):
    import csv
    #outputs: lists of list for each individual
    timeLists=[]
    heightLists=[]
    latLists=[]
    lngLists=[]
    IDList=[]
    filePath = d.filepath
    #base_dir+'/'+'filtered.csv'
    csv_file=open(filePath, encoding='utf-8')
    csv_reader = csv.DictReader(csv_file, delimiter=',')
    #create initial list for each individual
    cur_id=''
    last_id=''
    curTimeList=[]
    curLatList=[]
    curLngList=[]
    curHeightList=[]
    # find header names
    idHeader=p.idHeaderName
    lngHeader = p.lngHeaderName
    latHeader = p.latHeaderName
    heightHeader = p.heightHeaderName
    timeHeader = p.timestampHeaderName
    for row in csv_reader:
        cur_id=row[idHeader]
        if (last_id!=cur_id and last_id!='' and (last_id not in IDList)):
            #collect information
            IDList.append(last_id)
            timeLists.append(curTimeList)
            heightLists.append(curHeightList)
            latLists.append(curLatList)
            lngLists.append(curLngList)
            curTimeList=[]
            curLatList=[]
            curLngList=[]
            curHeightList=[]
        elif(last_id!=cur_id  and last_id!='' and (last_id in IDList)):
            #find the index of this ID and add the list to them
            ind=IDList.index(last_id)
            timeLists[ind]=timeLists[ind]+curTimeList
            heightLists[ind]=heightLists[ind]+curHeightList
            latLists[ind]=latLists[ind]+curLatList
            lngLists[ind]=lngLists[ind]+curLngList
            curTimeList=[]
            curLatList=[]
            curLngList=[]
            curHeightList=[]
        else:
            if(heightHeader=='------'):
                curHeightList.append(0)
                # the add the information into list
                curLngList.append(row[lngHeader])
                curLatList.append(row[latHeader])
                curTimeList.append(row[timeHeader])
            else:   
                curHeightList.append(row[heightHeader])
                # the add the information into list
                curLngList.append(row[lngHeader])
                curLatList.append(row[latHeader])
                curTimeList.append(row[timeHeader])
            
        last_id=cur_id
    if(last_id not in IDList):
        #store the information of the last individual
        IDList.append(last_id)
        timeLists.append(curTimeList)
        heightLists.append(curHeightList)
        latLists.append(curLatList)
        lngLists.append(curLngList)
    else:
        #find the index of this ID and add the list to them
        ind=IDList.index(last_id)
        timeLists[ind]=timeLists[ind]+curTimeList
        heightLists[ind]=heightLists[ind]+curHeightList
        latLists[ind]=latLists[ind]+curLatList
        lngLists[ind]=lngLists[ind]+curLngList
        
    #after this process is done we can store them in d(Datasets)
    d.individuals=IDList
    d.timeLists=timeLists
    d.heightLists=heightLists
    d.latLists=latLists
    d.lngLists=lngLists
#show information of this individual
def preAnalysis(idName,d,iB):
    #find individual list
    IDList=d.individuals
    timeLists=d.timeLists
    heightLists=d.heightLists
    latLists=d.latLists
    lngLists=d.lngLists
    #get the index of give individual
    ind=IDList.index(idName)
    timeList=timeLists[ind]
    heightList=heightLists[ind]
    latList=latLists[ind]
    lngList=lngLists[ind]
    #get the whole number of datapoints
    iB.setDataPoints(len(timeList))
    #get the number of rows with missing values
    iB.missingHeight=heightList.count('')
    iB.missingLat=latList.count('')
    iB.missingLng=lngList.count('')
    num_Missing=max(iB.missingHeight,iB.missingLat,iB.missingLng)
    iB.setMissing(num_Missing)
    #get start lat lng height
    #get the first non-empty value of the list
    Lats=list(filter(lambda a: a != '', latList))
    Lngs=list(filter(lambda a: a != '', lngList))
    Heights=list(filter(lambda a: a != '', heightList))
    s_lat=''
    s_height=''
    s_lng=''
    e_lat=''
    e_lng=''
    e_height=''
    
    
    slat_id=0
    slng_id=0
    sh_id=0
    elat_id=0
    elng_id=0
    eh_id=0
    if(len(Lats)!=0):
          s_lat=Lats[0]
          e_lat=Lats[-1]
          slat_id=latList.index(s_lat)
          elat_id=latList.index(e_lat)
    if(len(Lngs)!=0):
          s_lng=Lngs[0]
          e_lng=Lngs[-1]
          slng_id=lngList.index(s_lng)
          elng_id=lngList.index(e_lng)
    if(len(Heights)!=0):
          s_height=Heights[0]
          e_height=Heights[-1]
          sh_id=heightList.index(s_height)
          eh_id=heightList.index(e_height)
    #get max of start id
    start_id=max(slat_id,slng_id,sh_id)
    end_id=max(elat_id,elng_id,eh_id)
    startPos='(lat={0},lng={1},height={2})'.format(s_lat,s_lng,s_height)
    endPos='(lat={0},lng={1},height={2})'.format(e_lat,e_lng,e_height)
    #set start and end pos
    iB.setStartPos(startPos)
    iB.setEndPos(endPos)
    #get Start and end timestamp
    startTime=timeList[start_id]
    endTime=timeList[end_id]
    iB.setStartTime(startTime)
    iB.setEndTime(endTime)
def PostAnalysis(idName,d,iB):
    #get information of sampled results
    getPostInfo(iB)
    #find orignial individual list
    IDList=d.individuals
    timeLists=d.timeLists
    heightLists=d.heightLists
    latLists=d.latLists
    lngLists=d.lngLists
    #find sampled dataset
    post_timeLists=iB.timeLists
    
    post_heightLists=iB.heightLists
    post_latLists=iB.latLists
    post_lngLists=iB.lngLists
    #get the index of give individual
    ind=IDList.index(idName)
    #orignial data
    timeList=timeLists[ind]
    heightList=heightLists[ind]
    latList=latLists[ind]
    lngList=lngLists[ind]
    
    ind2=iB.individuals.index(idName)
    post_timeList=post_timeLists[ind2]
    post_heightList=post_heightLists[ind2]
    post_latList=post_latLists[ind2]
    post_lngList=post_lngLists[ind2]
    # number of datapoints
    wholeNumber=len(timeList)
    # record compression ratio
    iB.compressionratio=(1-len(post_timeList)/wholeNumber)*100
    
    #####################calculate the SED of (lat,lng,height)####################################
    def calculateSED(lat,lng,height,time,LatList,LngList,HeightList,timeList):
            import math
            from datetime import datetime
            import decimal
            first_lat = float(LatList[0])
            first_lng = float(LngList[0])
            first_height = float(HeightList[0])
            first_timestamp = timeList[0]
            #print(first_timestamp)
            last_lat = float(LatList[-1])
            last_lng = float(LngList[-1])
            last_height = float(HeightList[-1])
            last_timestamp = timeList[-1]
            #print(last_timestamp)
            lastTimeObj=datetime.strptime(last_timestamp,'%Y-%m-%d %H:%M:%S.%f')
            firstTimeObj=datetime.strptime(first_timestamp,'%Y-%m-%d %H:%M:%S.%f')
            timeDiff=decimal.Decimal(abs((firstTimeObj-lastTimeObj).total_seconds()))
            #print(timeDiff)
            cur_timeObj=datetime.strptime(time,'%Y-%m-%d %H:%M:%S.%f')
            curtimeDiff=decimal.Decimal(abs((firstTimeObj-cur_timeObj).total_seconds()))
            # interpolate lat,lng,height
            lati=first_lat+ (last_lat-first_lat)*float(curtimeDiff*(1/timeDiff))
            lngi=first_lng+ (last_lng-first_lng)*float(curtimeDiff*(1/timeDiff))
            hi=first_height+ (last_height-first_height)*float(curtimeDiff*(1/timeDiff))
            #calculate sed value
            value = math.sqrt((lat-lati)**2+(lng-lngi)**2+(height-hi)**2)
            return value
    def averageSEDError(latList,lngList,heightList,timeList,post_latList,post_lngList,post_heightList,post_timeList):
        SEDs=[]
        #the List of datapoints that need to calculate
        cur_Lats=[]
        cur_Lngs=[]
        cur_hs=[]
        cur_ts=[]
        j=0
        post_lats=[]
        post_lngs=[]
        post_hs=[]
        post_ts=[]
        for i in range(0,len(timeList)):
            #find the datapoint that needs to calculate the SED
            if ((latList[i] not in post_latList)and (lngList[i] not in post_lngList) and (heightList[i] not in post_heightList)):
                lati = float(latList[i])
                cur_Lats.append(lati)
                lngi = float(lngList[i])
                cur_Lngs.append(lngi)
                heighti = float(heightList[i])
                cur_hs.append(heighti)
                timei = timeList[i]
                cur_ts.append(timei)
            elif(len(post_lats)==0):
                latj = float(post_latList[j])
                post_lats.append(latj)
                lngj = float(post_lngList[j])
                post_lngs.append(lngj)
                heightj = float(post_heightList[j])
                post_hs.append(heightj)
                timej = post_timeList[j]
                post_ts.append(timej)
                j=j+1
                if(j>=len(post_latList)):
                    break
            elif(len(cur_Lats)==0 and len(post_lats)>=1):
                post_lats=[]
                post_lngs=[]
                post_hs=[]
                post_ts=[]
                latj = float(post_latList[j])
                post_lats.append(latj)
                lngj = float(post_lngList[j])
                post_lngs.append(lngj)
                heightj = float(post_heightList[j])
                post_hs.append(heightj)
                timej = post_timeList[j]
                post_ts.append(timej)
                j=j+1
                if(j>=len(post_latList)):
                    break
            else:
                print(len(cur_Lats))
                latj = float(post_latList[j])
                post_lats.append(latj)
                lngj = float(post_lngList[j])
                post_lngs.append(lngj)
                heightj = float(post_heightList[j])
                post_hs.append(heightj)
                timej = post_timeList[j]
                post_ts.append(timej)
                #calculate SED and initialize the lists
                if(len(post_lats)<=1):
                    print("有问题<=1")
                elif(len(post_lats)>2):
                    print(">2不对")
                for k in range(0,len(cur_Lats)):
                    latk = float(cur_Lats[k])
                    lngk = float(cur_Lngs[k])
                    heightk = float(cur_hs[k])
                    timek = cur_ts[k]
                    sed=calculateSED(latk,lngk,heightk,timek,post_lats,post_lngs,post_hs,post_ts)
                    SEDs.append(sed)
                cur_Lats=[]
                cur_Lngs=[]
                cur_hs=[]
                cur_ts=[]
                post_lats=[]
                post_lngs=[]
                post_hs=[]
                post_ts=[]
                j=j+1
                if(j>=len(post_latList)):
                    break
        
        
        return SEDs
    SEDvaules=averageSEDError(latList,lngList,heightList,timeList,post_latList,post_lngList,post_heightList,post_timeList)
    SED_error_avg=sum(SEDvaules)/len(SEDvaules)
    iB.averageSED= SED_error_avg
    ###########compare the orignial and sampled trjectory############
    #prepare the 3D distance calculation
    import math
    def d_2points(lat1,lng1,h1,lat2,lng2,h2):
        R = 6371000 #radius of earth
        lng1=math.radians(float(lng1))
        lng2=math.radians(float(lng2))
        lat1=math.radians(float(lat1))
        lat2=math.radians(float(lat2))
        dlng = lng1-lng2
        dlat = lat1 - lat2
        
        dh= float(h1)-float(h2) 
        a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlng / 2)**2

        c = math.asin(math.sqrt(a))
        dis_horizontal = 2 *R * c
        dis =math.sqrt( dh**2+dis_horizontal**2)
        return dis
    #define the frechet algorithm
    #input: 2 trejectories output: infimum distance of 2 points along the trajectoy
    
    ##helper function: c(p,q) p,q are the index of point for 2 trjectories
    # recursive calculation to find the infimum
    def cal(ca,i,j,lats1,lngs1,hs1,lats2,lngs2,hs2,lookupTable):
        if lookupTable[i,j]!=-2 and lookupTable[i,j]!=float("inf"):
            return lookupTable[i,j]
        elif ca[i,j]>-1:
            return ca[i,j]
        elif i == 0 and j == 0:
            ca[i,j] =d_2points(lats1[0],lngs1[0],hs1[0],lats2[0],lngs2[0],hs2[0])
            
        elif i == 0 and j > 0:

            c1=cal(ca,0,j-1,lats1,lngs1,hs1,lats2,lngs2,hs2,lookupTable)
            ca[i,j] = max(c1,d_2points(lats1[0],lngs1[0],hs1[0],lats2[j],lngs2[j],hs2[j]))
        elif i>0 and j==0:

                c1=cal(ca,i-1,0,lats1,lngs1,hs1,lats2,lngs2,hs2,lookupTable)
                ca[i,j] = max(c1,d_2points(lats1[i],lngs1[i],hs1[i],lats2[0],lngs2[0],hs2[0]))
        elif i>0 and j>0:

                c1=cal(ca,i-1,j,lats1,lngs1,hs1,lats2,lngs2,hs2,lookupTable)
                c2=cal(ca,i-1,j-1,lats1,lngs1,hs1,lats2,lngs2,hs2,lookupTable)
                 

                c3=cal(ca,i,j-1,lats1,lngs1,hs1,lats2,lngs2,hs2,lookupTable)
                 
                ca[i,j] = max(min(c1,c2,c3),d_2points(lats1[i],lngs1[i],hs1[i],lats2[j],lngs2[j],hs2[j]))
        else:
            ca[i,j] = float("inf")
        lookupTable[i,j] = ca[i,j]
        return ca[i,j]
    import numpy as np  
    def frechet(lats1,lngs1,hs1,lats2,lngs2,hs2):
        p=len(latList)
        q=len(post_latList)
        
        ca = np.ones((p,q))
        ca = np.multiply(ca,-1)
        lookupTable = np.ones((p,q))
        lookupTable = np.multiply(lookupTable,-2)
        return cal(ca,p-1,q-1,lats1,lngs1,hs1,lats2,lngs2,hs2,lookupTable)
    try:
        iB.frechetDistance=frechet(latList,lngList,heightList,post_latList,post_lngList,post_heightList)
    except(RecursionError): 
        print("The max Recursion depth exceeded, please split the dataset first")
        iB.frechetDistance='This trajectoy has too many datapoints, please split that first'
    print('frechet distance is: '+str(iB.frechetDistance))
    ################compute the information loss degree based on the SED#########################
    SED_error_min = min(SEDvaules)
    SED_error_max = max(SEDvaules)
    iB.ILD =(SED_error_min+SED_error_max+SED_error_avg)/3 
    
    print('PostAnalysis finished')
    
#store the Lists in infoBuffer
def getPostInfo(iB):
    import csv
    timeLists=[]
    heightLists=[]
    latLists=[]
    lngLists=[]
    IDList=[]
    filePath = iB.fileLoc
    #base_dir+'/'+'filtered.csv'
    csv_file=open(filePath, encoding='utf-8')
    csv_reader = csv.DictReader(csv_file, delimiter=',')
    #create initial list for each individual
    cur_id=''
    last_id=''
    curTimeList=[]
    curLatList=[]
    curLngList=[]
    curHeightList=[]
    # find header names
    idHeader=iB.idHeaderName
    lngHeader = iB.lngHeaderName
    latHeader = iB.latHeaderName
    heightHeader = iB.heightHeaderName
    timeHeader = iB.timestampHeaderName
    for row in csv_reader:
        cur_id=row[idHeader]
        if ((last_id!=cur_id and last_id!='')):
            #collect information
            IDList.append(last_id)
            timeLists.append(curTimeList)
            heightLists.append(curHeightList)
            latLists.append(curLatList)
            lngLists.append(curLngList)
            curTimeList=[]
            curLatList=[]
            curLngList=[]
            curHeightList=[]
        else:
            if(heightHeader=='------'):
                curHeightList.append(0)
                # the add the information into list
                curLngList.append(row[lngHeader])
                curLatList.append(row[latHeader])
                curTimeList.append(row[timeHeader])
            else:   
                curHeightList.append(row[heightHeader])
                # the add the information into list
                curLngList.append(row[lngHeader])
                curLatList.append(row[latHeader])
                curTimeList.append(row[timeHeader])
        last_id=cur_id
    if(last_id not in IDList):
        #store the information of the last individual
        IDList.append(last_id)
        timeLists.append(curTimeList)
        heightLists.append(curHeightList)
        latLists.append(curLatList)
        lngLists.append(curLngList)
    else:
        #find the index of this ID and add the list to them
        ind=IDList.index(last_id)
        timeLists[ind]=timeLists[ind]+curTimeList
        heightLists[ind]=heightLists[ind]+curHeightList
        latLists[ind]=latLists[ind]+curLatList
        lngLists[ind]=lngLists[ind]+curLngList
    #store Information in infobuffer(sampled datapoint)
    iB.individuals=IDList
    iB.timeLists=timeLists
    iB.heightLists=heightLists
    iB.latLists=latLists
    iB.lngLists=lngLists

            
            
            
            
            
            
            
            