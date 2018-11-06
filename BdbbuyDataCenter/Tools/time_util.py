#!/usr/bin/env python
# -*- coding: utf-8 -*
from datetime import datetime,timedelta
import time

def string2timestamp(strValue):
    dateFormat = "%Y-%m-%d %H:%M:%S"
    try:
        d = datetime.strptime(strValue, dateFormat)
        t = d.timetuple()
        timeStamp = int(time.mktime(t))
        timeStamp = float(str(timeStamp) + str("%06d" % d.microsecond)) / 1000000
        return timeStamp
    except ValueError as e:
        d = datetime.datetime.strptime(strValue, dateFormat)
        t = d.timetuple()
        timeStamp = int(time.mktime(t))
        timeStamp = float(str(timeStamp) + str("%06d" % d.microsecond)) / 1000000
        return timeStamp


def datetime_timestamp(dt, type='ms'):
     if isinstance(dt, str):
         try:
             if len(dt) == 10:
                 dt = datetime.strptime(dt.replace('/', '-'), '%Y-%m-%d')
             elif len(dt) == 19:
                 dt = datetime.strptime(dt.replace('/', '-'), '%Y-%m-%d %H:%M:%S')
             else:
                 raise ValueError()
         except ValueError as e:
             raise ValueError(
                 "{0} is not supported datetime format." \
                 "dt Format example: 'yyyy-mm-dd' or yyyy-mm-dd HH:MM:SS".format(dt)
             )

     if isinstance(dt, time.struct_time):
         dt = datetime.strptime(time.stftime('%Y-%m-%d %H:%M:%S', dt), '%Y-%m-%d %H:%M:%S')

     if isinstance(dt, datetime):
         if type == 'ms':
             ts = int(dt.timestamp()) * 1000
         else:
             ts = int(dt.timestamp())
     else:
         raise ValueError(
             "dt type not supported. dt Format example: 'yyyy-mm-dd' or yyyy-mm-dd HH:MM:SS"
         )
     return ts


def timestamp_datetime(ts):
     if isinstance(ts, (int, float, str)):
         try:
             ts = int(ts)
         except ValueError:
             raise

         if len(str(ts)) == 13:
             ts = int(ts / 1000)
         if len(str(ts)) != 10:
             raise ValueError
     else:
         raise ValueError()

     return datetime.fromtimestamp(ts)