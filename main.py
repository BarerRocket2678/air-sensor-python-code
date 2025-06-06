#For lines 21 to 51:
    # SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
    # SPDX-License-Identifier: MIT
    # Original Code: https://learn.adafruit.com/pm25-air-quality-sensor/python-and-circuitpython

#For all other lines:
    # Written by Cody Zavodsky
    # Debugging help from ChatGPT
    # Technical AQI info from the US EPA: https://document.airnow.gov/technical-assistance-document-for-the-reporting-of-daily-air-quailty.pdf

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

if os.path.exists('data_dy.json'):
    with open('data_dy.json', 'r') as filedy:
        logdy = json.load(filedy)
else:
    logdy = []


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
    aqi25_mn = []
    aqi100_mn = []

    aqi25_hr = []
    aqi100_hr = []

    aqi25_dy = []
    aqi100_dy = []

    ran_within_second = False
    ran_within_second_hr = False
    ran_within_second_dy = False

    while True:
        now = datetime.datetime.utcnow().replace(microsecond=0)
        
        if now.second == 10 or now.second == 20 or now.second == 30 or now.second == 40 or now.second == 50:
            ran_within_second = False
            ran_within_second_hr = False
            ran_within_second_dy = False
            
            while True:
                try:
                    aqdata = pm25.read()
                    aqi25_mn.append(aqdata["pm25 env"])
                    aqi100_mn.append(aqdata["pm100 env"])
                    break

                except Exception as e:
                    print(e)
                    continue
                 
                time.sleep(1)
        if now.second == 0 and len(aqi25_mn) != 0 and len(aqi100_mn) != 0 and ran_within_second == False:
            try:
                if (len(log) > 120):
                    log.pop(0)

                log.append({
                "time": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "pm25": aqi_pm25(statistics.mode(aqi25_mn)),
                "pm100": aqi_pm100(statistics.mode(aqi100_mn))
                })

                aqi25_hr.append(statistics.mode(aqi25_mn))
                aqi100_hr.append(statistics.mode(aqi100_mn))

                aqi25_dy.append(statistics.mode(aqi25_mn))
                aqi100_dy.append(statistics.mode(aqi100_mn))

                aqi25_mn.clear()
                aqi100_mn.clear()

                with open('data_tmp.json', 'w') as file_tmp:
                    json.dump(log[-120:], file_tmp)
                    file_tmp.flush()
                    os.fsync(file_tmp.fileno())

                os.replace('data_tmp.json', 'data.json')

            except Exception as e:
                print(e)
                continue
            
            else:
                ran_within_second = True


        if now.hour == 0 and now.minute == 0 and now.second == 0 and ran_within_second_dy == False:
            try:
                if (len(logdy) > 48):
                    logdy.pop(0)

                logdy.append({
                "time": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "pm25_dy": aqi_pm25(statistics.mean(aqi25_dy)),
                "pm100_dy": aqi_pm100(statistics.mean(aqi100_dy))
                })

                aqi25_dy.clear()
                aqi100_dy.clear()

                with open('data_dy_tmp.json', 'w') as file_dy_tmp:
                    json.dump(logdy[-48:], file_dy_tmp)
                    file_dy_tmp.flush()
                    os.fsync(file_dy_tmp.fileno())
                
                os.replace('data_dy_tmp.json', 'data_dy.json')

            except Exception as e:
                print(e)
                continue

            else:
                ran_within_second_dy = True

        if now.minute == 0 and now.second == 0 and ran_within_second_hr == False:
            try:
                if (len(loghr) > 48):
                    loghr.pop(0)

                loghr.append({
                "time": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), 
                "pm25_hr": aqi_pm25(statistics.mean(aqi25_hr)), 
                "pm100_hr": aqi_pm100(statistics.mean(aqi100_hr))
                })

                aqi25_hr.clear()
                aqi100_hr.clear()

                with open('data_hr_tmp.json', 'w') as file_hr_tmp:
                    json.dump(loghr[-48:], file_hr_tmp)
                    file_hr_tmp.flush()
                    os.fsync(file_hr_tmp.fileno())
                
                os.replace('data_hr_tmp.json', 'data_hr.json')

            except Exception as e:
                print(e)
                continue

            else:
                ran_within_second_hr = True
            
        time.sleep(0.1)    

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

@app.route('/history_dy', methods=['GET'])
def history_dy():
    try:
        with open('data_dy.json', 'r') as file_dy:
            database_dy = json.load(file_dy)
        return jsonify(database_dy[-28:])
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
