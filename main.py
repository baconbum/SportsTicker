#!/usr/bin/env python

from configparser import ConfigParser
import time
import RPi.GPIO as GPIO
from SportsTicker.SportsTicker import SportsTicker

config = ConfigParser(allow_no_value=True)
config.read('config.ini')

# Create the SportsTicker object to control the LEDs and LCD
sportsTicker = SportsTicker(
	ledPinNumbers = [
		int(config.get('ledPins', 'LED_ONE')),
		int(config.get('ledPins', 'LED_TWO')),
		int(config.get('ledPins', 'LED_THREE')),
		int(config.get('ledPins', 'LED_FOUR'))
	],
	lcdPinRS =		int(config.get('lcdPins', 'LCD_RS')),
	lcdPinRW =		int(config.get('lcdPins', 'LCD_RW')) if config.get('lcdPins', 'LCD_RW') != None else None,
	lcdPinE =		int(config.get('lcdPins', 'LCD_E')),
	lcdPinData = [
		int(config.get('lcdPins', 'LCD_DATA_ONE')),
		int(config.get('lcdPins', 'LCD_DATA_TWO')),
		int(config.get('lcdPins', 'LCD_DATA_THREE')),
		int(config.get('lcdPins', 'LCD_DATA_FOUR'))
	],
	lcdPinBacklight =			int(config.get('lcdPins', 'LCD_BACKLIGHT')),
	nhlScheduleButtonPin =		int(config.get('dailySchedulePins', 'NHL_DAILY_SCHEDULE_PIN'))
)

try:
	while (True):
		sportsTicker.displayAllLiveScoringPlays()

		time.sleep(int(config.get('miscellaneous', 'apiPollingRate')))

except (KeyboardInterrupt, SystemExit):
	print("Exiting program")
finally:
	GPIO.cleanup()
