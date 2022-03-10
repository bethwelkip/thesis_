from django.contrib import admin
from .models import Measurements, Location, Sensor


# Allows access and control of database from the website

admin.site.register(Measurements)
admin.site.register(Location)
admin.site.register(Sensor)
