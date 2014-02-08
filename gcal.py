#!/usr/bin/env python
"""
"""

from __future__ import print_function
from __future__ import division
#from __future__ import unicode_literals
from __future__ import absolute_import

import pylib.osscripts as oss
try:
  from xml.etree import ElementTree
except ImportError:
  from elementtree import ElementTree
  
import gdata.calendar.data
import gdata.calendar.client
import gdata.acl.data
import atom
import getopt
import sys
import string
import time
import datetime


#-------------------------------------------------------------------------------
def main(argv):
#-------------------------------------------------------------------------------
    """ usage: 
    """
    args, opts = oss.gopt(argv[1:], [], [], main.__doc__ + __doc__)
    
        
    gcal = GoogleCalendar(args[0], args[1])
    
    for cal in gcal.userCalendars():
        print(cal.title.text)
        print(cal.content.src)

    for ce in gcal.getEntries():
        print(ce)
        
    oss.exit(0)
        

#-------------------------------------------------------------------------------
class CalEntry(object):
#-------------------------------------------------------------------------------
    def __init__(self):
        self.cal = ""
        self.title = ""
        self.text = ""
        self.start = None
        self.end = None
        
    def __str__(self):
        return self.cal + " " + self.title + " " + self.text + " " + str(self.start) + " " + str(self.end)


#-------------------------------------------------------------------------------
class GoogleCalendar(object):
#-------------------------------------------------------------------------------
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def __init__(self, email, password):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        object.__init__(self)
        self.client = gdata.calendar.client.CalendarClient(source='Google-Calendar-1.0')
        self.client.ClientLogin(email, password, self.client.source);

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -    
    def userCalendars(self):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        """ Retrieves the list of calendars to which the authenticated user either
        owns or subscribes to. This is the same list as is represented in the
        Google Calendar GUI. Although we are only printing the title of the
        calendar in this case, other information, including the color of the
        calendar, the timezone, and more. See CalendarListEntry for more
        details on available attributes.
        """
    
        feed = self.client.GetAllCalendarsFeed()
        return feed.entry
    
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def getEntries(self, start_date=None, end_date=None):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        if start_date is None:
            start_date = '2014-01-01'
            
        end_date = '2014-02-28'
        
        query = gdata.calendar.client.CalendarEventQuery(start_min=start_date, start_max=end_date)

        l = []
        
        for cal in self.userCalendars():
            user = cal.content.src
            feed = self.client.GetCalendarEventFeed(user, q=query, max_results='999')
            
            for ae in feed.entry:
                ce = CalEntry()
                l.append(ce)

                ce.cal = cal.title.text.encode('ascii', 'ignore')
                ce.title = ae.title.text.encode('ascii', 'ignore')

                a = ae.content.text
                if a:
                    ce.text = a.encode('ascii', 'ignore')

                for w in ae.when:
                    ce.start = cvtDateTime(w.start)
                    ce.end = cvtDateTime(w.end)

        return l
                
          
#-------------------------------------------------------------------------------
def cvtDateTime(s):
#-------------------------------------------------------------------------------
    # 2014-01-15T08:00:00.000-05:00
    try:
        a, b = s.rsplit('-', 1)
        return datetime.datetime.strptime(a, "%Y-%m-%dT%H:%M:%S.%f")
    except ValueError:
        return datetime.datetime.strptime(s, "%Y-%m-%d")


#-------------------------------------------------------------------------------
def DateTime2Str(dt, off=0):
#-------------------------------------------------------------------------------
    # 2014-01-15T08:00:00.000-05:00
    d = dt + datetime.timedelta(off)
    return "%4d-%02d-%02d" % (d.year, d.month, d.day)
    
        
if __name__ == "__main__":
    main(oss.argv)

