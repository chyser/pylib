#!/usr/bin/env python
"""
"""

from __future__ import print_function
from __future__ import division
#from __future__ import unicode_literals
from __future__ import absolute_import

import pylib.osscripts as oss
import gcal
import menu
import datetime
  
import time
import datetime
import webbrowser

import multiprocessing as mp

from collections import OrderedDict


#-------------------------------------------------------------------------------
def main(argv):
#-------------------------------------------------------------------------------
    """ usage: 
    """
    args, opts = oss.gopt(argv[1:], [], [], main.__doc__ + __doc__)
    
    bail = mp.Value('i', 0)
    sync = mp.Value('i', 1)
    mp.Process(target=MenuThread, args=(bail, sync)).start()

    gc = gcal.GoogleCalendar(args[0], args[1])

    entries = []

    calchk = 0
    first = True
    while 1:
        if bail.value:
	    break

        dt = datetime.datetime.now()

        if calchk == 30 or sync.value:
            entries = []

	    print('--------------------------------')
	    print("checking cal", time.ctime())
	    for ce in gc.getEntries(gcal.DateTime2Str(dt), gcal.DateTime2Str(dt, 1)):
	        print(ce)
		entries.append(ce)

            calchk = 0
	    sync.value = 0
        else:
	    calchk += 1
        
	for ce in entries:
	    td = ce.start - dt
	    secs = td.total_seconds()

	    dur = (ce.end - ce.start).total_seconds()
	    one = dur == 0 or dur == 60*60*24

	    if -30 < secs <= 30:
                mp.Process(target=DlgThread, args=('Event', ce)).start()
	        print("timer went off")
		print(ce)

	    elif not one and 540 < secs <= 600:
                mp.Process(target=DlgThread, args=('Event in 10 Minutes', ce)).start()
	        print("timer in 10 mins")

	    elif not one and 1140 < secs <= 1200:
                mp.Process(target=DlgThread, args=('Event in 20 Minutes', ce)).start()
	        print("timer in 20 mins")

	    elif not one and 240 < secs <= 300:
                mp.Process(target=DlgThread, args=('Event in 5 Minutes', ce)).start()
	        print("timer in 5 mins")

	    elif first:
	        if ce.start <= dt <= ce.end:
                     mp.Process(target=DlgThread, args=('Event in Progress', ce)).start()


	first = False

        t = 60 - dt.second
	if t <= 0: t = 60

        for i in range(t//2):
	    if bail.value or sync.value: break
	    time.sleep(2)

    oss.exit(0)
       

#-------------------------------------------------------------------------------
def DlgThread(title, ce):
#-------------------------------------------------------------------------------
    dct = OrderedDict([('_Time', time.ctime()), ('_Calendar', ce.cal), ('_Title',  ce.title), 
                       ('_Text', ce.text), ('_Start', str(ce.start)), ('_End', str(ce.end)), ('Sleep (mins)', '1')])

    t = title
    i = 0
    geo = None
    while 1:
        dlg = menu.Dialog("Event -- %s" % t, geo=geo, ok="Sleep", cancel="Acknowledge")
        a = dlg.run(dct)
	if not a:
	    break

        geo = dlg.getGeo()

        try:
	    mins = float(dct['Sleep (mins)'])
	except ValueError:
	    mins = 1

        secs = int(round(60*mins))
	time.sleep(secs)
	i += mins 

	t = title + '-- Sleep %3.0f mins' % i


#-------------------------------------------------------------------------------
def MenuThread(bail, sync):
#-------------------------------------------------------------------------------
    m = menu.Menu("Google Calendar Notifier")
    while 1:
        a = m.run([("Open Google Calendar", 0), ('Sync to Calendar', 2), ('Config', 3), ('Exit', 1)])

	if a == 1:
	    bail.value = 1
	    break

	if a == 0:
	    webbrowser.open("https://www.google.com/calendar/render?tab=wc")

	elif a == 2:
	   sync.value = 1 
        

if __name__ == '__main__':
    main(oss.argv)


    
