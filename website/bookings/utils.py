from calendar import HTMLCalendar
from datetime import datetime as dtime, date, time
import datetime

# from .utils import EventCalendar
from .models import Event
 
def formaStrDate(str_date):
    return (datetime.datetime.strptime(str_date, '%Y-%m-%d').date())

class EventCalendar(HTMLCalendar):
    def __init__(self, events=None):
        super(EventCalendar, self).__init__()
        self.events = events
 
    def formatday(self, day, weekday, events):
        """
        Return a day as a table cell.
        """
        events_from_day = events.filter(start_day__day=day)
        events_html = "<ul>"
        for event in events_from_day:
            # events_html += event.get_absolute_url() + "<br>"
            href = event.get_absolute_url()
            events_html += "<li><a href='"+ href+"'>" + str(event) + "</a></li><br>"
            # print(events_html)
        events_html += "</ul>"
 
        if day == 0:
            return '<td class="noday">&nbsp;</td>'  # day outside month
        else:
            return '<td class="%s">%d%s</td>' % (self.cssclasses[weekday], day, events_html)
 
    def formatweek(self, theweek, events):
        """
        Return a complete week as a table row.
        """
        s = ''.join(self.formatday(d, wd, events) for (d, wd) in theweek)
        return '<tr>%s</tr>' % s
 
    def formatmonth(self, theyear, themonth, withyear=True):
        """
        Return a formatted month as a table.
        """
 
        events = Event.objects.filter(start_day__month=themonth)
 
        v = []
        a = v.append
        a('<table border="0" cellpadding="0" cellspacing="0" class="month">')
        a('\n')
        a(self.formatmonthname(theyear, themonth, withyear=withyear))
        a('\n')
        a(self.formatweekheader())
        a('\n')
        for week in self.monthdays2calendar(theyear, themonth):
            a(self.formatweek(week, events))
            a('\n')
        a('</table>')
        a('\n')
        return ''.join(v)

def check_availability(fixed_startday, fixed_endday, new_startday, new_endday, inventory):
    availability = True
    # if new_startday == fixed_endday or new_endday == fixed_startday:  # edge case
    #     print("1")
    #     new_starttime = new_starttime.hour*60 + new_starttime.minute
    #     new_endtime = new_endtime.hour*60 + new_endtime.minute
    #     fixed_starttime = fixed_starttime.hour*60 + fixed_starttime.minute
    #     fixed_endtime = fixed_endtime.hour*60 + fixed_endtime.minute

    #     if (new_starttime - fixed_endtime)/60 >= 3.0:
    #         print("1--1")
    #         if inventory == 0:
    #             print("1--1-->1")
    #             availability = False
    #         elif inventory is None:
    #             print("1--1-->2")
    #             availability = True
    #         elif inventory > 0:
    #             availability = True
    #             print("1--1-->3")
    #             inventory -= 1
    #     elif (fixed_starttime - new_endtime)/60 >= 3.0:
    #         print("1--2")
    #         if inventory == 0:
    #             print("1--2-->1")
    #             availability = False
    #         elif inventory is None:
    #             print("1--2-->2")
    #             availability = True
    #         elif inventory > 0:
    #             availability = True
    #             print("1--2-->3")
    #             inventory -= 1
    #     else:
    #         availability = False
    #         print("1--3")
    if (new_startday >= fixed_startday and new_startday <= fixed_endday) or (new_endday >= fixed_startday and new_endday <= fixed_endday):  # innner limits
            # overlap = True
        print("2")
        if inventory == 0:
            print("2--1")
            availability = False
        elif inventory is None:
            print("2--2")
            availability = True
        elif inventory > 0:
            availability = True
            print("2--3")
            inventory -= 1
    elif new_startday <= fixed_startday and new_endday >= fixed_endday:  # outter limits
            # overlap = True
        print("3")
        if inventory == 0:
            availability = False
            print("3--1")
        elif inventory is None:
            availability = True
            print("3--2")
        elif inventory > 0:
            availability = True
            inventory -= 1
            print("3--3")

    return availability