# -*- coding: utf-8 -*-
"""
Created on Thu Sep 24 14:37:00 2020

@author: heziy
"""

import tkinter as tk
from tkinter import ttk
import tkinter.filedialog  as fd

import timeit



#setup tab1:
#   tab1 includes: select directory, select csv file' button , 
#   their label to explain the function

def setupTab1(tab):
     from utils.loadData import setupData,setupWorkdir
     ########### Select directory path ###################
     # Label for information
     tab1_TextLabel = ttk.Label(tab, text= "Please select a directory for preprocessing, the output will be saved in this directory")
     tab1_TextLabel.place(relx = 0.1, rely = 0.05)
     
     # Button select dataset
     btn1 = ttk.Button(tab, text ='Select directory', command = lambda:open_dir()) 
     btn1.place(relx = 0.8, rely = 0.1)
     # Show the directory path
     strPath = tk.StringVar()
     ttk.Entry(tab,textvariable = strPath,
           width=65).place(
           relx=0.1,rely=0.1,
           height=30
           )
     import launchGUI
     def open_dir():
         try:
           
           strPath.set('')
           filePath = fd.askdirectory()  
           if(filePath != ''):
                strPath.set(filePath)
                
                
                
                setupWorkdir(filePath, launchGUI.d)
         except:pass
     ########### Select csv ###################
     tab1_TextLabel2 = ttk.Label(tab, text= "Please select your dataset(csv)")
     tab1_TextLabel2.place(relx = 0.1, rely = 0.2)
     btn2 = ttk.Button(tab, text ='Select file', command = lambda:open_dataset()) 
     btn2.place(relx = 0.8, rely = 0.25)
     
     #select a file
     strFname = tk.StringVar()
     ttk.Entry(tab,textvariable = strFname,
                 width=65).place(
                 relx=0.1,rely=0.25,
                 height=30
                 )
     def open_dataset():
           
           
           filename =  fd.askopenfilename(title="Select your dataset") 
           if(filename != ''):
                
                strFname.set(filename)
                
                
                try:
                      #setup csv.DictReader, filepath, workdir 
                      setupData(filename, launchGUI.d)
                      choices1=launchGUI.d.headers
                      multibox1.config(values=choices1)
                      choices2=launchGUI.d.headers
                      multibox2.config(values=choices2)
                      choices3=launchGUI.d.headers
                      multibox3.config(values=choices3)
                      choices4=launchGUI.d.headers
                      multibox4.config(values=choices4)
                      choices5= launchGUI.d.headers + ['------']
                      multibox5.config(values=choices5)
                      
                except: 
                    print('there is something wrong in gui genderation(Tab1)')
                updateTab2(launchGUI.main.tab2, launchGUI.d)

      ############ define the headers for important information #############
     def getHeader1(event):#id
         idHeader=multibox1.get()
         import launchGUI
         launchGUI.pSetups.idHeaderName=idHeader
         if idHeader not in launchGUI.pSetups.choosenHeaders:
             launchGUI.pSetups.choosenHeaders.append(idHeader)
         launchGUI.iB.idHeaderName=idHeader
         print(launchGUI.pSetups.idHeaderName)
     def getHeader2(event):#time
         timeHeader=multibox2.get()
         import launchGUI
         launchGUI.pSetups.timestampHeaderName=timeHeader
         if timeHeader not in launchGUI.pSetups.choosenHeaders:
             launchGUI.pSetups.choosenHeaders.append(timeHeader)
         launchGUI.iB.timestampHeaderName=timeHeader
         print(launchGUI.pSetups.timestampHeaderName)
     def getHeader3(event):#lat
         latHeader=multibox3.get()
         import launchGUI
         launchGUI.pSetups.latHeaderName=latHeader
         if latHeader not in launchGUI.pSetups.choosenHeaders:
             launchGUI.pSetups.choosenHeaders.append(latHeader)
         launchGUI.iB.latHeaderName=latHeader
         print(launchGUI.pSetups.latHeaderName)
     def getHeader4(event):#lng
         lngHeader=multibox4.get()
         import launchGUI
         launchGUI.pSetups.lngHeaderName=lngHeader
         if lngHeader not in launchGUI.pSetups.choosenHeaders:
             launchGUI.pSetups.choosenHeaders.append(lngHeader)
         launchGUI.iB.lngHeaderName=lngHeader
         print(launchGUI.pSetups.lngHeaderName)
     def getHeader5(event):#height
         heightHeader=multibox5.get()
         import launchGUI
         launchGUI.pSetups.heightHeaderName=heightHeader
         if heightHeader not in launchGUI.pSetups.choosenHeaders:
             launchGUI.pSetups.choosenHeaders.append(heightHeader)
         launchGUI.iB.heightHeaderName=heightHeader
         print(launchGUI.pSetups.heightHeaderName)
     tab1_TextLabel3 = ttk.Label(tab, text= "Please define the critical header names below")
     tab1_TextLabel3.place(relx = 0.3, rely = 0.35) 
     
     tab1_TextLabel4 = ttk.Label(tab, text= "Id: ")
     tab1_TextLabel4.place(relx = 0.1, rely = 0.4) 
     choices1=[]
     multibox1=ttk.Combobox(tab,values=choices1
                           ,width=40
                           ,font=12
                           )
     multibox1.place(relx = 0.4, rely = 0.4)  
     multibox1.bind("<<ComboboxSelected>>", getHeader1)
     tab1_TextLabel5 = ttk.Label(tab, text= "Timestamp: ")
     tab1_TextLabel5.place(relx = 0.1, rely = 0.5) 
     choices2=[]
     multibox2=ttk.Combobox(tab,values=choices2
                           ,width=40
                           ,font=12
                           )
     multibox2.place(relx = 0.4, rely = 0.5)
     multibox2.bind("<<ComboboxSelected>>", getHeader2)
     tab1_TextLabel6 = ttk.Label(tab, text= "Latitude: ")
     tab1_TextLabel6.place(relx = 0.1, rely = 0.6) 
     choices3=[]
     multibox3=ttk.Combobox(tab,values=choices3
                           ,width=40
                           ,font=12
                           )
     multibox3.place(relx = 0.4, rely = 0.6)  
     multibox3.bind("<<ComboboxSelected>>", getHeader3)
     tab1_TextLabel7 = ttk.Label(tab, text= "Longitude: ")
     tab1_TextLabel7.place(relx = 0.1, rely = 0.7) 
     choices4=[]
     multibox4=ttk.Combobox(tab,values=choices4
                           ,width=40
                           ,font=12
                           )
     multibox4.place(relx = 0.4, rely = 0.7)  
     multibox4.bind("<<ComboboxSelected>>", getHeader4)
     tab1_TextLabel8 = ttk.Label(tab, text= "Height: ")
     tab1_TextLabel8.place(relx = 0.1, rely = 0.8) 
     choices5=[]
     multibox5=ttk.Combobox(tab,values=choices5
                           ,width=40
                           ,font=12
                           )
     multibox5.place(relx = 0.4, rely = 0.8)  
     multibox5.bind("<<ComboboxSelected>>", getHeader5)
     def confirmSelection():
         from utils.DataReport import getIndividualNum
         from launchGUI import d,pSetups,main
         getIndividualNum(d,pSetups)
         setupTab7(main.tab7)
         main.tabNotebook.select(main.tab7)
         #updateTab8(main.tab8)
     #confirm Button
     btn3 = ttk.Button(tab, text ='Preanalysis', command = lambda:confirmSelection()) 
     btn3.place(relx = 0.8, rely = 0.9)
