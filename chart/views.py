
from django.shortcuts import render
from django.shortcuts import render
# from django.db import models
from django.core import serializers
from .models import Temp, CO2, Hum
from django.http import JsonResponse
import datetime as timer
import csv

def initialize_db():
    
    file = 'chart/files/feeds.csv'
    print(file)
    with open(file, 'r') as file:
        reader = csv.reader(file)
        i = 0
        for r in reader:
            if r[0] == 'created_at':
                continue
            time, temp, co, hum = r[0], r[2],r[3],r[4]
            if len(temp) > 0:
                t = Temp( temp=temp)
                t.save()

            if len(co) > 0:
                c = CO2( co2=co)
                c.save()

            if len(hum) > 0:
                h = Hum( hum=hum)
                h.save()



def temperature(request):

    raw_data = CO2.objects.order_by('id')
    label, gas, temp, hum = [],[],[],[]
    if len(raw_data)== 0:
        initialize_db()
    print(len(raw_data))
    for dat in raw_data[:min(len(raw_data), 100)]:
        # label.append(dat.time)
        # gas.append(dat.co2)
        gas.append(float(dat.co2))
        label.append(dat.id)
        # hum.append(dat.hum)
    print(len(gas), len(label))
    return render(request, 'graph.html', {'label':label,'gas':gas, 'temp':temp, 'hum':hum })

def update(request, co2, temp, hum):
    return render(request,'graph.html' )
   
