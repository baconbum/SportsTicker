#!/usr/bin/env python

import RPi.GPIO as GPIO

class Button:
	'Class for a Button'

	def __init__(self, pinNumber, action=None):
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(pinNumber, GPIO.IN, pull_up_down=GPIO.PUD_UP)

		self.pinNumber =	pinNumber
		#self.action =		action

	def action(self, channel):
		print ("Button on channel {0} pressed!".format(channel))

	def activate(self):
		GPIO.add_event_detect(self.pinNumber, GPIO.RISING, self.action, 200)

	def deactivate(self):
		GPIO.remove_event_detect(self.pinNumber)