#setup tab2: 
#   tab2 includes: mutiple selection of headers we want to keep, launch button , 
#   their label to explain the function
#    

def setupTab2(tab):
      
      
      
      tab2_TextLabel1 = ttk.Label(tab, text= "Please choose the headers you want to keep")
      tab2_TextLabel1.place(relx = 0.1, rely = 0.1)
      
      
def updateTab2(tab,d):
      
      #clean tab
      for child in tab.winfo_children():
           child.destroy()
      s = ttk.Style()
      bg = s.lookup('TFrame', 'background')
      
      listbox = tk.Listbox(tab, selectmode = "multiple"  
               ) 
      scrollbar = tk.Scrollbar(listbox,orient=tk.VERTICAL)
      scrollbar.pack( side = tk.RIGHT, fill = 'y')
      listbox.config(yscrollcommand = scrollbar.set)
      listbox.place(relx = 0.1, rely = 0.2,
                    height = 400,width=500) 
     
      
      tab2_TextLabel1 = ttk.Label(tab, text= "Please choose the headers you want to keep")
      tab2_TextLabel1.place(relx = 0.1, rely = 0.1)
      headerList = d.headers
      count=1
      for i in headerList:
            #print(i)
             listbox.insert(tk.END, i) 
             listbox.config(bg = bg) 
             count=count+1
       #setup checkbox for default setting
      var1=tk.BooleanVar()
      checkBtn=ttk.Checkbutton(tab, text="Use Default", variable=var1)
      def selectValues(chosen):
          for c in chosen:
              #get list index 
              ind=listbox.get(0, tk.END).index(c)
              listbox.select_set(ind)
      def deselectValues(chosen):
          #get current selections 
          curSelections=listbox.curselection()
          #clear all selections
          listbox.selection_clear(0,tk.END)
          curSelectionsL=list(curSelections)
          #select the rest
          for c in chosen:
              #get list index 
              ind=listbox.get(0, tk.END).index(c)
              curSelectionsL.remove(ind)
          for s in curSelectionsL:
              #get list index 
              listbox.select_set(s)
      def useDefault(event):
            import launchGUI
            #the user use the default headers and the headers they selected
            if(not var1.get()):
                launchGUI.pSetups.useDefaultInfo()
                selectValues(launchGUI.pSetups.choosenHeaders)
                print("Use default info")
            else:
                
                deselectValues(launchGUI.pSetups.choosenHeaders)
                launchGUI.pSetups.cleanDefaultInfo()
                print("Deselect default info")
      checkBtn.bind("<ButtonPress>",useDefault)
      checkBtn.place(relx = 0.75, rely = 0.8)
      #setup checkbox to restore last configuration
      var2=tk.BooleanVar()
      checkBtn2=ttk.Checkbutton(tab, text="Restore Last Configuration", variable=var2)
      
      def useLast(event):
            import launchGUI
            #the user use the default headers and the headers they selected
            if(not var2.get()):
                launchGUI.pSetups.updateLastInfo()
                selectValues(launchGUI.pSetups.choosenHeaders)
                print("Use last info")
            else:
                deselectValues(launchGUI.pSetups.choosenHeaders)
                
                launchGUI.pSetups.cleanLasttInfo()
                print("Deselect last info")
      checkBtn2.bind("<ButtonPress>",useLast)
      checkBtn2.place(relx = 0.75, rely = 0.7)
      
      #confirm button
      btn1 = ttk.Button(tab, text ='Confirm', command = lambda:confirm()) 
      btn1.place(relx = 0.8, rely = 0.9)
      #once the update is done jump to new tab
      #
      def confirm():
            import launchGUI
            iB=launchGUI.iB
            values = [str(listbox.get(idx)) for idx in listbox.curselection()]

            launchGUI.pSetups.choosenHeaders= launchGUI.pSetups.choosenHeaders + values
            #make value unique
            launchGUI.pSetups.choosenHeaders=list(set(launchGUI.pSetups.choosenHeaders))
            launchGUI.pSetups.setBasicInfo(iB.idHeaderName, iB.latHeaderName, iB.lngHeaderName, iB.heightHeaderName, iB.timestampHeaderName)
            print (', '.join(launchGUI.pSetups.choosenHeaders))

            from utils.datafiltering import filtering
            filtering(launchGUI.pSetups.choosenHeaders, launchGUI.d)
            launchGUI.pSetups.storeLastInfo()
            
            
                  
