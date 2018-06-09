#!/usr/bin/env python

import time
import json
import math
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import sys
sys.path.insert(0,"..//")

import PCF8591 as ADC
import smbus

from sensor_utils import *

host = "a2xzgqat4h4es4.iot.us-east-1.amazonaws.com"
rootCAPath = "../IOT_AWS/root-CA.crt"
certificatePath = "../IOT_AWS/RPi-Mountain-Lion.cert.pem"
privateKeyPath = "../IOT_AWS/RPi-Mountain-Lion.private.key"
useWebsocket = True
clientId = "hackbikeserver"
topic = 'pi/#'


def on_message():
	time.sleep(0.1)
	joystick = direction()
	accel_xout = read_word_2c(0x3b)/16384.0
	accel_yout = read_word_2c(0x3d)/16384.0
	accel_zout = read_word_2c(0x3f)/16384.0
	terrain = {'x':get_x_rotation(accel_xout, accel_yout, accel_zout), 'y': get_y_rotation(accel_xout, accel_yout, accel_zout)}

	terrainMsg = Message("pi/terrain",terrain)
	if joystick == 'home' or data == 'pressed':
		joystick = "spam"
	joystickMsg = Message("pi/joystick", joystick)

	return terrainMsg, joystickMsg	

# Init AWSIoTMQTTClient
client = None
if useWebsocket:
    client = AWSIoTMQTTClient(clientId, useWebsocket=True)
    client.configureEndpoint(host, 443)
    client.configureCredentials(rootCAPath)
else:
    client = AWSIoTMQTTClient(clientId)
    client.configureEndpoint(host, 8883)
    client.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

# AWSIoTMQTTClient connection configuration
client.configureAutoReconnectBackoffTime(1, 32, 20)
client.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
client.configureDrainingFrequency(2)  # Draining: 2 Hz
client.configureConnectDisconnectTimeout(10)  # 10 sec
client.configureMQTTOperationTimeout(5)  # 5 sec

# Connect and subscribe to AWS IoT
client.connect()
# Note that we are not putting a message callback here. We are using the general message notification callback.
client.subscribeAsync(topic, 1)
time.sleep(2)


if __name__ == '__main__':		
	setup()
	while True:
		e1, e2 = on_message()
		client.publishAsync(e1.topic,round(time.time()) + ": "+ e1.data, 1)
		client.publishAsync(e2.topic, round(time.time()) + ": "+ e2.data, 1)
		time.sleep(0.5)
