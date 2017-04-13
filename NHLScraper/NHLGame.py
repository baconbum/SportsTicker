#!/usr/bin/env python3

import datetime, pytz
from .NHLScoringPlay import NHLScoringPlay
from .NHLTeam import NHLTeam

class NHLGame:
	'The details of a particular game'

	def __init__(self, gameData):
		self.homeTeam = NHLTeam(teamData=gameData["teams"]["home"]["team"])
		self.awayTeam = NHLTeam(teamData=gameData["teams"]["away"]["team"])
		self.startTime = pytz.UTC.localize(datetime.datetime.strptime(gameData["gameDate"], "%Y-%m-%dT%H:%M:%SZ"))
		self.scoringPlays = self.getScoringPlays(gameData["scoringPlays"])

	def getScoringPlays(self, scoringPlaysData):
		scoringPlays = list()

		for scoringPlayData in scoringPlaysData:
			scoringPlays.append(NHLScoringPlay(scoringPlayData))

		return scoringPlays