#setup tab3: 
#   tab3 includes: selection of mehtods, launch button , 
#   their label to explain the function
# 

def setupTab3(tab):
     # Label for information
     tab4_TextLabel1 = ttk.Label(tab, text= "Here you can decide whether to split by individual's ID or year, month etc.")
     tab4_TextLabel1.place(relx = 0.1, rely = 0.1)
     v = tk.StringVar(tab,"1") 
     checkbox1=ttk.Radiobutton(tab, text="Split by timestamp", variable=v,value="1")
     checkbox1.place(relx = 0.1, rely = 0.2)
     checkbox2=ttk.Radiobutton(tab, text="Split by individual", variable=v,value="2")
     checkbox2.place(relx = 0.1, rely = 0.8)
     v2 = tk.StringVar(tab,"1")
     # entry for year
     checkbox3=ttk.Radiobutton(tab, text="Year", variable=v2,value="1")
     checkbox3.place(relx = 0.1, rely = 0.3)
     
     # entry for month
     checkbox4=ttk.Radiobutton(tab, text="Month", variable=v2,value="2")
     checkbox4.place(relx = 0.2, rely = 0.3)
     
     #  entry for day
     checkbox5=ttk.Radiobutton(tab, text="Day", variable=v2,value="3")
     checkbox5.place(relx = 0.3, rely = 0.3)
     
     #  entry for min
     checkbox6=ttk.Radiobutton(tab, text="Hour", variable=v2,value="4")
     checkbox6.place(relx = 0.4, rely = 0.3)
     #  entry for min
     checkbox7=ttk.Radiobutton(tab, text="Minute", variable=v2,value="5")
     checkbox7.place(relx = 0.5, rely = 0.3)
     # entry for seconds
     checkbox7=ttk.Radiobutton(tab, text="Second", variable=v2,value="6")
     checkbox7.place(relx = 0.6, rely = 0.3)
     
     # Label for information
     tab4_TextLabel3 = ttk.Label(tab, text= "If the regular language of timestamp doesn't match, you can write your own:")
     tab4_TextLabel3.place(relx = 0.1, rely = 0.4)
     
     # Label for information
     defaultReg=tk.StringVar()
     defaultReg.set('%Y-%m-%d %H:%M:%S.%f')
     import launchGUI
     launchGUI.iB.timestampReg= '%Y-%m-%d %H:%M:%S.%f'
     entry1=tk.Entry(tab,
           width=108)
     entry1.config(textvariable = defaultReg,state='readonly',relief='flat')
     entry1.place(relx = 0.1, rely = 0.5)
     tab4_TextLabel5 = ttk.Label(tab, text= "Here you can write your regular language for timestamp")
     tab4_TextLabel5.place(relx = 0.1, rely = 0.6)
     textVar=tk.StringVar()
     entry2=tk.Entry(tab,
           width=108,
           textvariable = textVar,
           relief='flat')
     entry2.place(relx = 0.1, rely = 0.7)
     intVar=tk.IntVar()
     entry3=tk.Entry(tab,
           width=2,
           textvariable = intVar,
           relief='flat')
     entry3.place(relx = 0.7, rely = 0.3)
     tab4_TextLabel6 = ttk.Label(tab, text= "seconds")
     tab4_TextLabel6.place(relx = 0.73, rely = 0.3)
     #defaultReg.set("((?P<DD>\d{1,2})/(?P<MM>\d{1,2})/(?P<YY>\d{4}) (?P<h>\d{1,2}):(?P<min>\d{2}):(?P<sec>\d{2}) (?P<TT>[AM|PM]{2}))")
     #confirm button
     btn1 = ttk.Button(tab, text ='Confirm', command = lambda:confirm()) 
     btn1.place(relx = 0.8, rely = 0.9)
     
     
     def confirm():
           #check spilt option
           if(v.get()=="1"):#split by timestamp
                 reg=''
                 if(entry2.get()!=''):
                       reg=entry2.get()
                       
                 else:
                       reg='%Y-%m-%d %H:%M:%S.%f'
                 print(reg)
                 #split by which time difference
                 typ=v2.get()
                 import launchGUI
                 from utils.spliting import splitingTime
                 seconds=entry3.get()
                 splitingTime(launchGUI.d, launchGUI.pSetups, reg, typ, seconds)
                 launchGUI.iB.timestampReg=str(reg)
                 
