#!/usr/bin/env python3

import datetime, pytz
from .NHLTeam import NHLTeam

class NHLScoringPlay:
	'Details of a scoring play'

	def __init__(self, scoringPlayData):
		self.team =				NHLTeam(scoringPlayData["team"]["id"])
		self.timeStamp =		pytz.UTC.localize(datetime.datetime.strptime(scoringPlayData["about"]["dateTime"], "%Y-%m-%dT%H:%M:%SZ"))

		self.homeScore =		scoringPlayData["about"]["goals"]["home"]
		self.awayScore =		scoringPlayData["about"]["goals"]["away"]
		self.period =			scoringPlayData["about"]["period"]
		self.periodOrdinal =	scoringPlayData["about"]["ordinalNum"]
		self.periodTime =		scoringPlayData["about"]["periodTime"]
