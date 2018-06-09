#!/usr/bin/env python
import sys
sys.path.insert(0,"..//")

import PCF8591 as ADC
import time
import json
import smbus
import math

bus = smbus.SMBus(1)
power_mgmt_1 = 0x6b
address = 0x68
def read_word(adr):
    high = bus.read_byte_data(address, adr)
    low = bus.read_byte_data(address, adr+1)
    val = (high << 8) + low
    return val

def read_word_2c(adr):
    val = read_word(adr)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val

def dist(a,b):
    return math.sqrt((a*a)+(b*b))

def get_y_rotation(x,y,z):
    radians = math.atan2(x, dist(y,z))
    return -math.degrees(radians)

def get_x_rotation(x,y,z):
    radians = math.atan2(y, dist(x,z))
    return math.degrees(radians)
	
def setup():
	ADC.setup(0x48)				
	global state
	address = 0x68 
	bus.write_byte_data(address, power_mgmt_1, 0)

def direction():	#get joystick result
	state = ['home', 'up', 'down', 'left', 'right', 'pressed']
	i = 0

	if ADC.read(0) <= 5:
		i = 1
	if ADC.read(0) >= 250:
		i = 2
	if ADC.read(1) >= 250:
		i = 3
	if ADC.read(1) <= 5:
		i = 4
	if ADC.read(2) == 0:
		i = 5
	if ADC.read(0) - 125 < 15 and ADC.read(0) - 125 > -15	and ADC.read(1) - 125 < 15 and ADC.read(1) - 125 > -15 and ADC.read(2) == 255:
		i = 0

	return state[i]





class Message():
	def __init__(self,topic, data):
		self.topic = topic
		self.data = data
