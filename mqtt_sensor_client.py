#!/usr/bin/env python
import sys
sys.path.insert(0,"..//")

import PCF8591 as ADC
import time
import paho.mqtt.client as mqtt
import json
import smbus
import math

from sensor_utils import *

THINGSBOARD_HOST = '0.0.0.0'
ACCESS_TOKEN = 'hacknbike'

def on_connect(client, userdata, rc, *extra_params):
	print('Connected with result code ' + str(rc))
	accel_xout = read_word_2c(0x3b)/16384.0
	accel_yout = read_word_2c(0x3d)/16384.0
	accel_zout = read_word_2c(0x3f)/16384.0
        terrain = {'x':get_x_rotation(accel_xout, accel_yout, accel_zout), 'y': get_y_rotation(accel_xout, accel_yout, accel_zout)}
	client.subscribe('pi/#')
	client.publish('pi/joystick', "joystick: "+ direction())
	client.publish('pi/terrain', 'terrain: '+ str(terrain))

def on_message(client, userdata, msg):
        time.sleep(0.1)
	data = direction()
	accel_xout = read_word_2c(0x3b)/16384.0
	accel_yout = read_word_2c(0x3d)/16384.0
	accel_zout = read_word_2c(0x3f)/16384.0
	terrain = {'x':get_x_rotation(accel_xout, accel_yout, accel_zout), 'y': get_y_rotation(accel_xout, accel_yout, accel_zout)}
        client.publish('pi/terrain',str(terrain))
	
	if data == 'home':
        	client.publish('pi/joystick', 'spam')
	elif data == 'pressed':
        	client.publish('pi/joystick', 'spam')
	else:
        	client.publish('pi/joystick', data)
        
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(ACCESS_TOKEN)
client.connect(THINGSBOARD_HOST, 1883, 60)


if __name__ == '__main__':		
	setup()
	try:
		client.loop_forever()
	except KeyboardInterrupt:
		client.loop_stop(force=True)
