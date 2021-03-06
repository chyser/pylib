import caldav
from caldav.elements import dav, cdav

url = "https://chris.hyser@oracle.com:ATPA29bY@stbeehiveonline.oracle.com/caldav/Oracle/home/chris.hyser@oracle.com/calendars/MyCalendar"

client = caldav.DAVClient(url)
principal = caldav.Principal(client, url)
calendars = principal.calendars()

if len(calendars) > 0:
    calendar = calendars[0]
    print "Using calendar", calendar

    print "Renaming"
    calendar.set_properties([dav.DisplayName("Test calendar"),])
    print calendar.get_properties([dav.DisplayName(),])

    #event = caldav.Event(client, data = vcal, parent = calendar).save()
    #print "Event", event, "created"

    print "Looking for events after 2010-05-01"
    results = calendar.date_search(datetime(2013, 1, 1))
    for event in results:
        print "Found", event

