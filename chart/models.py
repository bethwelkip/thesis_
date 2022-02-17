from time import time
from django.db import models
import datetime
from django.utils import timezone
class Temp(models.Model):
    date = models.DateField(default=timezone.now())
    temp = models.DecimalField(max_digits=4, decimal_places=1)

class CO2(models.Model):
    date = models.DateField(default=timezone.now())
    co2 = models.DecimalField(max_digits=5, decimal_places=1)
class Hum(models.Model):
    date = models.DateField(default=timezone.now())
    hum = models.DecimalField(max_digits=3, decimal_places=1)




