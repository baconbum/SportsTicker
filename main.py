#!/usr/bin/env python

import RPi.GPIO as GPIO
from GoalCelebration.GoalCelebration import GoalCelebration

# Define the GPIO pins to be used
LED_ONE = 35
LED_TWO = 36
LED_THREE = 37
LED_FOUR = 38

LCD_RS = 11
LCD_RW = None
LCD_E = 12

LCD_DATA_ONE = 13
LCD_DATA_TWO = 15
LCD_DATA_THREE = 16
LCD_DATA_FOUR = 18

LCD_BACKLIGHT = 22

celebration = GoalCelebration(ledPinNumbers=[LED_ONE, LED_TWO, LED_THREE, LED_FOUR], ledPattern=GoalCelebration.AWESOME_PATTERN,
				lcdPinRS=LCD_RS, lcdPinRW=LCD_RW, lcdPinE=LCD_E, lcdPinData=[LCD_DATA_ONE, LCD_DATA_TWO, LCD_DATA_THREE, LCD_DATA_FOUR], lcdPinBacklight=LCD_BACKLIGHT)

celebration.playCelebration(repeat=1)

GPIO.cleanup()
