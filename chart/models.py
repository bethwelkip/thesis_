# import time
from django.db import models
import datetime, pytz
from django.utils import timezone
class Measurements(models.Model):
    date = models.DateField(default=datetime.datetime.now().astimezone(pytz.timezone("America/New_York")))
    time = models.TimeField(default=datetime.datetime.now().astimezone(pytz.timezone("America/New_York")))
    temp = models.DecimalField(max_digits=4, decimal_places=1)
    co2 = models.DecimalField(max_digits=5, decimal_places=1)
    hum = models.DecimalField(max_digits=3, decimal_places=1)

    @classmethod
    def get_two_hour(cls):
        curr_day = datetime.datetime.today().astimezone(pytz.timezone("America/New_York"))
        curr_time = curr_day - datetime.timedelta(hours=2)
        objects = cls.objects.all()
        print(curr_time.time(), objects[0].time)
        data = [obj for obj in objects if obj.time > curr_time.time() and obj.date == curr_time.date()]
        return  data

    @classmethod
    def get_today(cls):
        curr_day = datetime.datetime.today().astimezone(pytz.timezone("America/New_York"))
        curr_time = curr_day - datetime.timedelta(days=0)
        objects = cls.objects.all()
        data = [obj for obj in objects if obj.date == curr_time.date() ]

    @classmethod
    def get_yesterday(cls):
        curr_day = datetime.datetime.today().astimezone(pytz.timezone("America/New_York"))
        curr_time = curr_day - datetime.timedelta(days=1)
        objects = cls.objects.all()
        data = [obj for obj in objects if obj.date == curr_time.date()]
        return data
    @classmethod
    def get_all_time(cls):
        return cls.objects.all()


