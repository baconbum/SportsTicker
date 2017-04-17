#!/usr/bin/env python3

from configparser import ConfigParser
import datetime, pytz
import sqlite3
from .NHLTeam import NHLTeam
from .NHLScoringPlayPlayer import NHLScoringPlayPlayer

class NHLScoringPlay:
	'Details of a scoring play'

	def __init__(self, scoringPlayData):
		self.team =				NHLTeam(idForDatabase=scoringPlayData["team"]["id"])
		self.timeStamp =		pytz.UTC.localize(datetime.datetime.strptime(scoringPlayData["about"]["dateTime"], "%Y-%m-%dT%H:%M:%SZ"))

		self.homeScore =		scoringPlayData["about"]["goals"]["home"]
		self.awayScore =		scoringPlayData["about"]["goals"]["away"]
		self.period =			scoringPlayData["about"]["period"]
		self.periodOrdinal =	scoringPlayData["about"]["ordinalNum"]
		self.periodTime =		scoringPlayData["about"]["periodTime"]

		self.strength =			scoringPlayData["result"]["strength"]["code"]
		self.event =			scoringPlayData["result"]["event"]
		self.eventCode =		scoringPlayData["result"]["eventCode"]

		self.__parsePlayers(scoringPlayData["players"])

	def __parsePlayers(self, playersData):
		self.assistingPlayers = list()

		for playerData in playersData:
			if (playerData["playerType"] == "Scorer"):
				self.scorer =	NHLScoringPlayPlayer(playerData)
			elif (playerData["playerType"] == "Assist"):
				self.assistingPlayers.append(NHLScoringPlayPlayer(playerData))
			elif (playerData["playerType"] == "Goalie"):
				self.goalie =	NHLScoringPlayPlayer(playerData)

	def isPastMaximumAge(self):
		config = ConfigParser(allow_no_value=True)
		config.read('config.ini')

		currentDateTime = datetime.datetime.now(datetime.timezone.utc)

		if (config.get('miscellaneous', 'maximumGoalAgeForDisplay') == None or
			self.timeStamp > currentDateTime - datetime.timedelta(minutes=int(config.get('miscellaneous', 'maximumGoalAgeForDisplay')))):
			return False
		else:
			return True

	def alreadyDisplayed(self):
		connection =	sqlite3.connect("SportsTicker.db")
		cursor =		connection.cursor()

		try:
			cursor.execute("SELECT ID, EventCode, APITimeStamp, Displayed FROM ScoringPlays WHERE EventCode=? AND Displayed=1", (self.eventCode,))
		except sqlite3.OperationalError:
			print("Error executing ScoringPlays SELECT query in NHLScoringPlay.alreadyDisplayed, exiting method")
			connection.close()
			return

		row = cursor.fetchone()
		connection.close()

		if (row != None):
			return True
		else:
			return False

	def markAsDisplayed(self):
		connection =	sqlite3.connect("SportsTicker.db")
		cursor =		connection.cursor()

		try:
			cursor.execute("INSERT INTO ScoringPlays (EventCode, APITimeStamp, Displayed) VALUES (?, ?, ?)", (self.eventCode, self.timeStamp, 1))
		except sqlite3.OperationalError:
			print("Error inserting record with EventCode {0} into ScoringPlays table".format(self.EventCode))

		connection.commit()
		connection.close()
