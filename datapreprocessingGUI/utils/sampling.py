# -*- coding: utf-8 -*-
"""
Created on Fri Nov  6 20:25:52 2020

@author: ZiyaoHe
"""
import os
import csv

'''
 from the first row of the same individual, 
 it takes for each n line and store into new csv
'''
def averageSampling(d,p,n,iB):
      
    #d:launch.d, p: launch.pSetups, n: sample for each n points
    base_dir = d.workdir
    filePath = d.filepath
    outpath = base_dir+'/'+'sample'# define the output folder
    if not os.path.exists(outpath):
            os.makedirs(outpath)
    csv_file=open(filePath, encoding='utf-8')
    csv_reader = csv.DictReader(csv_file, delimiter=',')
    fieldnames = csv_reader.fieldnames
    count=0
    last_id=''
    idHeader=p.idHeaderName
    
    csvfile_write = open(outpath+'/'+'average_sample_'+str(n)+'points.csv', 'a', newline='')
    writer = csv.DictWriter(csvfile_write
                                    ,fieldnames=fieldnames
                                    )
    writer.writeheader()
    
    for row in csv_reader:
        cur_id=row[idHeader]
        if last_id!=cur_id:
             count=1
             writer.writerow(row)
        else:
            # the sample individual
            count=count+1
            if((count-1)%n==0):
                writer.writerow(row)
            
        last_id=cur_id
    #record compression ratio
    iB.compressionratio=(1-(iB.numOfDatapoints % n)/iB.numOfDatapoints)*100