#                 
           else:#split by inidividual
                 import launchGUI
                 from utils.spliting import individualSpliting
                 individualSpliting(launchGUI.d, launchGUI.pSetups)
                 #return
def setupTab4(tab):
     # Label for information
     tab3_TextLabel1 = ttk.Label(tab, text= "How to deal with missing value")
     tab3_TextLabel1.place(relx = 0.1, rely = 0.2)
     
     
     choices=["remove the data with missing value","cubic interpolation","linear interpolation","quadratic interpolation"]
     multibox=ttk.Combobox(tab,values=choices
                           ,width=40
                           ,font=12
                           )
     multibox.place(relx = 0.2, rely = 0.3)
     
     launchBtn= ttk.Button(tab, text="launch", command = lambda: cleandataset())
     launchBtn.place(relx = 0.8, rely = 0.3)
#     # Label for information
#     tab3_TextLabel2 = ttk.Label(tab, text= "How long in second do you want for a timeskip(set up for linear interpolation)")
#     tab3_TextLabel2.place(relx = 0.1, rely = 0.4)
#     #
#     Entry=ttk.Entry(tab
#                     ,width=5
#                           )
#     Entry.place(relx = 0.8, rely = 0.4)
     # Label for information
#     tab3_TextLabel3 = ttk.Label(tab, text= "")
#     tab3_TextLabel3.place(relx = 0.1, rely = 0.4)
#     
#     def TextBoxUpdate(event):
#         choice = multibox.get()
#         if(choice=='interpolation'):
#                 
#                 tab3_TextLabel3.config(text='(cubic) interpolation can be helpful dealing the missing value between a small interval of temporal difference')
#                 
#         elif(choice=='remove the data with missing value'): 
#                 
#                 tab3_TextLabel3.config(text='Remove missing value is easy but might lose some information make the trajectory intermittent')
#                 
#     multibox.bind("<<ComboboxSelected>>", TextBoxUpdate)
     def cleandataset():
           choice = multibox.get()
           print(choice)
           
           import launchGUI
           if(choice=='cubic interpolation'):
                 from utils.cleanData import interpolation
                 interpolation(launchGUI.d, launchGUI.pSetups, 'cubic')
           elif(choice=='linear interpolation'):
                 from utils.cleanData import interpolation
                 interpolation(launchGUI.d, launchGUI.pSetups, 'linear')
           elif(choice=='quadratic interpolation'):
                 from utils.cleanData import interpolation
                 interpolation(launchGUI.d, launchGUI.pSetups, 'quadratic')
           elif(choice=='remove the data with missing value'): 
                 from utils.cleanData import removeMissing
                 removeMissing(launchGUI.d, launchGUI.pSetups)
