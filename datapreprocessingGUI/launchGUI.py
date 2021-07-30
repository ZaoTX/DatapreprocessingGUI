# -*- coding: utf-8 -*-
"""
Created on Sat Oct  3 14:28:46 2020

@author: heziy
"""

from GUIFramework import MainGUI
from utils.dataset import dataInfo
from utils.processingSetups  import processingSetups
from utils.infoBuffer import infoBuffer
import tkinter as tk
from tkinter import ttk



iB=infoBuffer()
pSetups=processingSetups()
d=dataInfo('','',[],[])
main=MainGUI()
main.root.mainloop()
