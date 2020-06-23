from calendar import HTMLCalendar
from datetime import date
from datetime import datetime as dtime
from datetime import time

from django.conf import settings
from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import render_to_string

from equipments.models import ApiLog

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
            events_html += "<li><a href='" + href + \
                "'>" + str(event) + "</a></li><br>"
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
    if (new_startday >= fixed_startday and new_startday <= fixed_endday) or (new_endday >= fixed_startday and new_endday <= fixed_endday):  # innner limits
        # overlap = True
        # print("2")
        if inventory == 0:
            # print("2--1")
            availability = False
        elif inventory is None:
            # print("2--2")
            availability = True
        elif inventory > 0:
            availability = True
            # print("2--3")
            inventory -= 1
    elif new_startday <= fixed_startday and new_endday >= fixed_endday:  # outter limits
        # overlap = True
        # print("3")
        if inventory == 0:
            availability = False
            # print("3--1")
        elif inventory is None:
            availability = True
            # print("3--2")
        elif inventory > 0:
            availability = True
            inventory -= 1
            # print("3--3")

    return availability


def send_enquiry_mail(request, obj):
    subject, from_email, to = 'ENqiry ALERT!!!', settings.EMAIL_HOST_USER, settings.RECIPIENT_OWNER
    message = render_to_string('bookings/email.html', {
        'customer_name': request.POST['Firstname'] + ' ' + request.POST['Lastname'],
        'phone_num': request.POST['phone_num'],
        'start_date': request.POST['start_date'],
        'end_date': request.POST['end_date'],
        'enquiry': obj
    })
    # print(message)
    send_mail(subject, None, from_email, [to], html_message=message)

# making logs in the Database with make_log_in_db


def make_log_in_db(reference='', response='', log_type='', request={}, status_code=None):
    if status_code and status_code != HTTP_200_OK:
        send_bug_email(make_message_format(
            reference, request, response, status_code))

    try:
        ApiLog.objects.create(log_type=log_type,
                              reference=reference,
                              request=json.dumps(request),
                              response=json.dumps(response),
                              status_code=status_code)
        #print('log created in db')
    except Exception as error:
        print(error)


def send_bug_email(response):
    try:
        subject = 'Production Server Health Notification'
        message = response
        email_from = settings.EMAIL_HOST_USER
        recipient_list = list(settings.RECIPIENT_FOR_BUG)
        if not recipient_list:
            return
        send_mail(subject, message, email_from, recipient_list)
    except Exception as error:
        print(error)

# def get_email_list():
#     try:
#         conf = Configuration.objects.get(entity='downtime_notification')

#         email_list = list()
#         for email in conf.value.split(','):
#             email_list.append(email)
#         return email_list
#     except Exception as error:
#         return []


def make_message_format(reference, request, response, status_code):
    msg = 'Hi,\nSome issue with Server\n\n'
    msg += 'Reference: %s\n\n' % (reference)
    # if url:
    #     msg += 'URL: %s\n\n'%(url)
    msg += 'Request: %s\n\n' % (json.dumps(request))
    msg += 'Response: %s\n\n' % (json.dumps(response))
    if status_code:
        msg += 'Status_code: %i\n\n' % (status_code)

    return msg

# log.make_log_in_db(log_type = 'failure', reference = 'appcore.%s'%(reference), response = {'status' : 'member details api error', 'error' : str(error)}, request = {'policy_no' : policy_no, 'quote_no' : quote_no, "data" : payload})
