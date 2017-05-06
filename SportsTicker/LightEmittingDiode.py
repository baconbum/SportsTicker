#!/usr/bin/env python

import RPi.GPIO as GPIO

class LightEmittingDiode:
	'Class for a Light Emitting Diode'

	def __init__(self, pinNumber, state = False):
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(pinNumber, GPIO.OUT)

		self.pinNumber = pinNumber
		self.state = state

		self.setVoltage()

	def toggleState(self, state = None):
		if (state != None):
			self.state = state
		else:
			self.state = not self.state

		self.setVoltage()

	def setVoltage(self):
		if (self.state):
			GPIO.output(self.pinNumber, GPIO.HIGH)
		else:
			GPIO.output(self.pinNumber, GPIO.LOW)

	def printStatus(self):
		print("LED pin {0} is set to {1}".format(self.pinNumber, self.state))
