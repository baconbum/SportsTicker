#!/usr/bin/env python

from configparser import ConfigParser
import time
import datetime, pytz
import RPi.GPIO as GPIO
from SportsTicker.SportsTicker import SportsTicker
from NHLScraper.NHLDailySchedule import NHLDailySchedule

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
	lcdPinBacklight =	int(config.get('lcdPins', 'LCD_BACKLIGHT'))
)

localTimeZone = pytz.timezone(config.get('miscellaneous', 'timezone'))

def mainLoop():
	# Get the NHLDailySchedule object that contains all of the scoring data for the day
	dailySchedule = NHLDailySchedule(datetime.datetime.now(datetime.timezone.utc).astimezone(localTimeZone).date())
	#dailySchedule = NHLDailySchedule(datetime.date(2017, 4, 15))

	# Loop through all games in the day
	for game in dailySchedule.games:
		# Loop through all of the scoring plays in the game
		for index, scoringPlay in enumerate(game.scoringPlays):
			if (not scoringPlay.alreadyDisplayed()):
				if (scoringPlay.withinDisplayGracePeriod()):
					# Output the scoring play information to the SportsTicker
					scoringPlayOutput = game.getScoringPlayOutput(index)

					sportsTicker.displayNotification(lineOne=scoringPlayOutput[0], lineTwo=scoringPlayOutput[1], ledPattern=SportsTicker.LED_PATTERN_AWESOME, ledPatternRepeat=1)
					sportsTicker.displayNotification(lineOne=scoringPlayOutput[2], lineTwo=scoringPlayOutput[3], ledPatternRepeat=0)

					scoringPlay.markAsDisplayed()
				else:
					print("Scoring play {0} is more than {1} minute(s) old, skipping.".format(scoringPlay.eventCode, config.get('miscellaneous', 'displayGraceThreshold')))
			else:
				print("Scoring play {0} has already been displayed, skipping.".format(scoringPlay.eventCode))

	time.sleep(int(config.get('miscellaneous', 'pollingRate')))

try:
	while (True):
		mainLoop()
except (KeyboardInterrupt, SystemExit):
	print("Exiting program")
finally:
	GPIO.cleanup()
