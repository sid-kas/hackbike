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
rootCAPath = "/usr/lib/ssl/certs/root-CA.crt"
certificatePath = "/usr/lib/ssl/certs/RPi-Mountain-Lion.cert.pem"
privateKeyPath = "/usr/lib/ssl/certs/RPi-Mountain-Lion.private.key"
useWebsocket = False
clientId = "hackbikeserver"
topic = 'pi/1'

def customOnMessage(message):
    print("Received a new message: ")
    print(message.payload)
    print("from topic: ")
    print(message.topic)
    print("--------------\n\n")

# Suback callback
def customSubackCallback(mid, data):
    print("Received SUBACK packet id: ")
    print(mid)
    print("Granted QoS: ")
    print(data)
    print("++++++++++++++\n\n")


# Puback callback
def customPubackCallback(mid):
    print("Received PUBACK packet id: ")
    print(mid)
    print("++++++++++++++\n\n")

def on_message():
	time.sleep(0.1)
	joystick = direction()
	accel_xout = read_word_2c(0x3b)/16384.0
	accel_yout = read_word_2c(0x3d)/16384.0
	accel_zout = read_word_2c(0x3f)/16384.0
	terrain = {'x':get_x_rotation(accel_xout, accel_yout, accel_zout), 'y': get_y_rotation(accel_xout, accel_yout, accel_zout)}

	terrainMsg = Message("pi/terrain",str(terrain))
	if joystick == 'home' or joystick == 'pressed':
		joystick = "spam"
	joystickMsg = Message("pi/joystick", str(joystick))

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
client.onMessage = customOnMessage
# Connect and subscribe to AWS IoT
client.connect()
# Note that we are not putting a message callback here. We are using the general message notification callback.
client.subscribeAsync(topic, 1, ackCallback=customSubackCallback)
time.sleep(2)


if __name__ == '__main__':		
	setup()
	while True:
		e1, e2 = on_message()
		print("msg sent: ", e1.data, e2.data)
		client.publishAsync(e1.topic, "timestamp:"+str(round(time.time())) + ", "+e1.topic+": " + e1.data, 1)#, ackCallback=customPubackCallback)
		if e2.data != "spam":
			client.publishAsync(e2.topic,"timestamp:"+str(round(time.time())) + ", "+e2.topic+": "  + e2.data, 1)#, ackCallback=customPubackCallback)
		time.sleep(0.8)
