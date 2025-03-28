# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
Example sketch to connect to PM2.5 sensor with either I2C or UART.
"""

# pylint: disable=unused-import
from adafruit_pm25.uart import PM25_UART
import serial
import time
import board
import busio
from digitalio import DigitalInOut, Direction, Pull
from adafruit_pm25.i2c import PM25_I2C
from flask import Flask, render_template, jsonify
import threading
import datetime
import json
import os
import statistics

reset_pin = None
# If you have a GPIO, its not a bad idea to connect it to the RESET pin
# reset_pin = DigitalInOut(board.G0)
# reset_pin.direction = Direction.OUTPUT
# reset_pin.value = False


# For use with a computer running Windows:
# import serial
# uart = serial.Serial("COM30", baudrate=9600, timeout=1)

# For use with microcontroller board:
# (Connect the sensor TX pin to the board/computer RX pin)
# uart = busio.UART(board.TX, board.RX, baudrate=9600)

# For use with Raspberry Pi/Linux:
uart = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=0.25)

# For use with USB-to-serial cable:
# import serial
# uart = serial.Serial("/dev/ttyUSB0", baudrate=9600, timeout=0.25)

# Connect to a PM2.5 sensor over UART
pm25 = PM25_UART(uart, reset_pin)

# Create library object, use 'slow' 100KHz frequency!
# i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)
# Connect to a PM2.5 sensor over I2C
# pm25 = PM25_I2C(i2c, reset_pin)

print("Found PM2.5 sensor, reading data...")

app = Flask(__name__)

if os.path.exists('data.json'):
    with open('data.json', 'r') as file:
        log = json.load(file)
else:
    log = []

if os.path.exists('data_hr.json'):
    with open('data_hr.json', 'r') as filehr:
        loghr = json.load(filehr)
else:
    loghr = []



time.sleep(3)
aqdata = pm25.read()


def aqi_pm100(pm):
    pm = round(pm)

    if (pm <= 54):
        return (round((50.0 - 0.0)/(54 - 0.0) * (pm - 0.0) + 0.0))

    elif (pm >= 55 and pm <= 154):
        return (round((100.0 - 51.0)/(154.0 - 55.0) * (pm - 55.0) + 51.0))

    elif (pm >= 155 and pm <= 254):
        return (round((150.0 - 101.0)/(254.0 - 155.0) * (pm - 155.0) + 101.0))

    elif (pm >= 255 and pm <= 354):
        return (round((200.0 - 151.0)/(354.0 - 255.0) * (pm - 255.0) + 151.0))

    elif (pm >= 355 and pm <= 424):
        return (round((201.0 - 300.0)/(424.0 - 355.0) * (pm - 355.0) + 300.0))

    else:
        return (round((500.0 - 301.0)/(604.0 - 425.0) * (pm - 425.0) + 301.0))


def aqi_pm25(pm):
    pm = round(pm, 1)

    if (pm <= 9.0):
        return (round((50.0 - 0.0)/(9.0 - 0.0) * (pm - 0.0) + 0.0))

    elif (pm >= 9.1 and pm <= 35.4):
        return (round((100.0 - 51.0)/(35.4 - 9.1) * (pm - 9.1) + 51.0))

    elif (pm >= 35.5 and pm <= 55.4):
        return (round((150.0 - 101.0)/(55.4 - 35.5) * (pm - 35.5) + 101.0))

    elif (pm >= 55.5 and pm <= 125.4):
        return (round((200.0 - 151.0)/(125.4 - 55.5) * (pm - 55.5) + 151.0))

    elif (pm >= 125.5 and pm <= 225.4):
        return (round((300.0 - 201.0)/(225.4 - 125.5) * (pm - 125.5) + 201.0))

    else:
        return (round((500.0 - 301.0)/(325.4 - 225.5) * (pm - 225.5) + 301.0))

data_lock = threading.Lock()

def get_data():
    while True:
        aqi25_hr = []
        aqi100_hr = []


        for y in range(60):
            aqi25_tmp = []
            aqi100_tmp = []

            for x in range(6):
                try:
                    time.sleep(10)
                    aqdata = pm25.read()
                    aqi25_tmp.append(aqdata["pm25 env"])
                    aqi100_tmp.append(aqdata["pm100 env"])
                except Exception as e:
                    print(e)
                    continue
            try:
                    
                    while True:
                        if datetime.datetime.now().second == 0:
                            break
                        time.sleep(0.01)

                    log.append({                                                          
                    "time": datetime.datetime.now().astimezone().isoformat(),    
                    "pm25": aqi_pm25(statistics.median(aqi25_tmp)),                                                      
                    "pm100": aqi_pm100(statistics.median(aqi100_tmp))  
                    })
                    
                    aqi25_hr.append(statistics.median(aqi25_tmp))
                    aqi100_hr.append(statistics.median(aqi100_tmp))


                    with open('data_tmp.json', 'w') as file_tmp:
                        json.dump(log[-120:], file_tmp)
                        file_tmp.flush()
                        os.fsync(file_tmp.fileno())

                    os.replace('data_tmp.json', 'data.json')

            except Exception as e:
                print(e)
                continue
        
        try:
            loghr.append({
            "time": datetime.datetime.now().astimezone().isoformat(), 
            "pm25_hr": aqi_pm25(statistics.mean(aqi25_hr)), 
            "pm100_hr": aqi_pm100(statistics.mean(aqi100_hr))
            })

            with open('data_hr_tmp.json', 'w') as file_hr_tmp:
                json.dump(loghr[-48:], file_hr_tmp)
                file_hr_tmp.flush()
                os.fsync(file_hr_tmp.fileno())
            
            os.replace('data_hr_tmp.json', 'data_hr.json')

        except Exception as e:
            print(e)
            continue
            


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/notes')
def notes():
    return render_template('notes.html')

@app.route('/history', methods=['GET'])
def history():
    try:
        with open('data.json', 'r') as file:
            database = json.load(file)
        return jsonify(database[-60:])
    except FileNotFoundError:
        return jsonify([])

@app.route('/history_hr', methods=['GET'])
def history_hr():
    try:
        with open('data_hr.json', 'r') as file_hr:
            database_hr = json.load(file_hr)
        return jsonify(database_hr[-24:])
    except FileNotFoundError:
        return jsonify([])


if (data_lock.acquire(blocking=False)):
    try:
        sensor_thread = threading.Thread(target=get_data)
        sensor_thread.daemon = True
        sensor_thread.start()
    finally:
        data_lock.release()
else:
        print("Thread already running!")

app.run(host='0.0.0.0', port=5000, debug=False)
"""
while True:
    time.sleep(1)

    try:
        aqdata = pm25.read()
        # print(aqdata)
    except RuntimeError:
        print("Unable to read from sensor, retrying...")
        continue

    print()
    print("Concentration Units (standard)")
    print("---------------------------------------")
    print(
        "PM 1.0: %d\tPM2.5: %d\tPM10: %d"
        % (aqdata["pm10 standard"], aqdata["pm25 standard"], aqdata["pm100 standard"])
    )
    print("Concentration Units (environmental)")
    print("---------------------------------------")
    print(
        "PM 1.0: %d\tPM2.5: %d\tPM10: %d"
        % (aqdata["pm10 env"], aqdata["pm25 env"], aqdata["pm100 env"])
    )
    print("---------------------------------------")
    print("Particles > 0.3um / 0.1L air:", aqdata["particles 03um"])
    print("Particles > 0.5um / 0.1L air:", aqdata["particles 05um"])
    print("Particles > 1.0um / 0.1L air:", aqdata["particles 10um"])
    print("Particles > 2.5um / 0.1L air:", aqdata["particles 25um"])
    print("Particles > 5.0um / 0.1L air:", aqdata["particles 50um"])
    print("Particles > 10 um / 0.1L air:", aqdata["particles 100um"])
    print("---------------------------------------")
"""
