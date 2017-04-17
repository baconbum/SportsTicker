#!/usr/bin/env python

import time
import warnings
from multiprocessing import Process
from collections import namedtuple
from .LightEmittingDiode import LightEmittingDiode
from .LiquidCrystalDisplay import LiquidCrystalDisplay

class SportsTicker():

	PatternSegment = namedtuple('PatternSegment', ['duration', 'lights'])

	LED_PATTERN_ALTERNATING = [
		PatternSegment(duration=0.5,	lights=[0]),
		PatternSegment(duration=0.5,	lights=[1])
	]

	LED_PATTERN_SIMULTANEOUS = [
		PatternSegment(duration=0.5,	lights=[0,1,2,3]),
		PatternSegment(duration=0.25,	lights=[])
	]

	LED_PATTERN_AWESOME = [
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

	def __init__(self, ledPinNumbers, lcdPinRS, lcdPinRW, lcdPinE, lcdPinData, lcdPinBacklight = None):

		self.ledCollection = list()

		for pinNumber in ledPinNumbers:
			self.ledCollection.append(LightEmittingDiode(pinNumber))

		self.lcd = LiquidCrystalDisplay(pin_rs=lcdPinRS, pin_rw=lcdPinRW, pin_e=lcdPinE, pins_data=lcdPinData, pin_backlight=lcdPinBacklight)

	def displayNotification(self, lineOne, lineTwo, ledPattern=LED_PATTERN_SIMULTANEOUS, ledPatternRepeat=3):

		lcdNotificationArgs = {
			"lineOne": lineOne,
			"lineTwo": lineTwo
		}

		ledNotificationArgs = {
			"pattern":	ledPattern,
			"repeat":	ledPatternRepeat
		}

		p1 = Process(target = self.lcd.displayScrollingText, kwargs = lcdNotificationArgs)
		p1.start()
		p2 = Process(target = self.ledNotification, kwargs = ledNotificationArgs)
		p2.start()

		p1.join()
		p2.join()

	def ledNotification(self, pattern, repeat):
		# Ensure all LEDs are off to start
		self.toggleAllLEDs(False)

		for i in range(repeat):
			# Loop through the pattern segments
			for patternSegment in pattern:
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
