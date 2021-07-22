# -*- coding: utf-8 -*-
"""
Created on Thu Sep 24 14:37:00 2020

@author: heziy
"""

import tkinter as tk
from tkinter import ttk


class MainGUI:
     root = tk.Tk()
     tabNotebook = ttk.Notebook(root)
     # Add different tabs
     tab1 = ttk.Frame(tabNotebook)
     tab2 = ttk.Frame(tabNotebook)
     tab3 = ttk.Frame(tabNotebook)
     tab4 = ttk.Frame(tabNotebook)
     tab5 = ttk.Frame(tabNotebook)
     tab6 = ttk.Frame(tabNotebook)
     tab7 = ttk.Frame(tabNotebook)
     tab8 = ttk.Frame(tabNotebook)
     tab9 = ttk.Frame(tabNotebook)
     
     def addTab(self):
           try:
                 from utils.Tabsetups import setupTab1,setupTab2,setupTab3,setupTab4,setupTab5,setupTab6,updateTab9
                 #set up style
                 self.setStyle()
                 
                 #setup tab1:
                 setupTab1(self.tab1)
                 #setup tab2:
                 
                 setupTab2(self.tab2)
                 
                 #setup tab3:
                 setupTab3(self.tab3)
                 #setup tab4:
                 setupTab4(self.tab4)
                 #setup tab5
                 setupTab5(self.tab5)
                 #setup tab6
                 setupTab6(self.tab6)
                 #setup tab7
                 #Tab7 will setup once the user select their datafile and the headers
                 # See utils.Tabsetups updateTab7
                 #Tab8 as well, updated once the preanalysis is triggled
                 #updateTab9(self.tab9)
                 
                 self.tabNotebook.add(self.tab1, text = "Select Dataset")
                 self.tabNotebook.add(self.tab2, text = "Data Filtering")
                 self.tabNotebook.add(self.tab3, text = "Split Dataset")
                 self.tabNotebook.add(self.tab4, text = "Clean Data")
                 self.tabNotebook.add(self.tab5, text = "Sample Dataset")
                 self.tabNotebook.add(self.tab6, text = "Summary")
                 self.tabNotebook.add(self.tab7, text = "Data Report")
                 self.tabNotebook.add(self.tab8, text = "Distribution")
                 self.tabNotebook.add(self.tab9, text = "Timeline")
                 
                 self.tabNotebook.pack(fill ="both"
                                       ,expand=1
                                       ,padx=10, pady=10
                                       )
           except:
                 pass
               
     def setStyle(self):
           style= ttk.Style()
           style.theme_use('clam')
     
     def __init__(self):
           self.root.title("Movement Data Preprocessing")
           self.root.geometry("800x600")
           self.addTab()
           #self.root.mainloop()
#mainGui=MainGUI() 
         

           
          