
from django.shortcuts import render
from django.shortcuts import render
# from django.db import models
from django.core import serializers
from .models import Measurements #, Temp, CO2, Hum
from django.http import JsonResponse
import datetime
import csv
import plotly.express as px
from plotly.offline import plot
from plotly.graph_objs import Scatter
import pandas as pd

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
def generate_csv():
    file = '/Users/bethwelkiplimo/desktop/mae345_2022/feeds.csv'
    print(file)
    data = Measurements.objects.all()

    with open(file,'w') as f:
        options = ["date",'time', 'co2','temp', 'hum']
        for i in range(5):
            f.write(options[i])
            if i != 4:
                f.write('\t')
        f.write('\n')
        for r in data:
            f.write(str(r.date))
            f.write('\t')
            f.write(str(r.time))
            f.write('\t')
            f.write(str(r.co2))
            f.write('\t')
            f.write(str(r.temp))
            f.write('\t')
            f.write(str(r.hum))
            f.write('\n')





def temperature(request, today = False, yesterday = False, two_hour = False):
    # generate_csv()
    if today:
        raw_data = Measurements.get_today()
    elif two_hour:
        raw_data = Measurements.get_all_time()
    elif yesterday:
        raw_data = Measurements.get_yesterday()
    else:
        raw_data = Measurements.get_all_time()

    label, gas, temp, hum = [],[],[],[]
    print(len(raw_data))
    j = 0
    for i, dat in enumerate(raw_data[:min(len(raw_data), 100)]):
        lab = dat.date + datetime.timedelta(days=j)
        # lab = lab.strftime("%m/%-d/%Y, %H:%M:%S")
        hum.append(float(dat.hum))
        gas.append(float(dat.co2))
        label.append(lab)#""+str(j)+dat.date.strftime("%m/%-d/%Y,")+""+dat.time.strftime("%H:%M:%S"))
        temp.append(float(dat.temp))
        j += 1
    df = pd.DataFrame(gas, index = label)
    h = pd.Series(hum)
    df += pd.Series(hum)
    df['temp'] = pd.Series(temp)
    print(df)
    graph_2 = plot([Scatter(x = label, y = hum,
                        mode='lines', name='humidity',
                        opacity=0.8, marker_color='blue'), Scatter(x = label, y = temp,
                        mode='lines', name='temperature',
                        opacity=0.8, marker_color='red')],
               output_type='div')

    graph_co = plot([Scatter(x = label, y = gas,
                        mode='lines', name='Carbon(IV)Oxide (CO_2)',
                        opacity=0.8, marker_color='green', showlegend = True)],output_type='div')

    
    graph = px.line(x  = label, y = hum)
    print(graph)
    print(len(gas), len(label))
    return render(request, 'graph.html', {'graph_co': graph_co, 'graph': graph_2, 'label':label,'gas':gas, 'temp':temp, 'hum':hum })

def update(request, co,temp,hum):
    now = datetime.datetime.now().strftime("%m/%-d/%Y, %H:%M:%S")
    hum = float(hum)/100
    temp = float(temp)/100
    co = int(co)
    new_measurement = Measurements(co2 = co, hum = hum, temp = temp)
    new_measurement.save()

    return render(request,'graph.html' )
   
