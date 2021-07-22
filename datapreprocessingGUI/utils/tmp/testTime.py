# -*- coding: utf-8 -*-
"""
Created on Sat Oct 10 11:58:07 2020

@author: heziy
"""
#import re
from datetime import datetime
#正则语言
#test_date='2019-10-01 02:00:00.000'
regStr=r"((?P<YY>\d{4})-(?P<MM>\d{1,2})-(?P<DD>\d{1,2}) (?P<h>\d{1,2}):(?P<min>\d{2}):(?P<sec>\d{2}[.]\d{3}))"
#mat = re.match(regStr,test_date)
#print(mat.group('sec'))
#print (type(mat.group(0)))
#import time
#print(time.strptime('30/03/09 16:31:32', '%d/%m/%y %H:%M:%S'))
test='2019-10-01 02:00:00.000'
test1='2019-10-01 03:00:00.000'
date_time_obj=datetime.strptime(test,'%Y-%m-%d %H:%M:%S.%f')
date_time_obj1=datetime.strptime(test1,'%Y-%m-%d %H:%M:%S.%f')
print('Date:', date_time_obj.date())
print('Time:', date_time_obj.time())
print('Date-time:', date_time_obj)
print(abs((date_time_obj-date_time_obj1).total_seconds()))

