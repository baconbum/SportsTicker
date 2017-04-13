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

dailySchedule = NHLDailySchedule(datetime.datetime.now(datetime.timezone.utc).astimezone(localTimeZone).date())
#dailySchedule = NHLDailySchedule(datetime.date(2017, 4, 9))

celebration = GoalCelebration(ledPinNumbers=[LED_ONE, LED_TWO, LED_THREE, LED_FOUR], ledPattern=GoalCelebration.AWESOME_PATTERN,
				lcdPinRS=LCD_RS, lcdPinRW=LCD_RW, lcdPinE=LCD_E, lcdPinData=[LCD_DATA_ONE, LCD_DATA_TWO, LCD_DATA_THREE, LCD_DATA_FOUR], lcdPinBacklight=LCD_BACKLIGHT)

for game in dailySchedule.games:
	for scoringPlay in game.scoringPlays:
		lineOne = "{0} Goal ({1} {2})".format(scoringPlay.team.abbreviation, scoringPlay.periodTime, scoringPlay.periodOrdinal)
		lineTwo = "{0} {1} @ {2} {3}".format(game.awayTeam.abbreviation, scoringPlay.awayScore, game.homeTeam.abbreviation, scoringPlay.homeScore)

		celebration.playCelebration(lineOne=lineOne, lineTwo=lineTwo, ledPatternRepeat=1)

		lineOne = "{0} ({1})".format(scoringPlay.scorer.fullName, scoringPlay.scorer.seasonTotal)
		if (len(scoringPlay.assistingPlayers) > 0):
			lineTwo = "Assisted by: {0} ({1})".format(scoringPlay.assistingPlayers[0].fullName, scoringPlay.assistingPlayers[0].seasonTotal)
			if (len(scoringPlay.assistingPlayers) > 1):
				lineTwo += ", {0} ({1})".format(scoringPlay.assistingPlayers[1].fullName, scoringPlay.assistingPlayers[1].seasonTotal)
		else:
			lineTwo = "Unassisted"

		celebration.playCelebration(lineOne=lineOne, lineTwo=lineTwo, ledPatternRepeat=0)

GPIO.cleanup()
