# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 14:57:24 2020

@author: heziy
"""
import os
import csv
# this step use the filtered data and the output will be stored under the same directory
def individualSpliting(d,p):#d is dataset, p is processingsetups
      base_dir = d.workdir
      #specify the critical headers
      idHeader=p.idHeaderName
      filePath = d.filepath
      #base_dir+'/'+'filtered.csv'
      splitpath = base_dir+'/'+'SplitByID'
      if not os.path.exists(splitpath):
               os.makedirs(splitpath)
      csv_file=open(filePath, encoding='utf-8')
      csv_reader = csv.DictReader(csv_file, delimiter=',')
      fieldnames = csv_reader.fieldnames
      
      individual_id=[]
      for row in csv_reader:
        if individual_id==[]:
            last_id=None
        else:
            last_id=individual_id[-1]
        cur_id=row[idHeader]
        cur_id=cur_id.replace("/","-")#avoid bad id names
        individual_id.append(cur_id)
        if last_id!=cur_id:
            #csvfile_write.close()
            newpath = splitpath+'/'+cur_id
            #newpath = newpath.replace(" ","")
            if not os.path.exists(newpath):
                   os.makedirs(newpath)
            resultCSV=newpath+'/'+cur_id+'.csv'
            
            if(not os.path.exists(resultCSV)):
                csvfile_write = open(resultCSV, 'a', newline='')
                writer = csv.DictWriter(csvfile_write
                                    ,fieldnames=fieldnames
                                    )
                writer.writeheader()
            csvfile_write = open(resultCSV, 'a', newline='')
            writer = csv.DictWriter(csvfile_write
                                    ,fieldnames=fieldnames
                                    )
            
            writer.writerow(row)
        else:
            
            writer.writerow(row)
# d is launch.d, p is launch.pSetup, 
# reg is the Regular language of Time, aim is the split by which time skip
def splitingTimeHighresolution(d,p,reg,aim,sec):
      from datetime import datetime
      base_dir = d.workdir
      splitpath = base_dir+'/'+'SplitByTimeStamp'+'/'+'highresolution'
      if not os.path.exists(splitpath):
             os.makedirs(splitpath)
      #specify the critical headers
#      idHeader=p.idHeaderName
#      latHeader=p.latHeaderName
#      lngHeader=p.lngHeaderName
#      heightHeader=p.heightHeaderName
      timestampHeader=p.timestampHeaderName
      filePath = d.filepath
      #base_dir+'/'+'filtered.csv'
      csv_file=open(filePath, encoding='utf-8')
      csv_reader = csv.DictReader(csv_file, delimiter=',')
      fieldnames = csv_reader.fieldnames
      
      
      if(aim=="1"):#Year
          threshold =31540000
          splitpath = splitpath + '/' + 'HighResolution_year'
      elif(aim=="2"):#Month
          threshold = 2628000
          splitpath = splitpath + '/' + 'HighResolution_month'
      elif(aim=="3"):#Day
          threshold = 86400
          splitpath = splitpath + '/' + 'HighResolution_day'
      elif(aim=="4"):#Hour
          threshold = 3600
          splitpath = splitpath + '/' + 'HighResolution_hour'
      elif(aim=="5"):#Minute
            
            threshold=60#the threshold in second
            splitpath = splitpath + '/' + 'HighResolution_minute'
      elif(aim=="6"): #Second
            
            threshold=float(sec)#the threshold in second
            splitpath = splitpath + '/' + 'HighResolution_second'
      lastTime=''
      count = 1

      if not os.path.exists(splitpath):
          os.makedirs(splitpath)
      for row in csv_reader:

          cur_time = row[timestampHeader]
          if (lastTime == ''):
              resultCSV = splitpath + '/' + str(count) + '.csv'
              if (not os.path.exists(resultCSV)):
                  csvfile_write = open(resultCSV, 'a', newline='')
                  writer = csv.DictWriter(csvfile_write
                                          , fieldnames=fieldnames
                                          )
                  writer.writeheader()
              csvfile_write = open(resultCSV, 'a', newline='')  # a for append (instead of overwrite)
              writer = csv.DictWriter(csvfile_write, fieldnames=fieldnames)
              writer.writerow(row)
          else:
              lastTimeObj = datetime.strptime(lastTime, reg)
              cur_timeObj = datetime.strptime(cur_time, reg)
              TimeDiff = abs((cur_timeObj - lastTimeObj).total_seconds())
              if (TimeDiff <= threshold):
                  writer.writerow(row)
              else:
                  count = count + 1
                  resultCSV = splitpath + '/' + str(count) + '.csv'
                  if (not os.path.exists(resultCSV)):
                      csvfile_write = open(resultCSV, 'a', newline='')
                      writer = csv.DictWriter(csvfile_write
                                              , fieldnames=fieldnames
                                              )
                      writer.writeheader()
                  csvfile_write = open(resultCSV, 'a', newline='')  # a for append (instead of overwrite)
                  writer = csv.DictWriter(csvfile_write, fieldnames=fieldnames)
                  writer.writerow(row)
          lastTime = cur_time
      print("finished")
      
      return
# store for each time skip a file
def splitingTime(d,p,reg,aim,sec):
    from datetime import datetime
    base_dir = d.workdir
    splitpath = base_dir + '/' + 'SplitByTimeStamp'+'/'+'ForeachTimeskip'
    if not os.path.exists(splitpath):
        os.makedirs(splitpath)
    # specify the critical headers
    #      idHeader=p.idHeaderName
    #      latHeader=p.latHeaderName
    #      lngHeader=p.lngHeaderName
    #      heightHeader=p.heightHeaderName
    timestampHeader = p.timestampHeaderName
    filePath = d.filepath
    # base_dir+'/'+'filtered.csv'
    csv_file = open(filePath, encoding='utf-8')
    csv_reader = csv.DictReader(csv_file, delimiter=',')
    fieldnames = csv_reader.fieldnames

    if (aim == "1"):  # Year
        lastYear = 99999  # initialize last time
        splitpath = splitpath + '/' + 'ByYear'
        if not os.path.exists(splitpath):
            os.makedirs(splitpath)
        for row in csv_reader:
            cur_time = row[timestampHeader]
            cur_timeObj = datetime.strptime(cur_time, reg)
            cur_Year = cur_timeObj.year
            if lastYear != cur_Year:  # not the same year
                newpath = splitpath
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
                resultCSV = newpath + '/' + str(cur_Year) + '.csv'
                if (not os.path.exists(resultCSV)):
                    csvfile_write = open(resultCSV, 'a', newline='')
                    writer = csv.DictWriter(csvfile_write
                                            , fieldnames=fieldnames
                                            )
                    writer.writeheader()
                csvfile_write = open(resultCSV, 'a', newline='')  # a for append (instead of overwrite)
                writer = csv.DictWriter(csvfile_write, fieldnames=fieldnames)
                writer.writerow(row)

            else:

                writer.writerow(row)
            lastYear = cur_Year
    elif (aim == "2"):  # Month
        lastYear = 99999  # initialize last Year
        lastMonth = 99999  # initialize last Month
        splitpath = splitpath + '/' + 'ByMonth'
        if not os.path.exists(splitpath):
            os.makedirs(splitpath)
        for row in csv_reader:

            cur_time = row[timestampHeader]

            cur_time = row[timestampHeader]
            cur_timeObj = datetime.strptime(cur_time, reg)
            cur_Year = cur_timeObj.year
            cur_Month = cur_timeObj.month
            if (lastYear != cur_Year or lastMonth != cur_Month):  # not the same Month
                newpath = splitpath + '/' + str(cur_Year)
                # newpath = newpath.replace(" ","")
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
                resultCSV = newpath + '/' + str(cur_Month) + '.csv'
                if (not os.path.exists(resultCSV)):
                    csvfile_write = open(resultCSV, 'a', newline='')
                    writer = csv.DictWriter(csvfile_write
                                            , fieldnames=fieldnames
                                            )
                    writer.writeheader()
                csvfile_write = open(resultCSV, 'a', newline='')  # a for append (instead of overwrite)
                writer = csv.DictWriter(csvfile_write, fieldnames=fieldnames)
                writer.writerow(row)

            else:

                writer.writerow(row)
            lastYear = cur_Year
            lastMonth = cur_Month
    elif (aim == "3"):  # Day
        lastYear = 99999  # initialize last Year
        lastMonth = 99999  # initialize last Month
        lastDay = 99999  # initialize last Day
        splitpath = splitpath + '/' + 'ByDay'
        if not os.path.exists(splitpath):
            os.makedirs(splitpath)
        for row in csv_reader:

            cur_time = row[timestampHeader]

            cur_timeObj = datetime.strptime(cur_time, reg)
            cur_Year = cur_timeObj.year
            cur_Month = cur_timeObj.month
            cur_Day = cur_timeObj.day
            if lastYear != cur_Year or lastMonth != cur_Month or lastDay != cur_Day:  # not the same Day
                newpath = splitpath + '/' + str(cur_Year) + '-' + str(cur_Month)
                # newpath = newpath.replace(" ","")
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
                resultCSV = newpath + '/' + str(cur_Day) + '.csv'
                if (not os.path.exists(resultCSV)):
                    csvfile_write = open(resultCSV, 'a', newline='')
                    writer = csv.DictWriter(csvfile_write
                                            , fieldnames=fieldnames
                                            )
                    writer.writeheader()
                csvfile_write = open(resultCSV, 'a', newline='')  # a for append (instead of overwrite)
                writer = csv.DictWriter(csvfile_write, fieldnames=fieldnames)
                writer.writerow(row)

            else:

                writer.writerow(row)
            lastYear = cur_Year
            lastMonth = cur_Month
            lastDay = cur_Day
    elif (aim=="4"):# hour
        lastYear = 99999  # initialize last Year
        lastMonth = 99999  # initialize last Month
        lastDay = 99999  # initialize last Day
        lastHour = 99999 # initialize the hour
        lastMinute = 99999# initialize last Minute value
        splitpath = splitpath + '/' + 'ByHour'
        if not os.path.exists(splitpath):
            os.makedirs(splitpath)
        for row in csv_reader:

            cur_time = row[timestampHeader]

            cur_timeObj = datetime.strptime(cur_time, reg)
            cur_Year = cur_timeObj.year
            cur_Month = cur_timeObj.month
            cur_Day = cur_timeObj.day
            cur_Hour = cur_timeObj.hour
            if lastYear != cur_Year or lastMonth != cur_Month or lastDay != cur_Day or cur_Hour!=lastHour :  # not the same hour
                newpath = splitpath + '/' + str(cur_Year) + '-' + str(cur_Month)+'-'+str(cur_Day)
                # newpath = newpath.replace(" ","")
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
                resultCSV = newpath + '/' + str(cur_Hour) + '.csv'
                if (not os.path.exists(resultCSV)):
                    csvfile_write = open(resultCSV, 'a', newline='')
                    writer = csv.DictWriter(csvfile_write
                                            , fieldnames=fieldnames
                                            )
                    writer.writeheader()
                csvfile_write = open(resultCSV, 'a', newline='')  # a for append (instead of overwrite)
                writer = csv.DictWriter(csvfile_write, fieldnames=fieldnames)
                writer.writerow(row)

            else:

                writer.writerow(row)
            lastYear = cur_Year
            lastMonth = cur_Month
            lastDay = cur_Day
            lastHour = cur_Hour
    elif (aim == "5"):  # Minute
        lastYear = 99999  # initialize last Year
        lastMonth = 99999  # initialize last Month
        lastDay = 99999  # initialize last Day
        lastHour = 99999  # initialize the hour
        lastMinute = 99999  # initialize last Minute value
        splitpath = splitpath + '/' + 'ByMinute'
        if not os.path.exists(splitpath):
            os.makedirs(splitpath)
        for row in csv_reader:

            cur_time = row[timestampHeader]

            cur_timeObj = datetime.strptime(cur_time, reg)
            cur_Year = cur_timeObj.year
            cur_Month = cur_timeObj.month
            cur_Day = cur_timeObj.day
            cur_Hour = cur_timeObj.hour
            cur_Minute = cur_timeObj.minute
            if lastYear != cur_Year or lastMonth != cur_Month or lastDay != cur_Day or cur_Hour!=lastHour  or lastMinute != cur_Minute:  # not the same Minute
                newpath = splitpath + '/' + str(cur_Year) + '-' + str(cur_Month)+'-'+str(cur_Day)+' '+str(cur_Hour)+'h'
                # newpath = newpath.replace(" ","")
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
                resultCSV = newpath + '/' + str(cur_Minute) + '.csv'
                if (not os.path.exists(resultCSV)):
                    csvfile_write = open(resultCSV, 'a', newline='')
                    writer = csv.DictWriter(csvfile_write
                                            , fieldnames=fieldnames
                                            )
                    writer.writeheader()
                csvfile_write = open(resultCSV, 'a', newline='')  # a for append (instead of overwrite)
                writer = csv.DictWriter(csvfile_write, fieldnames=fieldnames)
                writer.writerow(row)

            else:

                writer.writerow(row)
            lastYear = cur_Year
            lastMonth = cur_Month
            lastDay = cur_Day
            lastHour = cur_Hour
            lastMinute = cur_Minute
    elif (aim == "6"):  # Second
        # lastYear = 99999  # initialize last Year
        # lastMonth = 99999  # initialize last Month
        # lastDay = 99999  # initialize last Day
        # lastHour = 99999 # initialize the hour
        # lastMinute = 99999  # initialize last Minute value
        # import numpy as np
        #lastSecond = np.iinfo(np.int32).max  # initialize the second
        last_timeObj = None
        splitpath = splitpath + '/' + 'Foreach'+str(sec)+'Second'
        count = 1
        if not os.path.exists(splitpath):
            os.makedirs(splitpath)
        for row in csv_reader:

            cur_time = row[timestampHeader]

            cur_timeObj = datetime.strptime(cur_time, reg)


            cur_Year = cur_timeObj.year
            cur_Month = cur_timeObj.month
            cur_Day = cur_timeObj.day
            cur_Hour = cur_timeObj.hour
            cur_Minute = cur_timeObj.minute
            #cur_Second = cur_timeObj.second
            if (count == 1):
                newpath = splitpath + '/' + str(cur_Year) + '-' + str(cur_Month) + '-' + str(cur_Day) + ' ' + str(
                    cur_Hour) + 'h' + str(cur_Minute) + 'm'

                if not os.path.exists(newpath):
                    os.makedirs(newpath)
                resultCSV = newpath + '/' + str(count * float(sec)) + '.csv'
                if (not os.path.exists(resultCSV)):
                    csvfile_write = open(resultCSV, 'a', newline='')
                    writer = csv.DictWriter(csvfile_write
                                            , fieldnames=fieldnames
                                            )
                    writer.writeheader()
                csvfile_write = open(resultCSV, 'a', newline='')  # a for append (instead of overwrite)
                writer = csv.DictWriter(csvfile_write, fieldnames=fieldnames)
                writer.writerow(row)
                last_timeObj = cur_timeObj
                count += 1
            if(abs((cur_timeObj-last_timeObj).total_seconds())>float(sec)):
                    newpath = splitpath + '/' + str(cur_Year) + '-' + str(cur_Month) + '-' + str(cur_Day) + ' ' + str(
                        cur_Hour) + 'h' + str(cur_Minute) + 'm'
                    # newpath = newpath.replace(" ","")
                    if not os.path.exists(newpath):
                        os.makedirs(newpath)
                    resultCSV = newpath + '/' + str(count*float(sec)) + '.csv'
                    if (not os.path.exists(resultCSV)):
                        csvfile_write = open(resultCSV, 'a', newline='')
                        writer = csv.DictWriter(csvfile_write
                                                , fieldnames=fieldnames
                                                )
                        writer.writeheader()
                    csvfile_write = open(resultCSV, 'a', newline='')  # a for append (instead of overwrite)
                    writer = csv.DictWriter(csvfile_write, fieldnames=fieldnames)
                    writer.writerow(row)
                    last_timeObj = cur_timeObj
                    count += 1

            else:

                writer.writerow(row)



