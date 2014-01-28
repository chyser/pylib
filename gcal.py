#!/usr/bin/env python
"""
"""

from __future__ import print_function
from __future__ import division
from __future__ import unicode_literals
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


#-------------------------------------------------------------------------------
def main(argv):
#-------------------------------------------------------------------------------
    """ usage: 
    """
    args, opts = oss.gopt(argv[1:], [], [], main.__doc__ + __doc__)
    
        
    gcal = GoogleCalendar('chrish6141960@gmail.com', 'sariboodo2')
    
    for i in gcal.userCalendars():
        print(i.title.text)

    gcal.getEntries()
        
    oss.exit(0)
        
    

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
    def getEntries(self):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        start_date = '2014-01-01'
        end_date = '2014-01-31'
        
        query = gdata.calendar.client.CalendarEventQuery(start_min=start_date, start_max=end_date)
        feed = self.client.GetCalendarEventFeed(q=query)
        
        for ae in feed.entry:
            print('\t%s' % ae.title.text)

          
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def __str__(self):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        return str(self.__dict__)
        
    
        
if __name__ == "__main__":
    main(oss.argv)

