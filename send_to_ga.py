#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyga.entities import Visitor, Session, Event
from pyga.requests import Tracker
import sys
import ConfigParser
import StringIO

subject = sys.argv[1]
body = sys.argv[2]

class MyParser(ConfigParser.ConfigParser):
    def as_dict(self):
        d = dict(self._sections)
        for k in d:
            d[k] = dict(self._defaults, **d[k])
            d[k].pop('__name__', None)
        return d

ini_fp = StringIO.StringIO(body)
parse = MyParser()
parse.readfp(ini_fp)
parsed = parse.as_dict()

def convert_time(x):
    x = x.split()
    res = 0
    for i in x:
        if i[-1:] == "m":
            res += int(i[:-1])
        elif i[-1:] == "h":
            res += int(i[:-1]) * 60
        elif i[-1:] == "d":
            res += int(i[:-1]) * 1440

    return res

#with open('zabbix_log', 'w') as the_file:
    #the_file.write(parsed['zabbix_data'])
    #the_file.write(parsed['zabbix_data']['name'])
#    the_file.write('Just test')

our_IDs = ['UA-50813600-1', 'UA-96028720-1']


visitor = Visitor()
session = Session()

for ID in our_IDs:
    tracker = Tracker(ID)
    if subject == "down":
        event = Event(category="MONITORING", action="SERVER_DOWN", label=parsed['zabbix_data']['name'])
        tracker.track_event(event, session, visitor)
    elif subject == "recovery":
        rec_time = parsed['zabbix_data']['duration']
        rec_time = str(convert_time(rec_time))
        event = Event(category="MONITORING", action="SERVER_UP", label=parsed['zabbix_data']['name'], value=rec_time)
        tracker.track_event(event, session, visitor)

