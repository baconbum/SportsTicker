#!/usr/bin/env python3

import time
import RPi.GPIO as GPIO
from RPLCD import CharLCD, BacklightMode

class LiquidCrystalDisplay:
	'Class for a LCD 1602'

	LCD_WIDTH =		16
	LCD_HEIGHT =	2

	def __init__(self, pin_rs, pin_rw, pin_e, pins_data, pin_backlight=None, backlight_enabled=False):

		self.lcd = CharLCD(pin_rs=pin_rs, pin_rw=pin_rw, pin_e=pin_e, pins_data=pins_data, pin_backlight=pin_backlight,
			numbering_mode=GPIO.BOARD,
			cols=self.LCD_WIDTH, rows=self.LCD_HEIGHT, dotsize=8,
			auto_linebreaks=True,
			backlight_enabled=backlight_enabled,
			backlight_mode=BacklightMode.active_high)

	def toggleBacklight(self, state=None):
		if (state == None):
			state = not self.lcd.backlight_enabled

		if (state):
			print("Turning backlight on")
		else:
			print("Turning backlight off")

		self.lcd.backlight_enabled = state

		if (self.lcd.backlight_enabled):
			print("Backlight turned on")
		else:
			print("Backlight turned off")

	def displayText(self, text, duration=5):
		if (text == None):
			print ("Warning (LiquidCrystalDisplay.displayText): Text parameter is empty")
			return

		maxCharacters = self.LCD_WIDTH * self.LCD_HEIGHT

		self.toggleBacklight(True)

		print("Writing " + text + " to LCD")

		if (len(text) > maxCharacters):
			print ("Trimming " + text + " to " + text[:maxCharacters])
			text = text[:maxCharacters]

		self.lcd.write_string(text)
		time.sleep(duration)
		self.lcd.clear()

		self.toggleBacklight(False)

	def displayScrollingText(self, lineOne, lineTwo=None, lineOneDelay=5, lineTwoDelay=2, lineOneResetDelay=2, clearDelay=5, tick=0.2):
		if (lineOne == None):
			print ("Warning (LiquidCrystalDisplay.displayScrollingText): LineOne parameter is empty")
			return

		self.toggleBacklight(True)

		# Determine how many ticks it will take to dislay lineOne
		lineOneTicks = len(lineOne) - self.LCD_WIDTH + 1 if len(lineOne) > 16 else 1

		# Scroll through lineOne, while keeping a maximum of 16 characters of lineTwo stationary (if it's not None)
		for i in range(0, lineOneTicks):
			self.lcd.clear()
			self.writeTextToRow(lineOne[i:i + self.LCD_WIDTH], 0)

			if (lineTwo != None):
				self.writeTextToRow(lineTwo[0:self.LCD_WIDTH], 1)

			time.sleep(lineOneDelay if i == 0 else tick)

		if (lineTwo != None):
			time.sleep(lineOneResetDelay)

			# Determine how many ticks it will take to dislay lineTwo
			lineTwoTicks = len(lineTwo) - self.LCD_WIDTH + 1 if len(lineTwo) > 16 else 1

			# Scroll through lineTwo, while keeping a maximum of 16 characters of lineOne stationary
			for i in range(0, lineTwoTicks):
				self.lcd.clear()
				self.writeTextToRow(lineOne[0:self.LCD_WIDTH],		0)
				self.writeTextToRow(lineTwo[i:i + self.LCD_WIDTH],	1)

				time.sleep(lineTwoDelay if i == 0 else tick)

		time.sleep(clearDelay)
		self.lcd.clear()

		self.toggleBacklight(False)

	def writeTextToRow(self, text, row):
		if (row > self.LCD_HEIGHT - 1):
			print ("Warning (LiquidCrystalDisplay.writeTextToRow): Row parameter is too high")
			return

		print("Writing " + text + " to LCD row " + str(row))

		if (len(text) > self.LCD_WIDTH):
			print ("Trimming " + text + " to " + text[:self.LCD_WIDTH])
			text = text[:self.LCD_WIDTH]

		self.lcd.cursor_pos = (row, 0)
		self.lcd.write_string(text)
