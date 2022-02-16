from django.shortcuts import render
from django.shortcuts import render
# from django.db import models
from django.core import serializers
from .models import Measurements
from django.http import JsonResponse
import time
# Create your models here.
# def dashboard(request):
#     return render(request, 'graph.html')

def temperature(request):
    raw_data = [] #Measurements.objects.order_by('time')
    label, gas, temp, hum = [1,2,3],[3,4,7],[5,12,1],[7,8,16]

    for dat in raw_data:
        label.append(dat.time)
        gas.append(dat.co2)
        temp.append(dat.temp)
        hum.append(dat.hum)

    return render(request, 'graph.html', {'label':label,'gas':gas, 'temp':temp, 'hum':hum })

def update(request, co2, temp, hum):
    current_time = time.localtime()
    new_measurement = Measurements(current_time, co2, temp, hum)
    new_measurement.save()
    return render(request,'graph.html' )
   
