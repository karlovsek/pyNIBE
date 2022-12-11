from pyNIBE import pyNIBE
from influxdb import InfluxDBClient
import json
import time

client = InfluxDBClient('localhost', 8086, 'grafana', 'grafana', 'nibe')



iteration = 0
while True:
    # update our readings
    #.refresh()
    my_heater.open()

    # first value of the 'status'-section holds "BT1 Outdoor temperature"
    outdoor_temperature = float(my_heater.readings[0]['status'][0]['value'][0:-2])
    hot_water_charging = float(my_heater.readings[0]['status'][1]['value'][0:-2])
    degree_minutes = int(my_heater.readings[0]['status'][7]['value'][0:-2])

    calculated_flow_temp = float(my_heater.readings[0]['climate system 1'][2]['value'][0:-2])
    room_temperature = float(my_heater.readings[0]['climate system 1'][5]['value'][0:-2])
    
    addition = 0 if my_heater.readings[0]['addition'][0]['value'] == "no" else 10

    defrosting = 0 if my_heater.readings[1]['status'][0]['value'] == "no" else 1

    outdoor_temp_slave = float(my_heater.readings[1]['status'][2]['value'][0:-2])

    current_compr_freq = float(my_heater.readings[1]['compressor module '][16]['value'][0:-2])
    requested_compr_freq = float(my_heater.readings[1]['compressor module '][17]['value'][0:-2])


    # bagging and tagging our data
    my_datapoint = {}
    my_datapoint["measurement"] = "F2120-12"
    my_datapoint["tags"] = {'sensor': 'outdoor'}
    my_datapoint["fields"] = {
    "Avg Outdoor temp": outdoor_temperature,
    "Hot water temp": hot_water_charging,
    "DM": degree_minutes,
    "Calc flow temp": calculated_flow_temp,
    "Room temp" : room_temperature,
    "Addition" : addition,
    "Defrosting" : defrosting,
    "Out temp slave" : outdoor_temp_slave,
    "Current freq" : current_compr_freq,
    "Requested freq" : requested_compr_freq
    }

    # sending our data to influxDB
    # client.write_points([my_datapoint])
    print(my_datapoint)
    client.write_points([my_datapoint])

    # log out, wait for a while and start over
    my_heater.close()
    iteration = iteration + 1
    print("Sleeping for some time ZZzzz ", iteration)
    time.sleep(300)