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
    
    bail = mp.Value('i', 0);  sync = mp.Value('i', 1)

    sp, rp = mp.Pipe()
    mp.Process(target=MenuThread, args=(bail, sync, sp)).start()

    gc = gcal.GoogleCalendar(args[0], args[1])

    cfg = Config()
    entries = []; calchk = 0;  first = True
    
    while 1:
        if bail.value:
            break

        if rp.poll():
            cfg = rp.recv()

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
            mult = (dur == 0 or dur == 60*60*24)
    
            if not mult and -30 < secs <= 30:
                mp.Process(target=DlgThread, args=('Event', ce)).start()

            else:
                for i in cfg.timechk:
                    ss = i * 60
                    if ss - 60 < secs <= ss:
                        mp.Process(target=DlgThread, args=('Event in %d Minutes' % i, ce)).start()
                        break
                else:
                    if first and ce.start <= dt <= ce.end:
                        mp.Process(target=DlgThread, args=('Event in Progress', ce)).start()
        
        first = False
    
        t = 60 - dt.second
        if t <= 0: t = 60
    
        for i in range(t//5):
            if bail.value or sync.value: break
            time.sleep(5)

    oss.exit(0)
       

#-------------------------------------------------------------------------------
def DlgThread(title, ce):
#-------------------------------------------------------------------------------
    dct = OrderedDict([('_Time', time.ctime()), ('_Calendar', ce.cal), ('_Title',  ce.title), 
        ('_Text', ce.text), ('_Start', str(ce.start)), ('_End', str(ce.end)), ('1', None), ('Sleep (mins)', '1')])

    t = title;  tmins = 0;  geo = None
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
        tmins += mins 

        t = title + '-- Sleep %03.0f mins' % tmins


#-------------------------------------------------------------------------------
class Config(object):
#-------------------------------------------------------------------------------
    def __init__(self):
        self.timechk = {5, 10, 15, 20, 25, 30}


#-------------------------------------------------------------------------------
def MenuThread(bail, sync, sp):
#-------------------------------------------------------------------------------
    m = menu.Menu("Google Calendar Notifier")

    cfg = Config()
    sp.send(cfg)
    
    while 1:
        a = m.run([("Open Google Calendar", 0), ('Sync to Calendar', 2), ('Config', 3), ('Exit', 1)])

        if a == 1:
            bail.value = 1
            break
    
        if a == 0:
            webbrowser.open("https://www.google.com/calendar/render?tab=wc")
    
        elif a == 2:
           sync.value = 1 
           
        elif a == 3:
            dct = OrderedDict()
            for i in (5, 10, 15, 20, 25, 30):
                dct['%d Minute Warning' % i] = i in cfg.timechk

            dlg = menu.Dialog("Config", geo=m.getGeo(True)) 
            a = dlg.run(dct)
            if not a:
                cfg.timechk = {}
                for i in (5, 10, 15, 20, 25, 30):
                    if dct['%d Minute Warning' % i]:
                        cfg.timechk.add(i)
            sp.send(cfg)
                
           
if __name__ == '__main__':
    main(oss.argv)


    