#           ind=choices.index(choice,0,len(choices))
#           print(ind)
#           if(ind==0):#remove value
#                 return
#           elif(ind==1):#linear interpolation
#                 return
#           else:#remove value
#             return
           #print('function finished')
     tab3_TextLabel2 = ttk.Label(tab, text= "Detect outliers with DBSCAN")
     tab3_TextLabel2.place(relx = 0.1, rely = 0.45)
     
     entry=ttk.Entry(tab,textvariable = tk.StringVar(),
                 width=5)
     entry4=ttk.Entry(tab,textvariable = tk.StringVar(),
                 width=5)
     tab3_TextLabel4 = ttk.Label(tab, text= "eps=")
     tab3_TextLabel4.place(relx = 0.2, rely = 0.55)
     tab3_TextLabel8 = ttk.Label(tab, text= "MinPts=")
     tab3_TextLabel8.place(relx = 0.43, rely = 0.55)
     entry.place(
                 relx=0.25,rely=0.55,
                 height=25
                 )
     entry4.place(
                 relx=0.51,rely=0.55,
                 height=25
                 )
     launchBtn= ttk.Button(tab, text="launch", command = lambda: launchDBSCAN())
     launchBtn.place(relx = 0.8, rely = 0.55)
     def launchDBSCAN():
         eps=float(entry.get())
         minPts=float(entry4.get())
         #print(eps)
         from utils.cleanData import Clustering
         import launchGUI
         outliersIndex,outlierLists = Clustering(launchGUI.d, launchGUI.pSetups, eps, minPts)
         launchGUI.iB.outlierLists=outlierLists
         print('The index of the outliers are:')
         print(outliersIndex)
         print('Now you can refresh the 2D distirbution to see where the outliers are located')
     tab3_TextLabel5 = ttk.Label(tab, text= "Detect outliers with ST-DBSCAN")
     tab3_TextLabel5.place(relx = 0.1, rely = 0.65)
     
     entry1=ttk.Entry(tab,textvariable = tk.StringVar(),
                 width=5)
     tab3_TextLabel6 = ttk.Label(tab, text= "sptial threshold =")
     tab3_TextLabel6.place(relx = 0.12, rely = 0.75)
     entry1.place(
                 relx=0.25,rely=0.75,
                 height=25
                 )
     entry2=ttk.Entry(tab,textvariable = tk.StringVar(),
                 width=5)
     tab3_TextLabel7 = ttk.Label(tab, text= "temporal threshold=")
     tab3_TextLabel7.place(relx = 0.35, rely = 0.75)
     entry2.place(
                 relx=0.51,rely=0.75,
                 height=25
                 )
     tab3_TextLabel9 = ttk.Label(tab, text= "MinPts=")
     tab3_TextLabel9.place(relx = 0.61, rely = 0.75)
     entry3=ttk.Entry(tab,textvariable = tk.StringVar(),
                 width=5)
     entry3.place(
                 relx=0.69,rely=0.75,
                 height=25
                 )
     launchBtn= ttk.Button(tab, text="launch", command = lambda: launchSTDBSCAN())
     launchBtn.place(relx = 0.8, rely = 0.75)
     def launchSTDBSCAN():
         eps1=float(entry1.get())
         eps2=float(entry2.get())
         minPts=float(entry3.get())
         from utils.cleanData import STDBSCAN_Clustering
         import launchGUI
         reg=''
         if launchGUI.iB.timestampReg== '':
             reg='%Y-%m-%d %H:%M:%S.%f'
         else: 
             reg =launchGUI.iB.timestampReg
         outliersIndex,outlierLists = STDBSCAN_Clustering(launchGUI.d, launchGUI.pSetups, eps1, eps2, reg, minPts)
         launchGUI.iB.outlierLists=outlierLists
         print('The index of the outliers are:')
         print(outliersIndex)
         print('Now you can refresh the 2D distirbution to see where the outliers are located')
