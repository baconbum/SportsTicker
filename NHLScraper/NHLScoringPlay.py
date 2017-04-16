#!/usr/bin/env python3

import datetime, pytz
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
