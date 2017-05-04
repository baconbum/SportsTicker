#!/usr/bin/env python

import RPi.GPIO as GPIO

class Button:
	'Class for a Button'

	def __init__(self, pinNumber, actionOverride=None):
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(pinNumber, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		GPIO.add_event_detect(pinNumber, GPIO.RISING, self.action, 200)

		self.pinNumber =	pinNumber
		self.__enabled =	True

		if (actionOverride != None):
			# Override action method
			self.__action =	actionOverride

	def activate(self):
		self.__enabled =	True

	def deactivate(self):
		self.__enabled =	False

	def action(self, channel):
		if (self.__enabled):
			self.__action(channel)

	def __action(self, channel):
		print ("Button on channel {0} pressed!".format(channel))

	def setAction(self, actionOverride):
		self.__action =	actionOverride
