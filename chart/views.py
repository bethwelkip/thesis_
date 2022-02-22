
from django.shortcuts import render
from django.shortcuts import render
# from django.db import models
from django.core import serializers
from .models import Measurements #, Temp, CO2, Hum
from django.http import JsonResponse
import datetime
import csv

# def initialize_db():
    
#     file = 'chart/files/feeds.csv'
#     print(file)
#     with open(file, 'r') as file:
#         reader = csv.reader(file)
#         i = 0
#         for r in reader:
#             if r[0] == 'created_at':
#                 continue
#             time, temp, co, hum = r[0], r[2],r[3],r[4]
#             if len(temp) > 0:
#                 t = Temp( temp=temp)
#                 t.save()

#             if len(co) > 0:
#                 c = CO2( co2=co)
#                 c.save()

#             if len(hum) > 0:
#                 h = Hum( hum=hum)
#                 h.save()



def temperature(request, today = False, yesterday = False, two_hour = False):

    if today:
        raw_data = Measurements.get_today()
    elif two_hour:
        raw_data = Measurements.get_all_time()
    elif yesterday:
        raw_data = Measurements.get_all_time()
    else:
        raw_data = Measurements.get_two_hour()


    # raw_data = Measurements.objects.order_by('time')
    # raw_data1 = Temp.objects.order_by('-id')
    # raw_data2 = Hum.objects.order_by('-id')
    label, gas, temp, hum = [],[],[],[]
    # if len(raw_data)== 0:
    #     initialize_db()
    print(len(raw_data))
    for i, dat in enumerate(raw_data[:min(len(raw_data), 100)]):
        lab = dat.date.strftime("%m/%-d/%Y, %H:%M:%S")
        hum.append(float(dat.hum))
        gas.append(float(dat.co2))
        label.append(""+dat.date.strftime("%m/%-d/%Y,")+""+dat.time.strftime("%H:%M:%S"))
        temp.append(float(dat.temp))
    print(len(gas), len(label))
    return render(request, 'graph.html', {'label':label,'gas':gas, 'temp':temp, 'hum':hum })

def update(request, co,temp,hum):
    now = datetime.datetime.now().strftime("%m/%-d/%Y, %H:%M:%S")
    hum = float(hum)/100
    temp = float(temp)/100
    co = int(co)
    new_measurement = Measurements(co2 = co, hum = hum, temp = temp)
    new_measurement.save()

    # co2 = CO2(co2 = co)
    # tem = Temp(date = now, temp=temp)
    # humidity = Hum(date = now, hum=hum)
    # humidity.save()
    # co2.save()
    # tem.save()

    return render(request,'graph.html' )
   