def setupTab5(tab):
     tab5_TextLabel1 = ttk.Label(tab, text= "Which method do you want to sample the dataset")
     tab5_TextLabel1.place(relx = 0.1, rely = 0.2)
     
     choices=["Douglas Peucker Sampling","Average Sampling","TD_TR","TD_SP","SQUISH"]
     multibox=ttk.Combobox(tab,values=choices
                           ,width=40
                           ,font=12
                           )
     multibox.place(relx = 0.2, rely = 0.3)
     
     tab5_TextLabel2 = ttk.Label(tab, text= "Here should be some comments about advantages and disadvantages for each method")
     tab5_TextLabel2.place(relx = 0.1, rely = 0.5)
     strFname=tk.StringVar()
     entry=ttk.Entry(tab,textvariable = strFname,
                 width=5)
     tab5_TextLabel3 = ttk.Label(tab, text= "default")
     tab5_TextLabel4 = ttk.Label(tab, text= "default")
     def TextBoxUpdate(event):
         choice = multibox.get()
         if(choice=='Average Sampling'):
             entry.place_forget()#hid
             tab5_TextLabel3.place_forget()#hid
             tab5_TextLabel4.place_forget()#hid
             tab5_TextLabel2.config(text="it takes for each n point of the trajectory \n"+
                                    "+: Easy, works well for high temporal resolution dataset\n"+
                                          "-: Random, not taking space and time into consideration")
             entry.place(
                 relx=0.53,rely=0.4,
                 height=25
                 )
             tab5_TextLabel3.config(text="I want to sample for each")
             tab5_TextLabel4.config(text="Points")
             tab5_TextLabel3.place(relx=0.3,rely=0.4)
             tab5_TextLabel4.place(relx=0.6,rely=0.4)
         elif(choice == 'Douglas Peucker Sampling'):
             entry.place_forget()#hid
             tab5_TextLabel3.place_forget()#hid
             tab5_TextLabel4.place_forget()#hid
             tab5_TextLabel2.config(text="Douglas Peucker algorithm \n"+
                                    "+: You can adjust the sampling by defining threshold of distance by yourself.\n"+
                                    "-: The proper size of threshold is difficult to find out\n     would not work for straight line")
             entry.place(
                 relx=0.53,rely=0.4,
                 height=25
                 )
             tab5_TextLabel3.config(text="I want to set up the threshold as")
             tab5_TextLabel4.config(text="Meter")
             tab5_TextLabel3.place(relx=0.3,rely=0.4)
             tab5_TextLabel4.place(relx=0.59,rely=0.4)
         elif(choice == 'TD_TR'):
             entry.place_forget()#hid
             tab5_TextLabel3.place_forget()#hid
             tab5_TextLabel4.place_forget()#hid
             tab5_TextLabel2.config(text="Top down_Time Ratio algorithm\n     please make sure of the form of timestamp like YY-MM-DD HH:MM:SS.FF\n"+
                                    "+:It takes the time into consideration.\n"+
                                    "-: The proper size of threshold is difficult to find out\n     would not work for straight line")
             entry.place(
                 relx=0.53,rely=0.4,
                 height=25
                 )
             tab5_TextLabel3.config(text="I want to set up the threshold as")
             tab5_TextLabel4.config(text="Meter")
             tab5_TextLabel3.place(relx=0.3,rely=0.4)
             tab5_TextLabel4.place(relx=0.59,rely=0.4)
         elif(choice == 'TD_SP'):
             entry.place_forget()#hid
             tab5_TextLabel3.place_forget()#hid
             tab5_TextLabel4.place_forget()#hid
             tab5_TextLabel2.config(text="Top down_Speed Based algorithm\n     please make sure of the form of timestamp like YY-MM-DD HH:MM:SS.FF\n"+
                                    "+:It takes the time into consideration.\n"+
                                    "-: The proper size of threshold is difficult to find out\n     would not work for straight line")
             entry.place(
                 relx=0.53,rely=0.4,
                 height=25
                 )
             tab5_TextLabel3.config(text="I want to set up the threshold as")
             tab5_TextLabel4.config(text="Meter pro second")
             tab5_TextLabel3.place(relx=0.3,rely=0.4)
             tab5_TextLabel4.place(relx=0.59,rely=0.4)
         elif(choice == 'SQUISH'):
             entry.place_forget()#hid
             tab5_TextLabel3.place_forget()#hid
             tab5_TextLabel4.place_forget()#hid
             tab5_TextLabel2.config(text="SQUISH algorithm\n     it returns foreach individual an approximated trajectory with user defined size\n"+
                                    "+: It uses Synchronized Euclidean Distance as metric to ensure the trajectory as approximated as possible\n"+
                                    "-: It doesn't take the time into consideration")
             entry.place(
                 relx=0.53,rely=0.4,
                 height=25
                 )
             tab5_TextLabel3.config(text="I want to set up the buffer size as")
             tab5_TextLabel4.config(text="")
             tab5_TextLabel3.place(relx=0.3,rely=0.4)
             tab5_TextLabel4.place(relx=0.59,rely=0.4)
     multibox.bind("<<ComboboxSelected>>", TextBoxUpdate)
     launchBtn= ttk.Button(tab, text="launch", command = lambda: sampling())
     launchBtn.place(relx = 0.8, rely = 0.4)
     def sampling():
         choice = multibox.get()
         import launchGUI
         #calculate run Time
         if(choice=='Average Sampling'):
             n=int(entry.get())
             from utils.sampling import averageSampling
             start = timeit.default_timer()
             averageSampling(launchGUI.d, launchGUI.pSetups, n, launchGUI.iB)
             stop = timeit.default_timer()
             launchGUI.iB.runtime= stop - start
         elif(choice == 'Douglas Peucker Sampling'):
             epsilon=float(entry.get())
             from utils.sampling import Douglas
             start = timeit.default_timer()
             Douglas(launchGUI.d, launchGUI.pSetups, epsilon, launchGUI.iB)
             stop = timeit.default_timer()
             launchGUI.iB.runtime= stop - start
         elif(choice == 'TD_TR'):
             epsilon=float(entry.get())
             from utils.sampling import TD_TR
             start = timeit.default_timer()
             TD_TR(launchGUI.d, launchGUI.pSetups, epsilon, launchGUI.iB)
             stop = timeit.default_timer()
             launchGUI.iB.runtime= stop - start
         elif(choice == 'TD_SP'):
             epsilon=float(entry.get())
             from utils.sampling import TD_SP
             start = timeit.default_timer()
             TD_SP(launchGUI.d, launchGUI.pSetups, epsilon, launchGUI.iB)
             stop = timeit.default_timer()
             launchGUI.iB.runtime= stop - start
         elif(choice == 'SQUISH'):
             epsilon=float(entry.get())
             from utils.sampling import SQUISH
             start = timeit.default_timer()
             SQUISH(launchGUI.d, launchGUI.pSetups, epsilon, launchGUI.iB)
             stop = timeit.default_timer()
             launchGUI.iB.runtime= stop - start
     launchBtn2= ttk.Button(tab, text="PostAnalysis", command = lambda: launchAnalysis())
     launchBtn2.place(relx = 0.8, rely = 0.8)
     def launchAnalysis():
         from utils.DataReport import getPostInfo
         import launchGUI
         getPostInfo(launchGUI.iB)
         
         updateTab6(launchGUI.main.tab6, launchGUI.d, launchGUI.iB)
         launchGUI.main.tabNotebook.select(launchGUI.main.tab6)
# summarize of sampling:
# 1. The Compression ratio
# 2. Average synchronized Euclidean distance
def setupTab6(tab):
    tab6_TextLabel1 = ttk.Label(tab, text= "Summary of Sampling", font='bold')
    tab6_TextLabel1.place(relx = 0.35, rely = 0.05)
    
