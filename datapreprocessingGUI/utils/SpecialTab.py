# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 20:06:17 2020

@author: ZiyaoHe
"""

import tkinter as tk
from tkinter import ttk
#this class extend the Tab of ttk package
class Tab6(ttk.Frame):
    def __init__(self):
        self.tab6_TextLabel1 = ttk.Label(self, text= "Summary of Sampling", font='bold')
        self.tab6_TextLabel1.place(relx = 0.35, rely = 0.05)
        self.tab6_TextLabel2 = ttk.Label(self, text= "Compression Ratio")
        self.tab6_TextLabel2.place(relx = 0.1, rely = 0.15)
        self.tab6_TextLabel21 = ttk.Label(self, text='' )
        self.tab6_TextLabel21.place(relx = 0.4, rely = 0.15)