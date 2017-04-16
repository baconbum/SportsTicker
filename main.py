#!/usr/bin/env python

import datetime, pytz
import RPi.GPIO as GPIO
from GoalCelebration.GoalCelebration import GoalCelebration
from NHLScraper.NHLDailySchedule import NHLDailySchedule

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

localTimeZone = pytz.timezone("Canada/Eastern")

#dailySchedule = NHLDailySchedule(datetime.datetime.now(datetime.timezone.utc).astimezone(localTimeZone).date())
dailySchedule = NHLDailySchedule(datetime.date(2017, 4, 15))

celebration = GoalCelebration(ledPinNumbers=[LED_ONE, LED_TWO, LED_THREE, LED_FOUR], ledPattern=GoalCelebration.AWESOME_PATTERN,
				lcdPinRS=LCD_RS, lcdPinRW=LCD_RW, lcdPinE=LCD_E, lcdPinData=[LCD_DATA_ONE, LCD_DATA_TWO, LCD_DATA_THREE, LCD_DATA_FOUR], lcdPinBacklight=LCD_BACKLIGHT)

for game in dailySchedule.games:
	for index, scoringPlay in enumerate(game.scoringPlays):
		scoringPlayOutput = game.getScoringPlayOutput(index)
		
		celebration.playCelebration(lineOne=scoringPlayOutput[0], lineTwo=scoringPlayOutput[1], ledPatternRepeat=1)
		celebration.playCelebration(lineOne=scoringPlayOutput[2], lineTwo=scoringPlayOutput[3], ledPatternRepeat=0)

GPIO.cleanup()