# Once the sampling is done, Show User the compression ratio, 
# the average of SED 
def updateTab6(tab,d,iB):
      
    #clean tab
    for child in tab.winfo_children():
       child.destroy()
    tab6_TextLabel1 = ttk.Label(tab, text= "Summary of Sampling", font='bold')
    tab6_TextLabel1.place(relx = 0.35, rely = 0.05)
    import launchGUI
    choices=launchGUI.iB.individuals
    #show the information of selected ID
    def showIdInfo(event):
          idName=multibox.get()
          from utils.DataReport import PostAnalysis
          PostAnalysis(idName, launchGUI.d, launchGUI.iB)
          #setup texts:
          compressionratio=str(round(iB.compressionratio,3))+'%'
          tab6_TextLabel21.config(text= compressionratio)
          #tab6_TextLabel21.place(relx = 0.4, rely = 0.35)
          
          runtime=str(round(iB.runtime,3))
          tab6_TextLabel31.config(text= runtime + 'seconds')
          #tab6_TextLabel31.place(relx = 0.4, rely = 0.15)
          
          averageSED=str(iB.averageSED)
          tab6_TextLabel41.config(text= averageSED)
          
          frechetDistance=str(iB.frechetDistance)
          tab6_TextLabel51.config(text= frechetDistance)
          ILD = str(iB.ILD)
          tab6_TextLabel61.config(text= ILD)
          #tab6_TextLabel41.place(relx = 0.4, rely = 0.45)
    tab6_TextLabel3 = ttk.Label(tab, text= "The whole run time of sampling")
    tab6_TextLabel3.place(relx = 0.1, rely = 0.15)
          
    multibox=ttk.Combobox(tab,values=choices
                           ,width=40
                           ,font=12
                           )
     
    multibox.place(relx = 0.4, rely = 0.25)
    multibox.bind("<<ComboboxSelected>>", showIdInfo)
    
    tab6_TextLabel2 = ttk.Label(tab, text= "Compression Ratio")
    tab6_TextLabel2.place(relx = 0.1, rely = 0.35)
    
    
   
    
    
    tab6_TextLabel4 = ttk.Label(tab, text= "Average SED Error")
    tab6_TextLabel4.place(relx = 0.1, rely = 0.45)
    
    tab6_TextLabel5 = ttk.Label(tab, text= "Frechet Distance(Similarity)")
    tab6_TextLabel5.place(relx = 0.1, rely = 0.55)
    
    tab6_TextLabel6 = ttk.Label(tab, text= "Information Loss Degree")
    tab6_TextLabel6.place(relx = 0.1, rely = 0.65)
    #initialize text
    tab6_TextLabel21 = ttk.Label(tab, text= '')
    tab6_TextLabel21.place(relx = 0.4, rely = 0.35)
    tab6_TextLabel31 = ttk.Label(tab, text= '')
    tab6_TextLabel31.place(relx = 0.4, rely = 0.15)
    tab6_TextLabel41 = ttk.Label(tab, text= '')
    tab6_TextLabel41.place(relx = 0.4, rely = 0.45)
    tab6_TextLabel51 = ttk.Label(tab, text= '')
    tab6_TextLabel51.place(relx = 0.4, rely = 0.55)
    tab6_TextLabel61 = ttk.Label(tab, text= '')
    tab6_TextLabel61.place(relx = 0.4, rely = 0.65)
    