'''
Douglas peucker sampling:
  1.Find the first point A and last point B of the whole trajectory 
  2.Find the furtherst point C to line AB on the trajectory
  3.If the furtherst distance is less than our threshold then we use AB to represent the trajectory
    Else Do the same thing to line AC and BC
  O(n^2)
'''
def Douglas(d,p,epsilon,iB):
    import math
    import pandas as pd
    def d_2points(lat1,lng1,h1,lat2,lng2,h2):
        R = 6371000 #radius of earth
        lng1=math.radians(lng1)
        lng2=math.radians(lng2)
        lat1=math.radians(lat1)
        lat2=math.radians(lat2)
        dlng = lng1-lng2
        dlat = lat1 - lat2
        
        dh= h1-h2 
        a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlng / 2)**2

        c = math.asin(math.sqrt(a))
        dis_horizontal = 2 *R * c
        dis =math.sqrt( dh**2+dis_horizontal**2)
        return dis
    
    def d_pointLine(lat1,lng1,h1,lat2,lng2,h2,lat3,lng3,h3):
        try: 
            a=d_2points(lat1,lng1,h1,lat2,lng2,h2)
            b=d_2points(lat3,lng3,h3,lat2,lng2,h2)
            c=d_2points(lat1,lng1,h1,lat3,lng3,h3)
            s=(a+b+c)/2 
            A=math.sqrt(s*(s-a)*(s-b)*(s-c))  #Heron's formula
            
            return 2*A/a;# area of triangle ABC= 0.5*h*|AB| h= 2A/a  
        except:
            return 0
    def douglasAlgo(latList,lngList,heightList,timeList,epsilon):
        dmax = 0
        index = 0
        end = len(latList)
        #find the first and the last point
        lat1=float(latList[0])
        lng1=float(lngList[0])
        height1=float(heightList[0])
        lat2=float(latList[-1])
        lng2=float(lngList[-1])
        height2=float(heightList[-1])
        time1=timeList[0]
        time2=timeList[-1]
        #find the largest distance
        for i in range(1,end-1):
            lat=float(latList[i])
            lng=float(lngList[i])
            height=float(heightList[i])
            d = d_pointLine(lat1,lng1,height1,lat2,lng2,height2,lat,lng,height)
            if(d>dmax):
                index = i
                dmax = d
        
        out_latList=[]
        out_lngList=[]
        out_heightList=[]
        out_timeList=[]
        #out_idList=[]
        if(dmax>epsilon):
                latList1,lngList1,heightList1,timeList1= douglasAlgo(latList[:index],lngList[:index],heightList[:index],timeList[:index],epsilon)
                latList2,lngList2,heightList2,timeList2= douglasAlgo(latList[index:],lngList[index:],heightList[index:],timeList[index:],epsilon)
                out_latList=latList1+latList2
                out_lngList=lngList1+lngList2
                out_heightList=heightList1+heightList2
                out_timeList=timeList1+timeList2
            
        else:
            out_latList.append(lat1)
            out_latList.append(lat2)
            out_lngList.append(lng1)
            out_lngList.append(lng2)
            out_heightList.append(height1)
            out_heightList.append(height2)
            out_timeList.append(time1)
            out_timeList.append(time2)
        return out_latList,out_lngList,out_heightList,out_timeList
   
    base_dir = d.workdir
    filePath = d.filepath
    outpath = base_dir+'/'+'sample'# define the output folder
    if not os.path.exists(outpath):
            os.makedirs(outpath)
    csv_file=open(filePath, encoding='utf-8')
    csv_reader = csv.DictReader(csv_file, delimiter=',')
    
    #initialize
    last_id=''
    currentLngList=[]
    currentLatList=[]
    currentHeightList=[]
    currentTimeList=[]
    resultCSV=outpath+'/'+'douglas_sample_'+str(epsilon)+'meters.csv'
    # find header names
    idHeader=p.idHeaderName
    lngHeader = p.lngHeaderName
    latHeader = p.latHeaderName
    heightHeader = p.heightHeaderName
    timeHeader = p.timestampHeaderName
   
    # store the position 
    # and if the last_id!=cur_id
    # then we apply the Douglas algo to this individual
    for row in csv_reader:
        cur_id=row[idHeader]
        
        if ((last_id!=cur_id and last_id!='')):
             # 1.do the douglas for last id 
             # 2.store the data into new csv
             # 3.renew the list
             out_latList,out_lngList,out_heightList,out_timeList=douglasAlgo(currentLatList,currentLngList,currentHeightList,currentTimeList,epsilon)
             idList=[last_id]*len(out_latList)
             df=pd.DataFrame({
                   p.idHeaderName:idList,
                   p.timestampHeaderName:out_timeList,
                   p.lngHeaderName:out_lngList,
                   p.latHeaderName:out_latList,
                   p.heightHeaderName:out_heightList
                }
#                   ,[p.idHeaderName,
#                   p.timestampHeaderName,
#                   p.lngHeaderName,
#                   p.latHeaderName,
#                   p.heightHeaderName
#                   ]
                   )
             if(not os.path.exists(resultCSV)):
                 df=df.drop_duplicates(keep='first')
                 df.to_csv(resultCSV,index=False,header=True,mode='a')
             else:
                
                df=df.drop_duplicates(keep='first')
                df.to_csv(resultCSV,index=False,header=False,mode='a')
             #renew List
             currentLngList=[]
             currentLatList=[]
             currentHeightList=[]
             currentTimeList=[]
             if(heightHeader=='------'):
                currentHeightList.append(0)
                # the add the information into list
                currentLngList.append(row[lngHeader])
                currentLatList.append(row[latHeader])
                currentTimeList.append(row[timeHeader])
             else:   
                currentHeightList.append(row[heightHeader])
                # the add the information into list
                currentLngList.append(row[lngHeader])
                currentLatList.append(row[latHeader])
                currentTimeList.append(row[timeHeader])
        else:
            if(heightHeader=='------'):
                currentHeightList.append(0)
                # the add the information into list
                currentLngList.append(row[lngHeader])
                currentLatList.append(row[latHeader])
                currentTimeList.append(row[timeHeader])
            else:   
                currentHeightList.append(row[heightHeader])
                # the add the information into list
                currentLngList.append(row[lngHeader])
                currentLatList.append(row[latHeader])
                currentTimeList.append(row[timeHeader])
            
            
        last_id=cur_id
    out_latList,out_lngList,out_heightList,out_timeList=douglasAlgo(currentLatList,currentLngList,currentHeightList,currentTimeList,epsilon)
    idList=[last_id]*len(out_latList)
    df=pd.DataFrame({
           p.idHeaderName:idList,
           p.timestampHeaderName:out_timeList,
           p.lngHeaderName:out_lngList,
           p.latHeaderName:out_latList,
           p.heightHeaderName:out_heightList
        }
    #                   ,[p.idHeaderName,
    #                   p.timestampHeaderName,
    #                   p.lngHeaderName,
    #                   p.latHeaderName,
    #                   p.heightHeaderName
    #                   ]
           )
    if(not os.path.exists(resultCSV)):
             df=df.drop_duplicates(keep='first')
             df.to_csv(resultCSV,index=False,header=True,mode='a')
    else:
                
            df=df.drop_duplicates(keep='first')
            df.to_csv(resultCSV,index=False,header=False,mode='a')
    iB.fileLoc=resultCSV
    
