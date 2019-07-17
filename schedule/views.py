from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render
from django.views import generic

from .models import Group, Schedule

import json, requests, datetime, calendar

def get_type_of_week(date):
    type_of_week = date.isocalendar()[1]
    if type_of_week % 2 == 0:
        type_of_week = "неч"
    else:
        type_of_week = "чет"
    return type_of_week

def schedule(group_number, date=None):
    """
    Return list of lists that contain objects for the day
    [!]Doesn't work if class have dates
    :return:
    """
    days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"]
    classes = list()
    if date is None:  # If no date return for the whole week
        for day in days:
            cls = Schedule.objects.filter(group=group_number, weekday=day)
            if cls:
                classes.append(cls)
        return classes
    else:
        weekday = date.weekday()

    type_of_week = date.isocalendar()[1]
    if type_of_week % 2 == 0:
        type_of_week = "неч"
    else:
        type_of_week = "чет"

    cls = Schedule.objects.filter(group=group_number, weekday=days[weekday], date__in=["", type_of_week])
    if cls:
        classes.append(cls)
    return classes

def set_date(option="for a week"):
    """
    Setting correct date
    """
    date = datetime.datetime.today().weekday()
    date = datetime.datetime.today() - datetime.timedelta(days=date)
    if option == "for next week":
        date += datetime.timedelta(days=7)
    return date

def set_everything(date, group_number):
    """
    Final result for a template
    """
    # Start date(Monday)
    days = list()
    for _ in range(6):
        days.append([date.strftime("%d.%m.%y"), schedule(group_number, date)])
        date += datetime.timedelta(days=1)
    return days

# Views
def index(request):
    # Можно объединить первые 3 сравнения
    for action in ["full", "week", "next_week"]:
        if action in request.GET:
            if not request.GET["group_number"]:
                return HttpResponseRedirect("/schedule")
            else:
                return HttpResponseRedirect(redirect_to="%s/%s" % (action, request.GET["group_number"]))
    # if "full" in request.GET:
    #     if not request.GET["group_number"]:
    #         return HttpResponseRedirect(redirect_to="schedule")
    #     return HttpResponseRedirect(redirect_to="full/%s" % request.GET["group_number"])
    # elif "week" in request.GET:
    #     return HttpResponseRedirect(redirect_to="week/%s" % request.GET["group_number"])
    # elif "next_week" in request.GET:
    #     return HttpResponseRedirect(redirect_to="next_week/%s" % request.GET["group_number"])
    if "date" in request.GET:
        # return HttpResponse(request.GET["date"])
        if not request.GET["group_number"] or not request.GET["day"]:
            return HttpResponseRedirect("/schedule")
        group_number = request.GET["group_number"]
        date = request.GET["day"].split("-")
        date = "%s-%s-%s" % (date[2], date[1], date[0])
        return HttpResponseRedirect(redirect_to="%s/%s" % (date, group_number))
    return render(request, "schedule/index.html")

class FullScheduleView(generic.ListView):
    template_name = 'schedule/full_schedule.html'
    context_object_name = 'classes'

    def get_queryset(self):
        return schedule(self.kwargs['group_number'])

def schedule_for_a_week(request, group_number):
    ground_date = datetime.datetime.today().strftime("%d.%m.%y")
    context = {"days": set_everything(set_date(), group_number), "ground_date": ground_date}
    return render(request, "schedule/schedule_for_a_week.html", context)

class ScheduleForNextWeek(generic.ListView):
    template_name = 'schedule/schedule_for_a_week.html'
    context_object_name = 'days'

    def get_queryset(self):
        group_number = self.kwargs['group_number']
        return set_everything(set_date("for next week"), group_number)

def schedule_for_a_day(request, group_number, target_date):
    target_date = target_date.split('-')
    # # Date format: dd-mm-yy
    # day = int(target_date[1])
    # month = int(target_date[0])
    # year = int(target_date[2])

    # Date format: dd-mm-yy
    day = int(target_date[0])
    month = int(target_date[1])
    year = int(target_date[2])
    custom_date = datetime.datetime(year, month, day)

    date = custom_date.weekday()
    date = custom_date - datetime.timedelta(days=date)

    context = {"days": set_everything(date, group_number), "ground_date": custom_date.strftime("%d.%m.%y")}
    return render(request, "schedule/schedule_for_a_week.html", context)

def simple_text(request, group_number, type):
    weekdays = list([weekday.lower() for weekday in calendar.day_abbr[:-1]])
    if type == "today":
        date = datetime.datetime.today()
    elif type == "tomorrow":
        date = datetime.datetime.today() + datetime.timedelta(days=1)
    elif type in weekdays:
        date = datetime.datetime.today().weekday()
        date = datetime.datetime.today() - datetime.timedelta(days=date)
        date += datetime.timedelta(days=weekdays.index(type))
    else:  # Doesn't work
        type = type.split('-')
        day = int(type[0])
        month = int(type[1])
        year = int(type[2])
        date = datetime.datetime(year, month, day)
        # date = type
    context = { "schedule": schedule(group_number, date),
                "date": date.strftime("%d.%m.%y"),
                "type_of_week": get_type_of_week(date)}
    return render(request, "schedule/simple_text.html" ,context)