#give a short report about the dataset 
#and hint the user which algorithm to use 
def setupTab7(tab):
     #clean tab
    for child in tab.winfo_children():
       child.destroy()
    import launchGUI
    tab7_TextLabel1 = ttk.Label(tab, text= "Data Report", font='bold')
    tab7_TextLabel1.place(relx = 0.35, rely = 0.05)
    tab7_TextLabel2 = ttk.Label(tab, text= "Please select an individual")
    tab7_TextLabel2.place(relx = 0.1, rely = 0.15)
    choices=launchGUI.d.individuals
    multibox=ttk.Combobox(tab,values=choices
                           ,width=40
                           ,font=12
                           )
     
    multibox.place(relx = 0.4, rely = 0.15)
    #############Answer Area###############
    tab7_TextLabel31 = ttk.Label(tab, text='' )
    tab7_TextLabel31.place(relx = 0.4, rely = 0.2)
    tab7_TextLabel41 = ttk.Label(tab, text= '')
    tab7_TextLabel41.place(relx = 0.4, rely = 0.25)
    tab7_TextLabel51 = ttk.Label(tab, text= '')
    tab7_TextLabel51.place(relx = 0.4, rely = 0.3)
    tab7_TextLabel61 = ttk.Label(tab, text= '')
    tab7_TextLabel61.place(relx = 0.4, rely = 0.35)
    tab7_TextLabel71 = ttk.Label(tab, text= '')
    tab7_TextLabel71.place(relx = 0.4, rely = 0.4)
    tab7_TextLabel81 = ttk.Label(tab, text= '')
    tab7_TextLabel81.place(relx = 0.4, rely = 0.45)
    tab7_TextLabel91 = ttk.Label(tab, text= '')
    tab7_TextLabel91.place(relx = 0.4, rely = 0.5)
    tab7_TextLabel101 = ttk.Label(tab, text= '')
    tab7_TextLabel101.place(relx = 0.4, rely = 0.55)
    tab7_TextLabel111 = ttk.Label(tab, text= '')
    tab7_TextLabel111.place(relx = 0.4, rely = 0.6)
    #show the information of selected ID
    def showIdInfo(event):
          idName=multibox.get()
          from utils.DataReport import preAnalysis
          preAnalysis(idName, launchGUI.d, launchGUI.iB)
          #setup texts:
          tab7_TextLabel31.config(text=launchGUI.iB.numOfDatapoints)
          tab7_TextLabel41.config(text= launchGUI.iB.missingvalue)
          tab7_TextLabel51.config(text= launchGUI.iB.missingLat)
          tab7_TextLabel61.config(text= launchGUI.iB.missingLng)
          tab7_TextLabel71.config(text= launchGUI.iB.missingHeight)
          tab7_TextLabel81.config(text= launchGUI.iB.startPos)
          tab7_TextLabel91.config(text= launchGUI.iB.endPos)

          tab7_TextLabel101.config(text= launchGUI.iB.startTime)
          tab7_TextLabel111.config(text= launchGUI.iB.endTime)
    multibox.bind("<<ComboboxSelected>>", showIdInfo)
    tab7_TextLabel3 = ttk.Label(tab, text= "The number of datapoints: ")
    tab7_TextLabel3.place(relx = 0.1, rely = 0.2)
    tab7_TextLabel4 = ttk.Label(tab, text= "The number of missing values: ")
    tab7_TextLabel4.place(relx = 0.1, rely = 0.25)
    tab7_TextLabel401 = ttk.Label(tab, text= "Missing values in latitude: ")
    tab7_TextLabel401.place(relx = 0.1, rely = 0.3)
    tab7_TextLabel402 = ttk.Label(tab, text= "Missing values in longitude: ")
    tab7_TextLabel402.place(relx = 0.1, rely = 0.35)
    tab7_TextLabel403 = ttk.Label(tab, text= "Missing values in height: ")
    tab7_TextLabel403.place(relx = 0.1, rely = 0.4)
    
    tab7_TextLabel5 = ttk.Label(tab, text= "Start Coordinate: ")
    tab7_TextLabel5.place(relx = 0.1, rely = 0.45)
    tab7_TextLabel6 = ttk.Label(tab, text= "End Coordinate: ")
    tab7_TextLabel6.place(relx = 0.1, rely = 0.5)
    
    tab7_TextLabel7 = ttk.Label(tab, text= "Start TimeStamp: ")
    tab7_TextLabel7.place(relx = 0.1, rely = 0.55)
    tab7_TextLabel8 = ttk.Label(tab, text= "End TimeStamp: ")
    tab7_TextLabel8.place(relx = 0.1, rely = 0.6)
    
    def showDistibution():
        
        updateTab8(launchGUI.main.tab8)
        launchGUI.main.tabNotebook.select(launchGUI.main.tab8)
    def showTimelineOverlap():
        updateTab9(launchGUI.main.tab9)
        launchGUI.main.tabNotebook.select(launchGUI.main.tab9)
        
    #show Distribution
    btn1 = ttk.Button(tab, text ='Show Distibution', command = lambda:showDistibution()) 
    btn1.place(relx = 0.8, rely = 0.85)
    #show Timeline
    btn2 = ttk.Button(tab, text ='Show Timeline', command = lambda:showTimelineOverlap()) 
    btn2.place(relx = 0.6, rely = 0.85)
# A very general plot of distribution of the individuals using lat, lng
# Using Matplotlib package
def updateTab8(tab):
    #clean tab
    for child in tab.winfo_children():
       child.destroy()
    #import numpy as np
    from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
    #from matplotlib.backend_bases import key_press_handler
    from matplotlib.figure import Figure
    import launchGUI
    from utils.Distribution import plotHorizontal,plotDensity,plotDensity3D
    #import matplotlib.patches as mpatch
    
    fig = Figure(figsize=(5, 4))
    
    main_plot=fig.add_subplot(111)
    main_plot.set_title('Horizontal Distribution of Individuals')
    main_plot.set_xlabel('longitude')
    main_plot.set_ylabel('latitude')
    
    plotDensity(main_plot, launchGUI.iB, launchGUI.d)

    canvas = FigureCanvasTkAgg(fig, master=tab)  # A tk.DrawingArea.
    canvas.draw()
    #setup position
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
def updateTab9(tab):
    
    #clean tab
    for child in tab.winfo_children():
       child.destroy()
    #import numpy as np
    from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
    #from matplotlib.backend_bases import key_press_handler
    from matplotlib.figure import Figure
    import launchGUI
#    import matplotlib.dates as mdates
#    import pandas as pd
#    import matplotlib.pyplot as plt
#    from datetime import datetime
    from utils.Distribution import plotTimeline
    fig = Figure(figsize=(5, 4))

    main_plot=fig.add_subplot(111)
    main_plot.set_title('Timeline Distribution of Individuals')
    main_plot.set_xlabel('Timeline')
    main_plot.set_ylabel('Indiviudal')
    reg=''
    if launchGUI.iB.timestampReg== '':
             reg='%Y-%m-%d %H:%M:%S.%f'
    else: 
             reg =launchGUI.iB.timestampReg
    plotTimeline(fig, main_plot, launchGUI.iB, launchGUI.d, reg)

    canvas = FigureCanvasTkAgg(fig, master=tab)  # A tk.DrawingArea.
    canvas.draw()
    #setup position
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)