#a top-down time-ratio algorithm based on DP
# the idea is to use Synchornized Euclidean Distance to compare with distance threshold
def TD_TR(d,p,dist_threshold,iB):
    import math
    import pandas as pd
    def d_2points(lat1,lng1,h1,lat2,lng2,h2):
        R = 6371000 #radius of earth
        lng1=math.radians(lng1)
        lng2=math.radians(lng2)
        lat1=math.radians(lat1)
        lat2=math.radians(lat2)
        dlng = lng1-lng2
        dlat = lat1 - lat2
        
        dh= h1-h2 
        a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlng / 2)**2

        c = math.asin(math.sqrt(a))
        dis_horizontal = 2 *R * c
        dis =math.sqrt( dh**2+dis_horizontal**2)
        return dis
    
    def d_pointLine(lat1,lng1,h1,lat2,lng2,h2,lat3,lng3,h3):
        try: 
            a=d_2points(lat1,lng1,h1,lat2,lng2,h2)
            b=d_2points(lat3,lng3,h3,lat2,lng2,h2)
            c=d_2points(lat1,lng1,h1,lat3,lng3,h3)
            s=(a+b+c)/2 
            A=math.sqrt(s*(s-a)*(s-b)*(s-c))  #Heron's formula
            
            return 2*A/a;# area of triangle ABC= 0.5*h*|AB| h= 2A/a  
        except:
            return 0
    def TD_TR_Algo(latList,lngList,heightList,timeList,dist_threshold):
            from datetime import datetime
            end = len(latList)
            if end<=2:
                return latList,lngList,heightList,timeList
            else:
                max_threshold=0
                index=0
                last_time=timeList[-1]
                first_time=timeList[0]
                lastTimeObj=datetime.strptime(last_time,iB.timestampReg)
                firstTimeObj=datetime.strptime(first_time,iB.timestampReg)
                delta_e=abs((firstTimeObj-lastTimeObj).total_seconds())
                #find the first and the last point
                lat1=float(latList[0])
                lng1=float(lngList[0])
                height1=float(heightList[0])
                lat2=float(latList[-1])
                lng2=float(lngList[-1])
                height2=float(heightList[-1])
                time1=timeList[0]
                time2=timeList[-1]
                
                for i in range(1,end-2):
                    cur_time=timeList[i]
                    cur_timeObj=datetime.strptime(cur_time,iB.timestampReg)
                    delta_i=abs((firstTimeObj-cur_timeObj).total_seconds())
                    #get time ratio
                    ratio=delta_i/delta_e
                    newLat=lat1+(lat2-lat1)*ratio
                    newLng=lng1+(lng2-lng1)*ratio
                    newHeight=height1+(height2-height1)*ratio
                    # calculate distance between the i-th point and our new position
                    dist=d_2points(lat1,lng1,height1,newLat,newLng,newHeight)
                    if(dist>max_threshold):
                        max_threshold=dist
                        index=i
                #initialize the output
                out_latList=[]
                out_lngList=[]
                out_heightList=[]
                out_timeList=[]
                if(max_threshold>dist_threshold):
                    latList1,lngList1,heightList1,timeList1= TD_TR_Algo(latList[:index],lngList[:index],heightList[:index],timeList[:index],dist_threshold)
                    latList2,lngList2,heightList2,timeList2= TD_TR_Algo(latList[index:],lngList[index:],heightList[index:],timeList[index:],dist_threshold)
                    out_latList=latList1+latList2
                    out_lngList=lngList1+lngList2
                    out_heightList=heightList1+heightList2
                    out_timeList=timeList1+timeList2
                else:
                    out_latList.append(lat1)
                    out_latList.append(lat2)
                    out_lngList.append(lng1)
                    out_lngList.append(lng2)
                    out_heightList.append(height1)
                    out_heightList.append(height2)
                    out_timeList.append(time1)
                    out_timeList.append(time2)
                return out_latList,out_lngList,out_heightList,out_timeList
                    
                         
            
    base_dir = d.workdir
    filePath = d.filepath
    outpath = base_dir+'/'+'sample'# define the output folder
    if not os.path.exists(outpath):
            os.makedirs(outpath)
    csv_file=open(filePath, encoding='utf-8')
    csv_reader = csv.DictReader(csv_file, delimiter=',')
    
    #initialize
    last_id=''
    currentLngList=[]
    currentLatList=[]
    currentHeightList=[]
    currentTimeList=[]
    resultCSV=outpath+'/'+'TDTR_sample_'+str(dist_threshold)+'meters.csv'
    # find header names
    idHeader=p.idHeaderName
    lngHeader = p.lngHeaderName
    latHeader = p.latHeaderName
    heightHeader = p.heightHeaderName
    timeHeader = p.timestampHeaderName
    # store the position 
    # and if the last_id!=cur_id
    # then we apply the Douglas algo to this individual
    for row in csv_reader:
        cur_id=row[idHeader]
        if ((last_id!=cur_id and last_id!='')):
             # 1.do the TD_TR for last id 
             # 2.store the data into new csv
             # 3.renew the list
             out_latList,out_lngList,out_heightList,out_timeList=TD_TR_Algo(currentLatList,currentLngList,currentHeightList,currentTimeList,dist_threshold)
             #Store info
             idList=[last_id]*len(out_latList)
             df=pd.DataFrame({
                   p.idHeaderName:idList,
                   p.timestampHeaderName:out_timeList,
                   p.lngHeaderName:out_lngList,
                   p.latHeaderName:out_latList,
                   p.heightHeaderName:out_heightList
                   })
             if(not os.path.exists(resultCSV)):
                 df=df.drop_duplicates(keep='first')
                 df.to_csv(resultCSV,index=False,header=True,mode='a')
             else:
                
                df=df.drop_duplicates(keep='first')
                df.to_csv(resultCSV,index=False,header=False,mode='a')
             #renew List
             currentLngList=[]
             currentLatList=[]
             currentHeightList=[]
             currentTimeList=[]
             if(heightHeader=='------'):
                currentHeightList.append(0)
                # the add the information into list
                currentLngList.append(row[lngHeader])
                currentLatList.append(row[latHeader])
                currentTimeList.append(row[timeHeader])
             else:   
                currentHeightList.append(row[heightHeader])
                # the add the information into list
                currentLngList.append(row[lngHeader])
                currentLatList.append(row[latHeader])
                currentTimeList.append(row[timeHeader])
        else:
            if(heightHeader=='------'):
                currentHeightList.append(0)
                # the add the information into list
                currentLngList.append(row[lngHeader])
                currentLatList.append(row[latHeader])
                currentTimeList.append(row[timeHeader])
            else:   
                currentHeightList.append(row[heightHeader])
                # the add the information into list
                currentLngList.append(row[lngHeader])
                currentLatList.append(row[latHeader])
                currentTimeList.append(row[timeHeader])
            
        last_id=cur_id
    out_latList,out_lngList,out_heightList,out_timeList=TD_TR_Algo(currentLatList,currentLngList,currentHeightList,currentTimeList,dist_threshold)
    idList=[last_id]*len(out_latList)
    df=pd.DataFrame({
           p.idHeaderName:idList,
           p.timestampHeaderName:out_timeList,
           p.lngHeaderName:out_lngList,
           p.latHeaderName:out_latList,
           p.heightHeaderName:out_heightList
        }
    #                   ,[p.idHeaderName,
    #                   p.timestampHeaderName,
    #                   p.lngHeaderName,
    #                   p.latHeaderName,
    #                   p.heightHeaderName
    #                   ]
           )
    if(not os.path.exists(resultCSV)):
             df=df.drop_duplicates(keep='first')
             df.to_csv(resultCSV,index=False,header=True,mode='a')
    else:
                
            df=df.drop_duplicates(keep='first')
            df.to_csv(resultCSV,index=False,header=False,mode='a')
    iB.fileLoc=resultCSV
   
