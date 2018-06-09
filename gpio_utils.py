import RPi.GPIO as GPIO

ReedPin = 11


def setup():
	GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
	GPIO.setup(ReedPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)    # Set BtnPin's mode is input, and pull up to high level(3.3V)
	GPIO.add_event_detect(ReedPin, GPIO.BOTH, callback=detect, bouncetime=200)

def Print(x):
	if x == 0:
		print '    ***********************************'
		print '    *   Detected Magnetic Material!   *'
		print '    ***********************************'

def detect():
	#Led(GPIO.input(ReedPin))
	var = GPIO.input(ReedPin)
    if var == 0:
        return "contact_made"
    else:
        return "no_contact"


def loop():
	while True:
		pass


if __name__ == '__main__':     # Program start from here
	setup()
	try:
		loop()
	except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
		destroy()