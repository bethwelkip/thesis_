
from django.shortcuts import render
from django.shortcuts import render
# from django.db import models
from django.core import serializers
from .models import Measurements, Sensor #, Temp, CO2, Hum
from django.http import JsonResponse
import datetime, pytz
import csv
import plotly.express as px
from plotly.offline import plot
from plotly.graph_objs import Scatter
import pandas as pd
import requests, json
from decouple import config, Csv
'''

FUTURE CONSIDERATIONS
- have global variables such as time period, specific regions(Frist etc)
- have a class for the sensors
    the user selects whether they want to view all sensors or sensors in specific regions

ANALYSIS OF INPUT FROM MULTIPLE SENSORS
    - Use groupby and then take min max, average per day.
    - maybe take hourly average
'''
def add_to_table(data):
    pass

def get_blynk_data():
    tokens = ["mae_3","mae_4", "mae_5","mae_6", "mae_7","mae_10","mae_11","mae_12","mae_13"]
    df_co =[]
    df_temp =[]
    for token in tokens:
        url = requests.get(f'https://blynk.cloud/external/api/data/get?token={config(token)}&period=MONTH&granularityType=MINUTE&sourceType=AVG&tzName=America/New_York&format=ISO_SIMPLE&sendEvents=true&output=JSON')
        raw_data = []
        if "error" not in json.loads(url.text).keys():
            raw_data = json.loads(url.text)['data']
        if raw_data:
            for dat in raw_data:
                if dat["data_stream_name"] in ["Button",'LCD']:
                    if dat["value"] > 5000:
                        dat["value"] = 999.99
                    df_co.append([dat["ts"], dat["value"], token])
                elif dat["data_stream_name"] ==["Random Value Send",'Pressao de ar comprimido']:
                    df_temp.append([dat["ts"], dat["value"], token])
    df_co = pd.DataFrame(df_co[:])
    df_co.columns = ["Time", "CO2 Concentration", "Sensor"]
    df_temp = pd.DataFrame(df_temp[:])

    return df_co

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



def specific(request, val):
    today, yesterday, two_hour = False, False, False
    if val == 100:
        two_hour = True
    elif val == 110:
        today = True
    elif val == 101:
        yesterday = True
    else:
        pass

    return temperature(request,today, yesterday, two_hour)

def temperature(request, today = False, yesterday = False, two_hour = False):
    data = get_blynk_data()
    print(data.head())
    print("two hour: ", two_hour, "yesterday: ", yesterday, "today: ", today)
    if today:
        raw_data = Measurements.get_today()
    elif two_hour:
        raw_data = Measurements.get_two_hour()
    elif yesterday:
        raw_data = Measurements.get_yesterday()
    else:
        raw_data = Measurements.get_all_time()
    if len(raw_data) == 0:
        message = True
        return render(request, 'graph.html', {'message': message})

    label, gas, temp, hum = [],[],[],[]
    print(len(raw_data))
    j = 0
    for i, dat in enumerate(raw_data[:min(len(raw_data), 100)]):
        lab = pd.to_datetime(dat.date.strftime("%m/%-d/%Y,") +' '+dat.time.strftime("%H:%M:%S"))+ datetime.timedelta(days=j)
        #dat.date + datetime.timedelta(days=j)
        hum.append(float(dat.hum))
        gas.append(float(dat.co2))
        label.append(lab)#""+str(j)+dat.date.strftime("%m/%-d/%Y,")+""+dat.time.strftime("%H:%M:%S"))
        temp.append(float(dat.temp))
        j += 1
    df = pd.DataFrame(gas, index = label)
    h = pd.Series(hum)
    df += pd.Series(hum)
    df['temp'] = pd.Series(temp)
    print("\n\n\n", data[data.Sensor == "mae_3"]["CO2 Concentration"])

    graph_co = plot([Scatter(x = data["Time"], y = data[data.Sensor == "mae_3"]["CO2 Concentration"],
                        mode='lines', name='sensor 3',
                        opacity=0.8), 
                    Scatter(x = data["Time"], y = data[data["Sensor"]=="mae_4"]["CO2 Concentration"],
                        mode='lines', name='sensor 4',
                        opacity=0.8), 
                    Scatter(x = data["Time"], y = data[data["Sensor"]=="mae_5"]["CO2 Concentration"],
                        mode='lines', name='sensor 5',
                        opacity=0.8), 
                    Scatter(x = data["Time"], y = data[data["Sensor"]=="mae_6"]["CO2 Concentration"],
                        mode='lines', name='sensor 6',
                        opacity=0.8)],
               output_type='div')

    graph_2 = plot([Scatter(x = label, y = gas,
                        mode='lines', name='Carbon(IV)Oxide (CO_2)',
                        opacity=0.8, marker_color='green', showlegend = True)],output_type='div')

    
    graph = px.line(x  = label, y = hum)
    # print(graph)
    print(len(gas), len(label))
    return render(request, 'graph.html', {'graph_co': graph_co, 'graph': graph_2, 'label':label,'gas':gas, 'temp':temp, 'hum':hum })

def update(request, co,temp,hum, sensor_id):
    print( co,temp,hum, sensor_id)
    if request.method == "GET":
        print("REQUEST GET:", request.GET)
    loc = Sensor.find_location(int(sensor_id))
    now = datetime.datetime.now().astimezone(pytz.timezone("America/New_York")) #.strftime("%m/%-d/%Y, %H:%M:%S")
    hum = float(int(hum))/100
    temp = float(temp)/100
    co = int(co)
    new_measurement = Measurements(date = now.date(),time = now.time(), co2 = co, hum = hum, temp = temp, loc = loc)
    new_measurement.save()

    return render(request,'graph.html' )
def updater(request):
    print(request)
    if request.method == "POST":
        print("REQUEST GET: ", request.POST)
    print("Here")
    return render(request,'graph.html' )
   

