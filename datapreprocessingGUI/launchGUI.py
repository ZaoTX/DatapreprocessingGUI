# -*- coding: utf-8 -*-
"""
Created on Sat Oct  3 14:28:46 2020

@author: heziy
"""

from GUIFramework import MainGUI
from utils.dataset import dataInfo
from utils.processingSetups  import processingSetups
from utils.infoBuffer import infoBuffer


import os
import sys
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)


iB=infoBuffer()
pSetups=processingSetups()
d=dataInfo('','',[],[])
main=MainGUI()
main.addTab()
main.root.mainloop()
