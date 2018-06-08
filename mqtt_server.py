#!/usr/bin/env python
import PCF8591 as ADC 
import time
import paho.mqtt.client as mqtt
import json

THINGSBOARD_HOST = '0.0.0.0'
ACCESS_TOKEN = 'joystick'


def setup():
	ADC.setup(0x48)					# Setup PCF8591
	global state

def direction():	#get joystick result
	state = ['home', 'up', 'down', 'left', 'right', 'pressed']
	i = 0

	if ADC.read(0) <= 5:
		i = 1		#up
	if ADC.read(0) >= 250:
		i = 2		#down

	if ADC.read(1) >= 250:
		i = 3		#left
	if ADC.read(1) <= 5:
		i = 4		#right

	if ADC.read(2) == 0:
		i = 5		# Button pressed

	if ADC.read(0) - 125 < 15 and ADC.read(0) - 125 > -15	and ADC.read(1) - 125 < 15 and ADC.read(1) - 125 > -15 and ADC.read(2) == 255:
		i = 0
	
	return state[i]

def on_connect(client, userdata, rc, *extra_params):
    print('Connected with result code ' + str(rc))
    client.subscribe('pi/joystick')
    client.publish('pi/joystick', "Connected: "+ direction(), 1)


def on_message(client, userdata, msg):
    data = direction()
	print("msg")
    if data != 'home':
		print("published")
        client.publish('pi/joystick', data, 1)

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