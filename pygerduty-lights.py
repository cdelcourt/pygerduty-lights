#!/usr/bin/python

#pagerduty_traffic_light - Christophe Delcourt <cd.delcourt@gmail.com>

# Some references to the LED's

# Row 1 Red		= pin 13
# Row 1 Amber		= pin 12
# Row 1 Green		= pin 7

# Row 2 Red		= pin 18
# Row 2 Amber		= pin 16
# Row 2 Green		= pin 15

import pygerduty
import RPi.GPIO as GPIO
import datetime

GPIO.setmode(GPIO.BOARD) #Set the board mode. BCM Pinouts are different, hence BOARD
GPIO.setwarnings(False)

leds = [13, 12, 7, 18, 16, 15] #Set up the GPIO pins to be used

# Your PagerDuty domain and API key below
pager = pygerduty.PagerDuty("acmeorg", "xxxyourpagerdutyapikeyxxx")

red = pager.incidents.count(status='triggered')
yellow = pager.incidents.count(status='acknowledged')

def trafficLight():
	for n in leds: #Reset all LEDs
        	GPIO.setup(n, GPIO.OUT)
	        GPIO.output(n, False)

	if red > 0:  #If something is wrong, light up the red light
		GPIO.output(13,GPIO.HIGH)
		print "PagerDuty Incident: ",pager.incidents.incident_number(status='triggered'), datetime.datetime.now()

	if red > 5:  #If something is *really* wrong, flash the red light to grab my attention!
		GPIO.output(13,GPIO.LOW)
		sleep(0.2)
		GPIO.output(13,GPIO.HIGH)
		sleep(0.2)			
		GPIO.output(13,GPIO.LOW)
		sleep(0.2)
		GPIO.output(13,GPIO.HIGH)

	if yellow > 0:
		GPIO.output(12,GPIO.HIGH)
	
	if all(x == 0 for x in (yellow,red)):
		GPIO.output(7,GPIO.HIGH)

trafficLight()