#a top-down speed-ratio algorithm based on DP
def TD_SP(d,p,speed_threshold,iB):
    import math
    import pandas as pd
    def d_2points(lat1,lng1,h1,lat2,lng2,h2):
        R = 6371000 #radius of earth
        lng1=math.radians(lng1)
        lng2=math.radians(lng2)
        lat1=math.radians(lat1)
        lat2=math.radians(lat2)
        dlng = lng1-lng2
        dlat = lat1 - lat2
        
        dh= h1-h2 
        a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlng / 2)**2

        c = math.asin(math.sqrt(a))
        dis_horizontal = 2 *R * c
        dis =math.sqrt( dh**2+dis_horizontal**2)
        return dis
    
    def d_pointLine(lat1,lng1,h1,lat2,lng2,h2,lat3,lng3,h3):
        try: 
            a=d_2points(lat1,lng1,h1,lat2,lng2,h2)
            b=d_2points(lat3,lng3,h3,lat2,lng2,h2)
            c=d_2points(lat1,lng1,h1,lat3,lng3,h3)
            s=(a+b+c)/2 
            A=math.sqrt(s*(s-a)*(s-b)*(s-c))  #Heron's formula
            
            return 2*A/a;# area of triangle ABC= 0.5*h*|AB| h= 2A/a  
        except:
            return 0
    def TD_SP_Algo(latList,lngList,heightList,timeList,speed_threshold):
            from datetime import datetime
            end = len(latList)
            if end<=2:
                return latList,lngList,heightList,timeList
            else:
                max_threshold=0
                index=0
                for i in range(1,end-2):
                    lat1=float(latList[i])
                    lng1=float(lngList[i])
                    height1=float(heightList[i])
                    lat2=float(latList[i-1])
                    lng2=float(lngList[i-1])
                    height2=float(heightList[i-1])
                    lat3=float(latList[i+1])
                    lng3=float(lngList[i+1])
                    height3=float(heightList[i+1])
                    cur_time=timeList[i]
                    cur_timeObj=datetime.strptime(cur_time,iB.timestampReg)
                    last_time=timeList[i-1]
                    last_timeObj=datetime.strptime(last_time,iB.timestampReg)
                    #time diff between last timestamp to current timestamp
                    delta_t1=abs((last_timeObj-cur_timeObj).total_seconds())
                    next_time=timeList[i+1]
                    next_timeObj=datetime.strptime(next_time,iB.timestampReg)
                    #time diff between next timestamp to current timestamp
                    delta_t2=abs((next_timeObj-cur_timeObj).total_seconds()) 
                    # calculate distance between the i-th point and i-1 th position
                    dist1=d_2points(lat1,lng1,height1,lat2,lng2,height2)
                    # calculate distance between the i-th point and i+1 th position
                    dist2=d_2points(lat1,lng1,height1,lat3,lng3,height3)
                    #get speed between i-th to i-1 th
                    sp1=dist1/delta_t1
                    sp2=dist2/delta_t2
                    if(abs(sp1-sp2)>max_threshold):
                        max_threshold=abs(sp1-sp2)
                        index=i
                #initialize the output
                out_latList=[]
                out_lngList=[]
                out_heightList=[]
                out_timeList=[]
                if(max_threshold>speed_threshold):
                    latList1,lngList1,heightList1,timeList1= TD_SP_Algo(latList[:index],lngList[:index],heightList[:index],timeList[:index],speed_threshold)
                    latList2,lngList2,heightList2,timeList2= TD_SP_Algo(latList[index:],lngList[index:],heightList[index:],timeList[index:],speed_threshold)
                    out_latList=latList1+latList2
                    out_lngList=lngList1+lngList2
                    out_heightList=heightList1+heightList2
                    out_timeList=timeList1+timeList2
                else:
                    #find the first and the last point
                    lat1=float(latList[0])
                    lng1=float(lngList[0])
                    height1=float(heightList[0])
                    lat2=float(latList[-1])
                    lng2=float(lngList[-1])
                    height2=float(heightList[-1])
                    time1=timeList[0]
                    time2=timeList[-1]
                    out_latList.append(lat1)
                    out_latList.append(lat2)
                    out_lngList.append(lng1)
                    out_lngList.append(lng2)
                    out_heightList.append(height1)
                    out_heightList.append(height2)
                    out_timeList.append(time1)
                    out_timeList.append(time2)
                return out_latList,out_lngList,out_heightList,out_timeList
                    
                         
            
    base_dir = d.workdir
    filePath = d.filepath
    outpath = base_dir+'/'+'sample'# define the output folder
    if not os.path.exists(outpath):
            os.makedirs(outpath)
    csv_file=open(filePath, encoding='utf-8')
    csv_reader = csv.DictReader(csv_file, delimiter=',')
    
    #initialize
    last_id=''
    currentLngList=[]
    currentLatList=[]
    currentHeightList=[]
    currentTimeList=[]
    resultCSV=outpath+'/'+'TDSP_sample_'+str(speed_threshold)+'MProS.csv'
    # find header names
    idHeader=p.idHeaderName
    lngHeader = p.lngHeaderName
    latHeader = p.latHeaderName
    heightHeader = p.heightHeaderName
    timeHeader = p.timestampHeaderName
    # store the position 
    # and if the last_id!=cur_id
    # then we apply the Douglas algo to this individual
    for row in csv_reader:
        cur_id=row[idHeader]
        if ((last_id!=cur_id and last_id!='')):
             # 1.do the TD_TR for last id 
             # 2.store the data into new csv
             # 3.renew the list
             out_latList,out_lngList,out_heightList,out_timeList=TD_SP_Algo(currentLatList,currentLngList,currentHeightList,currentTimeList,speed_threshold)
             #Store info
             idList=[last_id]*len(out_latList)
             df=pd.DataFrame({
                   p.idHeaderName:idList,
                   p.timestampHeaderName:out_timeList,
                   p.lngHeaderName:out_lngList,
                   p.latHeaderName:out_latList,
                   p.heightHeaderName:out_heightList
                   })
             if(not os.path.exists(resultCSV)):
                 df=df.drop_duplicates(keep='first')
                 df.to_csv(resultCSV,index=False,header=True,mode='a')
             else:
                
                df=df.drop_duplicates(keep='first')
                df.to_csv(resultCSV,index=False,header=False,mode='a')
             
             #renew List
             currentLngList=[]
             currentLatList=[]
             currentHeightList=[]
             currentTimeList=[]
             if(heightHeader=='------'):
                currentHeightList.append(0)
                # the add the information into list
                currentLngList.append(row[lngHeader])
                currentLatList.append(row[latHeader])
                currentTimeList.append(row[timeHeader])
             else:   
                currentHeightList.append(row[heightHeader])
                # the add the information into list
                currentLngList.append(row[lngHeader])
                currentLatList.append(row[latHeader])
                currentTimeList.append(row[timeHeader])
        else:
            if(heightHeader=='------'):
                currentHeightList.append(0)
                # the add the information into list
                currentLngList.append(row[lngHeader])
                currentLatList.append(row[latHeader])
                currentTimeList.append(row[timeHeader])
            else:   
                currentHeightList.append(row[heightHeader])
                # the add the information into list
                currentLngList.append(row[lngHeader])
                currentLatList.append(row[latHeader])
                currentTimeList.append(row[timeHeader])
            
        last_id=cur_id
    out_latList,out_lngList,out_heightList,out_timeList=TD_SP_Algo(currentLatList,currentLngList,currentHeightList,currentTimeList,speed_threshold)
    idList=[last_id]*len(out_latList)
    df=pd.DataFrame({
           p.idHeaderName:idList,
           p.timestampHeaderName:out_timeList,
           p.lngHeaderName:out_lngList,
           p.latHeaderName:out_latList,
           p.heightHeaderName:out_heightList
        }
    #                   ,[p.idHeaderName,
    #                   p.timestampHeaderName,
    #                   p.lngHeaderName,
    #                   p.latHeaderName,
    #                   p.heightHeaderName
    #                   ]
           )
    if(not os.path.exists(resultCSV)):
             df=df.drop_duplicates(keep='first')
             df.to_csv(resultCSV,index=False,header=True,mode='a')
    else:
                
            df=df.drop_duplicates(keep='first')
            df.to_csv(resultCSV,index=False,header=False,mode='a')
    iB.fileLoc=resultCSV
    
