#!/usr/bin/env python

from configparser import ConfigParser
import time
import datetime, pytz
import warnings
from multiprocessing import Process
from collections import namedtuple
from .LightEmittingDiode import LightEmittingDiode
from .LiquidCrystalDisplay import LiquidCrystalDisplay
from .Button import Button
from NHLScraper.NHLDailySchedule import NHLDailySchedule

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

	def __init__(self, ledPinNumbers, lcdPinRS, lcdPinRW, lcdPinE, lcdPinData, lcdPinBacklight, nhlScheduleButtonPin):

		config = ConfigParser(allow_no_value=True)
		config.read('config.ini')

		self.ledCollection = list()

		for pinNumber in ledPinNumbers:
			self.ledCollection.append(LightEmittingDiode(pinNumber))

		self.lcd = LiquidCrystalDisplay(pin_rs=lcdPinRS, pin_rw=lcdPinRW, pin_e=lcdPinE, pins_data=lcdPinData, pin_backlight=lcdPinBacklight)

		self.nhlScheduleButton = Button(nhlScheduleButtonPin, self.displayDailyNHLSchedule)

		self.enableLiveScoringUpdates = True

		self.localTimeZone =	pytz.timezone(config.get('miscellaneous', 'timezone'))
		self.scheduleDate =		None

		self.updateScheduleDate()

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

	def displayAllLiveScoringPlays(self):
		if self.enableLiveScoringUpdates:
			self.deactivateAllScheduleButtons()

			self.displayLiveNHLScoringPlays()

			self.activateAllScheduleButtons()
		else:
			print ("Skipping live scoring updates for this cycle.")

	def displayLiveNHLScoringPlays(self):
		config = ConfigParser(allow_no_value=True)
		config.read('config.ini')

		self.updateScheduleDate()

		# Get the NHLDailySchedule object that contains all of the scoring data for the day
		nhlDailySchedule = NHLDailySchedule(self.scheduleDate.date())

		# Loop through all games in the day
		for game in nhlDailySchedule.games:
			# Loop through all of the scoring plays in the game
			for index, scoringPlay in enumerate(game.scoringPlays):
				# Ensure scoring play should be displayed
				if (not scoringPlay.alreadyDisplayed()):
					if (not scoringPlay.isPastMaximumAge()):
						# Output the scoring play information to the SportsTicker
						scoringPlayOutput = game.getScoringPlayOutput(index)

						self.displayNotification(lineOne=scoringPlayOutput[0], lineTwo=scoringPlayOutput[1], ledPattern=SportsTicker.LED_PATTERN_AWESOME, ledPatternRepeat=1)
						self.displayNotification(lineOne=scoringPlayOutput[2], lineTwo=scoringPlayOutput[3], ledPatternRepeat=0)

						scoringPlay.markAsDisplayed()
					else:
						print("Scoring play {0} is more than {1} minute(s) old, skipping.".format(scoringPlay.eventCode, config.get('miscellaneous', 'maximumGoalAgeForDisplay')))
				else:
					print("Scoring play {0} has already been displayed, skipping.".format(scoringPlay.eventCode))

	def displayDailyNHLSchedule(self, *kwargs):
		self.deactivateAllScheduleButtons()

		self.enableLiveScoringUpdates = False

		self.updateScheduleDate()

		# Get the NHLDailySchedule object that contains all of the scoring data for the day
		nhlDailySchedule = NHLDailySchedule(self.scheduleDate.date())

		# Loop through all games in the day
		for game in nhlDailySchedule.games:
			gameStatusOutput = game.getGameStatusOutput()

			self.displayNotification(lineOne=gameStatusOutput[0], lineTwo=gameStatusOutput[1], ledPatternRepeat=0)

		self.enableLiveScoringUpdates = True

		self.activateAllScheduleButtons()

	def updateScheduleDate(self):
		config = ConfigParser(allow_no_value=True)
		config.read('config.ini')

		self.scheduleDate = datetime.datetime.now(datetime.timezone.utc).astimezone(self.localTimeZone)
		#self.scheduleDate = datetime.datetime(2017, 4, 15, 23, 59, 59) #Testing date only
		self.scheduleDate = self.scheduleDate - datetime.timedelta(hours=int(config.get('miscellaneous', 'dateRolloverOffset')))

	def deactivateAllScheduleButtons(self):
		self.nhlScheduleButton.deactivate()

	def activateAllScheduleButtons(self):
		self.nhlScheduleButton.activate()
