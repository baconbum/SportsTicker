#!/usr/bin/env python3

from configparser import ConfigParser
import datetime, pytz
from .NHLScoringPlay import NHLScoringPlay
from .NHLTeam import NHLTeam

class NHLGame:
	'The details of a particular game'

	def __init__(self, gameData):
		self.homeTeam =		NHLTeam(teamData=gameData["teams"]["home"]["team"])
		self.awayTeam =		NHLTeam(teamData=gameData["teams"]["away"]["team"])

		self.homeScore =	int(gameData["linescore"]["teams"]["home"]["goals"])
		self.awayScore =	int(gameData["linescore"]["teams"]["away"]["goals"])

		self.currentPeriod =				gameData["linescore"]["currentPeriod"]
		self.currentPeriodOrdinal =			gameData["linescore"]["currentPeriodOrdinal"] if "currentPeriodOrdinal" in gameData["linescore"] else None
		self.currentPeriodTimeRemaining =	gameData["linescore"]["currentPeriodTimeRemaining"] if "currentPeriodTimeRemaining" in gameData["linescore"] else None

		self.scoringPlays =	self.getScoringPlays(gameData["scoringPlays"])

		config = ConfigParser(allow_no_value=True)
		config.read('config.ini')

		localTimeZone = pytz.timezone(config.get('miscellaneous', 'timezone'))

		self.startTime =	pytz.UTC.localize(datetime.datetime.strptime(gameData["gameDate"], "%Y-%m-%dT%H:%M:%SZ")).astimezone(localTimeZone)

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

	def getGameStatusOutput(self):
		gameStatusOutputLines = list()

		if (self.currentPeriod != 0):
			# Display the score (e.g. MTL 2 @ TOR 4)
			gameStatusOutputLines.append("{0} {1} @ {2} {3}".format(
				self.awayTeam.abbreviation,
				self.awayScore,
				self.homeTeam.abbreviation,
				self.homeScore))

			# Display the current period and time remaining (e.g. 15:39 3rd)
			gameStatusOutputLines.append("{0} {1}".format(
				self.currentPeriodTimeRemaining,
				self.currentPeriodOrdinal if self.currentPeriodTimeRemaining != "Final" or self.currentPeriod > 3 else "").strip())
		else:
			# Display the matchup (e.g. MTL @ TOR)
			gameStatusOutputLines.append("{0} @ {1}".format(
				self.awayTeam.abbreviation,
				self.homeTeam.abbreviation))

			# Display the time of the game (e.g. 07:30PM)
			gameStatusOutputLines.append("{0}".format(
				self.startTime.strftime("%I:%M%p")))

		return gameStatusOutputLines
