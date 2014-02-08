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

from multiprocessing import Process, Value
from collections import OrderedDict


#-------------------------------------------------------------------------------
def main(argv):
#-------------------------------------------------------------------------------
    """ usage: 
    """
    args, opts = oss.gopt(argv[1:], [], [], main.__doc__ + __doc__)
    
    bail = Value('i', 0)
    sync = Value('i', 1)
    p = Process(target=MenuThread, args=(bail,sync))
    p.start()

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

	    if -30 < secs <= 30:
                p = Process(target=DlgThread, args=('Event', ce))
		p.start()

	        print("timer went off")
		print(ce)

	    elif 540 < secs <= 600:
                p = Process(target=DlgThread, args=('Event in 10 Minutes', ce))
		p.start()
	        print("timer in 10 mins")

	    elif 1140 < secs <= 1200:
                p = Process(target=DlgThread, args=('Event in 20 Minutes', ce))
		p.start()
	        print("timer in 20 mins")

	    elif 240 < secs <= 300:
                p = Process(target=DlgThread, args=('Event in 5 Minutes', ce))
		p.start()
	        print("timer in 5 mins")

	    elif first:
	        if ce.start <= dt <= ce.end:
                     p = Process(target=DlgThread, args=('Event in Progress', ce))
		     p.start()
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
    dct = OrderedDict([('Time', time.ctime()), ('Calendar', ce.cal), ('Title',  ce.title), ('Text', ce.text), ('Start', str(ce.start)), ('End', str(ce.end))])

    t = title
    i = 0
    while 1:
        dlg = menu.Dialog("Event -- %s" % t, ok="Sleep 1 Min", cancel="Acknowledge")
        a = dlg.run(dct)
	if not a:
	    break

	time.sleep(60)
	i += 1
	t = title + '-- Sleep %d mins' % i


#-------------------------------------------------------------------------------
def MenuThread(bail, sync):
#-------------------------------------------------------------------------------
    m = menu.Menu("G Calendar Notifier")
    while 1:
        a = m.run([("Open Google Calendar", 0), ('Sync to Calendar', 2), ('Exit', 1)])

	if a == 1:
	    bail.value = 1
	    break

	if a == 0:
	    webbrowser.open("https://www.google.com/calendar/render?tab=wc")

	elif a == 2:
	   sync.value = 1 
        

if __name__ == '__main__':
    main(oss.argv)


    