def  SQUISH(d,p,size,iB):
    import pandas as pd
    def d_2points(lat1,lng1,h1,lat2,lng2,h2):
        import math
        R = 6371000 #radius of earth
        lng1=math.radians(lng1)
        lng2=math.radians(lng2)
        lat1=math.radians(lat1)
        lat2=math.radians(lat2)
        dlng = lng1-lng2
        dlat = lat1 - lat2
        
        dh= h1-h2 
        a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlng / 2)**2

        c = math.asin(math.sqrt(a))
        dis_horizontal = 2 *R * c
        dis =math.sqrt( dh**2+dis_horizontal**2)
        return dis
    # synchronized Euclidean distance
    # used to estimate the importance of one point in the trajectory
    # In order to make sure the speed of calculation, 
    # we assume the latitude longitude are evenly distributed
    
    #To implement this we need a size for the buffer, and the list of positions
    def SQUISH_Algo(latList,lngList,heightList,timeList,size):
        # update the whole SED list
        def updateSED(LatList,LngList,HeightList,timeList):
            import decimal
            import math
            from datetime import datetime
            length=len(LatList)
            value=0
            first_lat = LatList[0]
            first_lng = LngList[0]
            first_height = HeightList[0]
            first_timestamp = timeList[0]
            
            last_lat = LatList[-1]
            last_lng = LngList[-1]
            last_height = HeightList[-1]
            last_timestamp = timeList[-1]
            
            lastTimeObj=datetime.strptime(last_timestamp,iB.timestampReg)
            firstTimeObj=datetime.strptime(first_timestamp,iB.timestampReg)
            timeDiff=decimal.Decimal(abs((lastTimeObj-firstTimeObj).total_seconds()))
            sedList=[]
            for i in range(0,length):
                #get current location
                time =timeList[i]
                lat = LatList[i]
                lng = LngList[i]
                height = HeightList[i]
                cur_timeObj=datetime.strptime(time,iB.timestampReg)
                curtimeDiff=decimal.Decimal(abs((firstTimeObj-cur_timeObj).total_seconds()))
                # interpolate lat,lng,height
                lati=first_lat+ (last_lat-first_lat)*float(curtimeDiff*(1/timeDiff))
                lngi=first_lng+ (last_lng-first_lng)*float(curtimeDiff*(1/timeDiff))
                hi=first_height+ (last_height-first_height)*float(curtimeDiff*(1/timeDiff))
                #calculate sed value
                value = math.sqrt((lat-lati)**2+(lng-lngi)**2+(height-hi)**2)
                sedList.append(value)
            return sedList
        #calculate the SED of (lat,lng,height)
        def calculateSED(lat,lng,height,time,LatList,LngList,HeightList,timeList):
            import math
            from datetime import datetime
            import decimal
            first_lat = LatList[0]
            first_lng = LngList[0]
            first_height = HeightList[0]
            first_timestamp = timeList[0]
            print(first_timestamp)
            last_lat = LatList[-1]
            last_lng = LngList[-1]
            last_height = HeightList[-1]
            last_timestamp = timeList[-1]
            print(last_timestamp)
            lastTimeObj=datetime.strptime(last_timestamp,iB.timestampReg)
            firstTimeObj=datetime.strptime(first_timestamp,iB.timestampReg)
            timeDiff=decimal.Decimal(abs((firstTimeObj-lastTimeObj).total_seconds()))
            print(timeDiff)
            cur_timeObj=datetime.strptime(time,iB.timestampReg)
            curtimeDiff=decimal.Decimal(abs((firstTimeObj-cur_timeObj).total_seconds()))
            # interpolate lat,lng,height
            lati=first_lat+ (last_lat-first_lat)*float(curtimeDiff*(1/timeDiff))
            lngi=first_lng+ (last_lng-first_lng)*float(curtimeDiff*(1/timeDiff))
            hi=first_height+ (last_height-first_height)*float(curtimeDiff*(1/timeDiff))
            #calculate sed value
            value = math.sqrt((lat-lati)**2+(lng-lngi)**2+(height-hi)**2)
            return value
        # get the SED of given index
        def getSED(ind,LatList,LngList,HeightList,timeList):
            import math
            from datetime import datetime
            import decimal
            first_lat = LatList[0]
            first_lng = LngList[0]
            first_height = HeightList[0]
            first_timestamp = timeList[0]
            
            last_lat = LatList[-1]
            last_lng = LngList[-1]
            last_height = HeightList[-1]
            last_timestamp = timeList[-1]
            
            lat = LatList[ind]
            lng = LngList[ind]
            height = HeightList[ind]
            time = timeList[ind]
            
            lastTimeObj=datetime.strptime(last_timestamp,iB.timestampReg)
            firstTimeObj=datetime.strptime(first_timestamp,iB.timestampReg)
            timeDiff=decimal.Decimal(abs((firstTimeObj-lastTimeObj).total_seconds()))
            
            cur_timeObj=datetime.strptime(time,iB.timestampReg)
            curtimeDiff=decimal.Decimal(abs((firstTimeObj-cur_timeObj).total_seconds()))
            # interpolate lat,lng,height
            lati=first_lat+ (last_lat-first_lat)*float(curtimeDiff*(1/timeDiff))
            lngi=first_lng+ (last_lng-first_lng)*float(curtimeDiff*(1/timeDiff))
            hi=first_height+ (last_height-first_height)*float(curtimeDiff*(1/timeDiff))
            #calculate sed value
            value = math.sqrt((lat-lati)**2+(lng-lngi)**2+(height-hi)**2)
            return value
        
        out_latList=[]
        out_lngList=[]
        out_heightList=[]
        out_timeList=[]
        length=len(latList)
        #initialize a min of sed value
        sedList=[]
        for i in range(0,length):
            cur_lat=float(latList[i])
            cur_lng=float(lngList[i])
            cur_height=float(heightList[i])
            cur_time=timeList[i]
            
            if(len(out_latList)<size):
                #insert the point into buffer
                out_latList.append(cur_lat)
                out_lngList.append(cur_lng)
                out_heightList.append(cur_height)
                out_timeList.append(cur_time)
            else:
                
                
                sedList= updateSED(out_latList,out_lngList,out_heightList,out_timeList)
                #find the smallest sed
                min_sed= min(sedList)
                ind = sedList.index(min_sed)
                
                #remove the smallest sed index
                del out_latList[ind]
                del out_lngList[ind]
                del out_heightList[ind]
                del out_timeList[ind]
                del sedList[ind]
                #add new point to our list
                out_latList.append(cur_lat)
                out_lngList.append(cur_lng)
                out_heightList.append(cur_height)
                out_timeList.append(cur_time)
                #get the current sed of new point
                cur_SED=calculateSED(cur_lat,cur_lng,cur_height,cur_time,out_latList,out_lngList,out_heightList,out_timeList)
                sedList.append(cur_SED)
                #update the sed of its neighbor the current i th point
                if(ind==0):
                    sed=getSED(ind,out_latList,out_lngList,out_heightList,out_timeList)
                    sedList[ind]=sed
                elif(ind==int(size)-1):
                    #update second last element
                    sed_i1=updateSED(ind-1,out_latList,out_lngList,out_heightList,out_timeList)
                    sedList[ind-1]=sed_i1
                else:
                    #update 2 neighbors
                    sed_i1=updateSED(ind-1,out_latList,out_lngList,out_heightList,out_timeList)
                    sedList[ind-1]=sed_i1
                    sed_i2=updateSED(ind,out_latList,out_lngList,out_heightList,out_timeList)
                    sedList[ind]=sed_i2
        return out_latList,out_lngList,out_heightList,out_timeList
    base_dir = d.workdir
    filePath = d.filepath
    outpath = base_dir+'/'+'sample'# define the output folder
    if not os.path.exists(outpath):
            os.makedirs(outpath)
    csv_file=open(filePath, encoding='utf-8')
    csv_reader = csv.DictReader(csv_file, delimiter=',')
    
    #initialize
    last_id=''
    currentLngList=[]
    currentLatList=[]
    currentHeightList=[]
    currentTimeList=[]
    resultCSV=outpath+'/'+'SQUISH_sample_'+str(size)+'.csv'
    # find header names
    idHeader=p.idHeaderName
    lngHeader = p.lngHeaderName
    latHeader = p.latHeaderName
    heightHeader = p.heightHeaderName
    timeHeader = p.timestampHeaderName
    # store the position 
    # and if the last_id!=cur_id
    # then we apply the Douglas algo to this individual
    for row in csv_reader:
        cur_id=row[idHeader]
        if ((last_id!=cur_id and last_id!='')):
             # 1.do the TD_TR for last id 
             # 2.store the data into new csv
             # 3.renew the list
             out_latList,out_lngList,out_heightList,out_timeList=SQUISH_Algo(currentLatList,currentLngList,currentHeightList,currentTimeList,size)
             #Store info
             idList=[last_id]*len(out_latList)
             df=pd.DataFrame({
                   p.idHeaderName:idList,
                   p.timestampHeaderName:out_timeList,
                   p.lngHeaderName:out_lngList,
                   p.latHeaderName:out_latList,
                   p.heightHeaderName:out_heightList
                   })
             if(not os.path.exists(resultCSV)):
                 df=df.drop_duplicates(keep='first')
                 df.to_csv(resultCSV,index=False,header=True,mode='a')
             else:
                
                df=df.drop_duplicates(keep='first')
                df.to_csv(resultCSV,index=False,header=False,mode='a')
             
             #renew List
             currentLngList=[]
             currentLatList=[]
             currentHeightList=[]
             currentTimeList=[]
             if(heightHeader=='------'):
                currentHeightList.append(0)
                # the add the information into list
                currentLngList.append(row[lngHeader])
                currentLatList.append(row[latHeader])
                currentTimeList.append(row[timeHeader])
             else:   
                currentHeightList.append(row[heightHeader])
                # the add the information into list
                currentLngList.append(row[lngHeader])
                currentLatList.append(row[latHeader])
                currentTimeList.append(row[timeHeader])
        else:
            if(heightHeader=='------'):
                currentHeightList.append(0)
                # the add the information into list
                currentLngList.append(row[lngHeader])
                currentLatList.append(row[latHeader])
                currentTimeList.append(row[timeHeader])
            else:   
                currentHeightList.append(row[heightHeader])
                # the add the information into list
                currentLngList.append(row[lngHeader])
                currentLatList.append(row[latHeader])
                currentTimeList.append(row[timeHeader])
            
        last_id=cur_id
    out_latList,out_lngList,out_heightList,out_timeList= SQUISH_Algo(currentLatList,currentLngList,currentHeightList,currentTimeList,size)
    idList=[last_id]*len(out_latList)
    df=pd.DataFrame({
           p.idHeaderName:idList,
           p.timestampHeaderName:out_timeList,
           p.lngHeaderName:out_lngList,
           p.latHeaderName:out_latList,
           p.heightHeaderName:out_heightList
        }
    #                   ,[p.idHeaderName,
    #                   p.timestampHeaderName,
    #                   p.lngHeaderName,
    #                   p.latHeaderName,
    #                   p.heightHeaderName
    #                   ]
           )
    if(not os.path.exists(resultCSV)):
             df=df.drop_duplicates(keep='first')
             df.to_csv(resultCSV,index=False,header=True,mode='a')
    else:
                
            df=df.drop_duplicates(keep='first')
            df.to_csv(resultCSV,index=False,header=False,mode='a')
    iB.fileLoc=resultCSV
    
    