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
import winsound as ws

from collections import OrderedDict


PAUSE_COUNT = 5
CHECK_COUNT = 30 


#-------------------------------------------------------------------------------
def main(argv):
#-------------------------------------------------------------------------------
    """ usage: 
    """
    args, opts = oss.gopt(argv[1:], [], [], main.__doc__ + __doc__)
    
    ## setup interface and comms
    sp, rp = mp.Pipe()
    sync = mp.Value('i', 0)
    menu = mp.Process(target=MenuThread, args=(sp, sync))
    menu.start()

    ## connect to cal
    gc = gcal.GoogleCalendar(args[0], args[1])

    calchk = 0;  
    first = True
    cfg = Config()
    
    ## check for entries
    entries = chkCal(gc)
    
    while 1:
        print(time.ctime())
        if not menu.is_alive():
            break

        ## chk config info
        cfg = chkConfig(rp, cfg)
            
        dt = datetime.datetime.now()

        ## check entries for notifications
        for ce in entries:
            td = ce.start - dt
            secs = td.total_seconds()
    
            dur = (ce.end - ce.start).total_seconds()
            mult = (dur != 0 and dur != 60*60*24)
            found = False
            
            if -30 < secs <= 30:
                mp.Process(target=DlgThread, args=('Event', ce, cfg)).start()
                found = True
                
            elif mult:
                for tc in cfg.timechk:
                    ss = tc * 60
                    if ss - 60 < secs <= ss:
                        mp.Process(target=DlgThread, args=('Event in %d Minutes' % tc, ce, cfg)).start()
                        found = True
                        break
            
            ## if first time and not notified, see if event already in progress                
            if first and not found:
                if ce.start <= dt <= ce.end:
                    mp.Process(target=DlgThread, args=('Event in Progress', ce, cfg)).start()
                
        first = False
        
        ## check for new entries
        if calchk == CHECK_COUNT or sync.value:
            entries = chkCal(gc, dt)
            calchk = 0
            sync.value = 0
        else:
            calchk += 1
        
        ## sleep proper amount of time    
        dt = datetime.datetime.now()
        nt = 60 - dt.second
        if nt <= 0: nt = 60
        pc, rs = divmod(nt, PAUSE_COUNT)
        
        try:
            for i in range(pc):
                if not menu.is_alive() or sync.value: 
                    raise EarlyOut('out')
                time.sleep(PAUSE_COUNT)
            time.sleep(rs)
        except EarlyOut:
            pass
        
    oss.exit(0)

class EarlyOut(Exception): pass    


#-------------------------------------------------------------------------------
def chkCal(gc, dt=None):
#-------------------------------------------------------------------------------
    if not dt:
        dt = datetime.datetime.now()

    entries = []        
    print('--------------------------------')
    print("checking cal", time.ctime())
    for ce in gc.getEntries(gcal.DateTime2Str(dt), gcal.DateTime2Str(dt, 1)):
        print(ce)
        entries.append(ce)
    
    return entries
    
    
#-------------------------------------------------------------------------------
def chkConfig(rp, cfg):
#-------------------------------------------------------------------------------
    if rp.poll():
        print('got new cfg')
        return rp.recv()   
    return cfg
    
        
#-------------------------------------------------------------------------------
def DlgThread(title, ce, cfg):
#-------------------------------------------------------------------------------
    dct = OrderedDict([('_Time', time.ctime()), ('_Calendar', ce.cal), ('_Title',  ce.title), 
        ('_Text', ce.text), ('_Start', str(ce.start)), ('_End', str(ce.end)), ('1', None), ('Sleep (mins)', '1')])

    t = title;  tmins = 0;  geo = None
    while 1:
        dlg = menu.Dialog("Event -- %s" % t, geo=geo, ok="Sleep", cancel="Acknowledge")
        ws.PlaySound('SystemHand', ws.SND_ALIAS | ws.SND_ASYNC )
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
        self.timechk = [5, 10, 15, 20, 25, 30]
        self.defaultSleep = '1'

    def __str__(self):
        s = [str(self.timechk)]
        return ' '.join(s)
        
        
#-------------------------------------------------------------------------------
def MenuThread(sp, sync):
#-------------------------------------------------------------------------------
    m = menu.Menu("Google Calendar Notifier")

    cfg = Config()
    sp.send(cfg)
    
    while 1:
        a = m.run([("Open Google Calendar", 1), ('Sync to Calendar', 2), ('Config', 3), ('Exit', 100)])

        if a == 100:
            break
    
        elif a == 1:
            webbrowser.open("https://www.google.com/calendar/render?tab=wc")
    
        elif a == 2:
            sync.value = 1
           
        elif a == 3:
            dct = {
                'Notifications (mins)' : ' '.join([str(s) for s in cfg.timechk]),
                'Default Sleep Setting' : cfg.defaultSleep,
            }

            dlg = menu.Dialog("Config", geo=m.getGeo(True)) 
            a = dlg.run(dct)
            
            if not a:
                try:
                    cfg.timechk = [int(x) for x in dct['Notifications (mins)'].split()]
                    cfg.defaultSleep = dct['Default Sleep Setting']
                    sp.send(cfg)
                except ValueError:
                    print('Error:', dct['Notifications (mins)'])
                
           
if __name__ == '__main__':
    main(oss.argv)


    
