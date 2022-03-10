from django.contrib import admin
from .models import Measurements, Location, Sensor
# Register your models here.

admin.site.register(Measurements)
admin.site.register(Location)
admin.site.register(Sensor)
''' 
# class RequestDemoAdmin(admin.ModelAdmin):
#     list_display = [field.name for field in Measurements._meta.get_fields()]

'''