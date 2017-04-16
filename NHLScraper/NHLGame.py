#!/usr/bin/env python3

import datetime, pytz
from .NHLScoringPlay import NHLScoringPlay
from .NHLTeam import NHLTeam

class NHLGame:
	'The details of a particular game'

	def __init__(self, gameData):
		self.homeTeam =		NHLTeam(teamData=gameData["teams"]["home"]["team"])
		self.awayTeam =		NHLTeam(teamData=gameData["teams"]["away"]["team"])
		self.startTime =	pytz.UTC.localize(datetime.datetime.strptime(gameData["gameDate"], "%Y-%m-%dT%H:%M:%SZ"))
		self.scoringPlays =	self.getScoringPlays(gameData["scoringPlays"])

	def getScoringPlays(self, scoringPlaysData):
		scoringPlays = list()

		for scoringPlayData in scoringPlaysData:
			scoringPlays.append(NHLScoringPlay(scoringPlayData))

		return scoringPlays

	def getScoringPlayOutput(self, scoringPlayIndex):
		if (scoringPlayIndex < 0 or scoringPlayIndex > len(self.scoringPlays) - 1):
			print("No such index exists in NHLGame.scoringPlays. Error occurred in NHLGame.getScoringPlayOutput")
			return

		scoringPlayOutputLines = list()

		scoringPlay = self.scoringPlays[scoringPlayIndex]

		scoringPlayOutputLines.append("{0}{1} Goal ({2} {3})".format(
			scoringPlay.team.abbreviation,
			" {0}".format(scoringPlay.strength) if scoringPlay.strength in ("PPG", "SHG") else "",
			scoringPlay.periodTime,
			scoringPlay.periodOrdinal))

		scoringPlayOutputLines.append("{0} {1} @ {2} {3}".format(
			self.awayTeam.abbreviation,
			scoringPlay.awayScore,
			self.homeTeam.abbreviation,
			scoringPlay.homeScore))

		scoringPlayOutputLines.append("{0} ({1})".format(
			scoringPlay.scorer.fullName,
			scoringPlay.scorer.seasonTotal))

		if (len(scoringPlay.assistingPlayers) > 0):
			assistOutput = "Assisted by: {0} ({1})".format(scoringPlay.assistingPlayers[0].fullName, scoringPlay.assistingPlayers[0].seasonTotal)
			if (len(scoringPlay.assistingPlayers) > 1):
				assistOutput += ", {0} ({1})".format(scoringPlay.assistingPlayers[1].fullName, scoringPlay.assistingPlayers[1].seasonTotal)

			scoringPlayOutputLines.append(assistOutput)
		else:
			scoringPlayOutputLines.append("Unassisted")

		return scoringPlayOutputLines
