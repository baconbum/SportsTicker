#!/usr/bin/env python3

import time
from configparser import ConfigParser
import RPi.GPIO as GPIO
from RPLCD import CharLCD, BacklightMode

class LiquidCrystalDisplay(CharLCD):
	'Class for a LCD.'

	def __init__(self, pin_rs, pin_rw, pin_e, pins_data, pin_backlight=None, backlight_enabled=False):

		config = ConfigParser(allow_no_value=True)
		config.read('config.ini')

		super(LiquidCrystalDisplay, self).__init__(
			pin_rs=				pin_rs,
			pin_rw=				pin_rw,
			pin_e=				pin_e,
			pins_data=			pins_data,
			pin_backlight=		pin_backlight,
			cols=				int(config.get('lcdSize', 'LCD_WIDTH')),
			rows=				int(config.get('lcdSize', 'LCD_HEIGHT')),
			backlight_enabled=	backlight_enabled,
			backlight_mode=		BacklightMode.active_high)

	def toggleBacklight(self, state=None):
		if (state == None):
			state = not self.backlight_enabled

		if (state):
			print("Turning LCD backlight on")
		else:
			print("Turning LCD backlight off")

		self.backlight_enabled = state

	def displayText(self, text, duration=5):
		if (text == None):
			print ("Warning (LiquidCrystalDisplay.displayText): Text parameter is empty")
			return

		maxCharacters = self.lcd.cols * self.lcd.rows

		self.toggleBacklight(True)

		print("Writing " + text + " to LCD")

		if (len(text) > maxCharacters):
			print ("Trimming " + text + " to " + text[:maxCharacters])
			text = text[:maxCharacters]

		self.write_string(text)
		time.sleep(duration)
		self.clear()

		self.toggleBacklight(False)

	def displayScrollingText(self, lineOne, lineTwo=None, lineOneDelay=5, lineTwoDelay=2, lineOneResetDelay=2, clearDelay=5, tick=0.2):
		if (lineOne == None):
			print ("Warning (LiquidCrystalDisplay.displayScrollingText): LineOne parameter is empty")
			return

		self.toggleBacklight(True)

		# Determine how many ticks it will take to dislay lineOne
		lineOneTicks = len(lineOne) - self.lcd.cols + 1 if len(lineOne) > 16 else 1

		# Scroll through lineOne, while keeping a maximum of 16 characters of lineTwo stationary (if it's not None)
		for i in range(0, lineOneTicks):
			self.clear()
			self.writeTextToRow(lineOne[i:i + self.lcd.cols], 0)

			if (lineTwo != None):
				self.writeTextToRow(lineTwo[0:self.lcd.cols], 1)

			time.sleep(lineOneDelay if i == 0 else tick)

		if (lineTwo != None):
			time.sleep(lineOneResetDelay)

			# Determine how many ticks it will take to dislay lineTwo
			lineTwoTicks = len(lineTwo) - self.lcd.cols + 1 if len(lineTwo) > 16 else 1

			# Scroll through lineTwo, while keeping a maximum of 16 characters of lineOne stationary
			for i in range(0, lineTwoTicks):
				self.clear()
				self.writeTextToRow(lineOne[0:self.lcd.cols],		0)
				self.writeTextToRow(lineTwo[i:i + self.lcd.cols],	1)

				time.sleep(lineTwoDelay if i == 0 else tick)

		time.sleep(clearDelay)
		self.clear()

		self.toggleBacklight(False)

	def writeTextToRow(self, text, row):
		if (row > self.lcd.rows - 1):
			print ("Warning (LiquidCrystalDisplay.writeTextToRow): Row parameter is too high")
			return

		print("Writing " + text + " to LCD row " + str(row))

		if (len(text) > self.lcd.cols):
			print ("Trimming " + text + " to " + text[:self.lcd.cols])
			text = text[:self.lcd.cols]

		self.cursor_pos = (row, 0)
		self.write_string(text)
