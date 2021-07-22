# -*- coding: utf-8 -*-
"""
Created on Wed Oct  7 23:07:58 2020

@author: heziy
"""

# Importing Tkinter module 
import  tkinter as tk
import tkinter.ttk  as ttk
  
# Creating master Tkinter window 
master = tk.Tk() 
master.geometry("175x175") 
  
# Tkinter string variable 
# able to store any string value 
v = tk.StringVar(master, "1") 
  
# Dictionary to create multiple buttons 
values = {"RadioButton 1" : "1", 
          "RadioButton 2" : "2", 
          "RadioButton 3" : "3", 
          "RadioButton 4" : "4", 
          "RadioButton 5" : "5"} 
  
# Loop is used to create multiple Radiobuttons 
# rather than creating each button separately 
for (text, value) in values.items(): 
    ttk.Radiobutton(master, text = text, variable = v, 
        value = value).pack(side = tk.TOP, ipady = 5) 
  
# Infinite loop can be terminated by 
# keyboard or mouse interrupt 
# or by any predefined function (destroy()) 
master.mainloop() 