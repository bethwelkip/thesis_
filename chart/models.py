# import time
from django.db import models
import datetime, pytz
from django.utils import timezone
import pandas as pd
class Location(models.Model):
    name = models.CharField(default="Spelman 17", max_length=20)
    num = models.IntegerField(default=0, max_length=2)

class Sensor(models.Model):
    num = models.IntegerField(unique = True)
    location = models.ForeignKey(to=Location,null = True, blank = True, on_delete=callable)

    @classmethod
    def find_location(cls, s_id):
        obj = cls.objects.filter(num = s_id).first()
        return obj.location.name

class Measurements(models.Model):
    date = models.DateField(default=datetime.datetime.now().astimezone(pytz.timezone("America/New_York")))
    time = models.TimeField(default=datetime.datetime.now().astimezone(pytz.timezone("America/New_York")))
    temp = models.DecimalField(max_digits=4, decimal_places=1)
    co2 = models.DecimalField(max_digits=5, decimal_places=1)
    hum = models.DecimalField(max_digits=3, decimal_places=1)
    loc = models.CharField(max_length = 20, null = True, blank = True)

    @classmethod
    def get_two_hour(cls):
        curr_day = datetime.datetime.today().astimezone(pytz.timezone("America/New_York"))
        curr_time = curr_day - datetime.timedelta(hours=2)
        objects = cls.objects.all()
        data = []
        for obj in objects:
            date = pd.to_datetime(obj.date.strftime("%m/%-d/%Y,") +' '+obj.time.strftime("%H:%M:%S"), utc=True).astimezone(pytz.timezone("America/New_York"))
            if date >= curr_time:
                data.append(obj)  

        return data

    @classmethod
    def get_today(cls):
        curr_day = datetime.datetime.today().astimezone(pytz.timezone("America/New_York"))
        curr_time = curr_day - datetime.timedelta(days=0)
        objects = cls.objects.all()
        data = [obj for obj in objects if obj.date == curr_time.date() ]
        return data

    @classmethod
    def get_yesterday(cls):
        curr_day = datetime.datetime.today().astimezone(pytz.timezone("America/New_York"))
        curr_time = curr_day - datetime.timedelta(days=1)
        objects = cls.objects.all()
        data = []# [obj for obj in objects if obj.date == curr_time.date()]
        for obj in objects:
            date = pd.to_datetime(obj.date.strftime("%m/%-d/%Y,") +' '+obj.time.strftime("%H:%M:%S"), utc=True).astimezone(pytz.timezone("America/New_York"))
            if date.date() == curr_time.date():
                data.append(obj)  
        print("--------------------", len(data))      
        return data

    @classmethod
    def get_all_time(cls):
        return list(cls.objects.all())


