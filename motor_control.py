#!/usr/bin/env python
import time
import serial
import io
import time
import RPi.GPIO as GPIO
import binascii
import sys

motor = serial.Serial(
        port='/dev/ttyUSB0',
        baudrate = 1200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout= 0.1
)

screen = serial.Serial(
        port='/dev/ttyUSB1',
        baudrate = 1200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout= 0.1
)

#def lop_roead_data1():
#       buffer=""
#       while 1:
#               bytedata=screen.read(1)
#               print bytedata
#               if bytedata == b"\r":
#                       print "Motor Data   : " + repr(buffer)
#                       break
#               else:
#                       buffer+=bytedata

#def lop_roead_data2():
#       buffer=""
#       while 1:
#               bytedata=motor.read(1)
#               print bytedata
#               if bytedata == b"\r":
#                       print "Motor Data   : " + repr(buffer)
#                       break
#               else:
#                       buffer+=bytedata

def destroy():
        motor.close()
        screen.close()
        pass

def loop():
        while 1:
                screendata=screen.readline()
                print  "Screen Data ___  : " + repr(screendata)
                motor.write(screendata)
                screen.flush()
                motordata=motor.readline(43)
                motorval =motordata.split(" ")
	        if "\xf0" in motorval[0]:
                        send = str.replace(motorval[0],"\xf0","\xf1",1)
                        print motorval[0]
                	print  "Motor Data ???? : " + repr(motorval[0])
                        print send
                	screen.write(send)
		else:
			print  "Motor Data ???? : " + repr(motor)
                        send = str.replace(motorval[0],"\xf1","\xf0",1)
                        print send     
                        screen.write(send)
                motor.flush()


if __name__ == '__main__':
        try:
                loop()
        except KeyboardInterrupt:
                destroy()
