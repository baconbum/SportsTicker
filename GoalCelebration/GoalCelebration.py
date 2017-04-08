#!/usr/bin/env python

import time
import warnings
from multiprocessing import Process
from collections import namedtuple
from .LightEmittingDiode import LightEmittingDiode
from .LiquidCrystalDisplay import LiquidCrystalDisplay

class GoalCelebration():

	# The number of LEDs hooked up
	MAX_LEDs = 4

	PatternSegment = namedtuple('PatternSegment', ['duration', 'lights'])

	ALTERNATING_PATTERN = [
		PatternSegment(duration=0.5,	lights=[0]),
		PatternSegment(duration=0.5,	lights=[1])
	]

	SIMULTANEOUS_PATTERN = [
		PatternSegment(duration=0.5,	lights=[0,1,2,3]),
		PatternSegment(duration=0.25,	lights=[])
	]

	AWESOME_PATTERN = [
		PatternSegment(duration=0.1,	lights=[0]),
		PatternSegment(duration=0.1,	lights=[1]),
		PatternSegment(duration=0.1,	lights=[2]),
		PatternSegment(duration=0.1,	lights=[3]),
		PatternSegment(duration=0.1,	lights=[2]),
		PatternSegment(duration=0.1,	lights=[1]),
		PatternSegment(duration=0.1,	lights=[0]),
		PatternSegment(duration=0.1,	lights=[1]),
		PatternSegment(duration=0.1,	lights=[2]),
		PatternSegment(duration=0.1,	lights=[3]),
		PatternSegment(duration=0.1,	lights=[2]),
		PatternSegment(duration=0.1,	lights=[1]),
		PatternSegment(duration=0.1,	lights=[0]),
		PatternSegment(duration=0.1,	lights=[1]),
		PatternSegment(duration=0.1,	lights=[2]),
		PatternSegment(duration=0.1,	lights=[3]),
		PatternSegment(duration=0.1,	lights=[2]),
		PatternSegment(duration=0.1,	lights=[1]),
		PatternSegment(duration=0.1,	lights=[0]),
		PatternSegment(duration=0.1,	lights=[0,1]),
		PatternSegment(duration=0.1,	lights=[0,1,2]),
		PatternSegment(duration=0.1,	lights=[0,1,2,3]),
		PatternSegment(duration=0.1,	lights=[1,2,3]),
		PatternSegment(duration=0.1,	lights=[2,3]),
		PatternSegment(duration=0.1,	lights=[3]),
		PatternSegment(duration=0.1,	lights=[2,3]),
		PatternSegment(duration=0.1,	lights=[1,2,3]),
		PatternSegment(duration=0.1,	lights=[0,1,2,3]),
		PatternSegment(duration=0.1,	lights=[0,1,2]),
		PatternSegment(duration=0.1,	lights=[0,1]),
		PatternSegment(duration=0.1,	lights=[0]),
		PatternSegment(duration=0.1,	lights=[0,1]),
		PatternSegment(duration=0.1,	lights=[0,1,2]),
		PatternSegment(duration=0.1,	lights=[0,1,2,3]),
		PatternSegment(duration=0.1,	lights=[1,2,3]),
		PatternSegment(duration=0.1,	lights=[2,3]),
		PatternSegment(duration=0.1,	lights=[3]),
		PatternSegment(duration=0.1,	lights=[2,3]),
		PatternSegment(duration=0.1,	lights=[1,2,3]),
		PatternSegment(duration=0.1,	lights=[0,1,2,3]),
		PatternSegment(duration=0.1,	lights=[0,1,2]),
		PatternSegment(duration=0.1,	lights=[0,1]),
		PatternSegment(duration=0.1,	lights=[0]),
		PatternSegment(duration=0.1,	lights=[0,1]),
		PatternSegment(duration=0.1,	lights=[0,1,2]),
		PatternSegment(duration=0.1,	lights=[0,1,2,3]),
		PatternSegment(duration=0.1,	lights=[1,2,3]),
		PatternSegment(duration=0.1,	lights=[2,3]),
		PatternSegment(duration=0.1,	lights=[3]),
		PatternSegment(duration=0.1,	lights=[2,3]),
		PatternSegment(duration=0.1,	lights=[1,2,3]),
		PatternSegment(duration=0.1,	lights=[0,1,2,3]),
		PatternSegment(duration=0.1,	lights=[0,1,2]),
		PatternSegment(duration=0.1,	lights=[0,1]),
		PatternSegment(duration=0.1,	lights=[0]),
		PatternSegment(duration=0.2,	lights=[]),
		PatternSegment(duration=0.4,	lights=[0,1,2,3]),
		PatternSegment(duration=0.2,	lights=[]),
		PatternSegment(duration=0.4,	lights=[0,1,2,3]),
		PatternSegment(duration=0.2,	lights=[]),
		PatternSegment(duration=0.4,	lights=[0,1,2,3]),
		PatternSegment(duration=0.2,	lights=[])
	]

	def __init__(self, ledPinNumbers, ledPattern, lcdPinRS, lcdPinRW, lcdPinE, lcdPinData, lcdPinBacklight = None):

		self.pattern = ledPattern
		self.ledCollection = []

		# If there are more than MAX_LEDs given in the pinNumbers list, trim the list
		if (len(ledPinNumbers) > self.MAX_LEDs):
			warnings.warn("The maximum number of LEDs is currently set to %d, and %d were specified. Trimming list." % (self.MAX_LEDs, len(pinNumbers)), Warning)
			ledPinNumbers = ledPinNumbers[0:self.MAX_LEDs]

		for pinNumber in ledPinNumbers:
			self.ledCollection.append(LightEmittingDiode(pinNumber))

		self.lcd = LiquidCrystalDisplay(pin_rs=lcdPinRS, pin_rw=lcdPinRW, pin_e=lcdPinE, pins_data=lcdPinData, pin_backlight=lcdPinBacklight)

	def playCelebration(self, repeat=3):

		lcdCelebrationArgs = {
			"lineOne": "TOR Goal: #43 N. Kadri (32)",
			"lineTwo": "Assisted by: #12 C. Brown (10)"
		}

		ledCelebrationArgs = {
			"repeat": repeat
		}

		p1 = Process(target = self.lcdCelebration, kwargs = lcdCelebrationArgs)
		p1.start()
		p2 = Process(target = self.ledCelebration, kwargs = ledCelebrationArgs)
		p2.start()

		p1.join()
		p2.join()

	def lcdCelebration(self, lineOne, lineTwo=None):
		self.lcd.displayScrollingText(lineOne, lineTwo)

	def ledCelebration(self, repeat):
		# Ensure all LEDs are off to start
		self.toggleAllLEDs(False)

		for i in range(repeat):
			# Loop through the pattern segments
			for patternSegment in self.pattern:
				# Loop through the LED pin mappings
				for light in patternSegment.lights:
					# Ensure the index is valid
					if (light >= 0 and light < len(self.ledCollection)):
						self.ledCollection[light].toggleState(True)
					else:
						warnings.warn("Index %d out of range, ignoring light." % light, Warning)

				# Output the status to the console
				self.printLEDStatus()

				# Wait for the specified amount of time
				time.sleep(patternSegment.duration)

				# Turn off all LEDs before the next pattern segment
				self.toggleAllLEDs(False)

	def toggleAllLEDs(self, state):
		for led in self.ledCollection:
			led.toggleState(state)

	def printLEDStatus(self):
		for led in self.ledCollection:
			led.printStatus()
