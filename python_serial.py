import serial
import time
import csv
import matplotlib
#matplotlib.use("tkAgg")
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt
import numpy as np
import json 
import datetime

ser = serial.Serial('COM9')
ser.flushInput()

plot_window = 20
y_var = np.array(np.zeros([plot_window]))
x_var = np.array(np.zeros([plot_window]))

plt.ion()
fig, ax = plt.subplots()
ax.set_title('Time VS Sound')
ax.set_xlabel("Time in Seconds")
ax.set_ylabel("Sound")
line, = ax.plot(y_var, x_var)

start_time = time.time()

while True:
    ser_bytes = ser.readline()
    try:
        decoded_bytes = str(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))
        json_object = json.loads(decoded_bytes)
        print(json_object)
    except:
        continue
    with open("sensors_data.csv","a") as f:
        writer = csv.writer(f,delimiter=",")
        writer.writerow([json_object['id'],json_object['microphone'], json_object['date'], json_object['time']])
    y_var = np.append(y_var,json_object['microphone'])
    x_var = np.append(x_var,time.time()-start_time)
    y_var = y_var[1:plot_window+1]
    x_var = x_var[1:plot_window+1]
    line.set_ydata(y_var)
    line.set_xdata(x_var)
    ax.relim()
    ax.autoscale_view()
    fig.canvas.draw()
    fig.canvas.flush_events()