# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 11:03:00 2021

@author: ZiyaoHe
"""

from geopy import distance
import time
newport_ri = (41.49008, -71.312796)
cleveland_oh = (41.499498, -81.695391)
import timeit

start = timeit.default_timer()
d1=distance.distance(newport_ri, cleveland_oh).meters
stop = timeit.default_timer()
print("---Geopy %s seconds ---" % (stop - start))

#newport_ri1 = (41.49008, -71.312796,300)
#cleveland_oh1 = (41.499498, -81.695391,712.5)
#d2=distance.distance(newport_ri1, cleveland_oh1).meters

start = timeit.default_timer()
import math
#d3=math.sqrt(d1**2+412.5**2)
#print('d2 is:' + d2)
#print('d3 is:' + d3)
def d_2points(lat1,lng1,h1,lat2,lng2,h2):
        R = 6378100 #radius of earth
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
        return dis_horizontal
    
d2= d_2points(41.49008, -71.312796,10,41.499498, -81.695391,12)
stop = timeit.default_timer()
print("---Haversine %s seconds ---" %( (stop - start)))
print('d1 is:' + str(d1))
print('d2 is:' + str(d2))

import decimal
a=decimal.Decimal('0.2285714285714285841168345671446461762700762068')
print(1/a)
print((1/a)%10)
