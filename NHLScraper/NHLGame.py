#!/usr/bin/env python3

import datetime, pytz

class NHLGame:
	'The details of a particular game'

	def __init__(self, gameData):
		self.homeTeam = gameData["teams"]["home"]["team"]["name"]
		self.awayTeam = gameData["teams"]["away"]["team"]["name"]
		self.startTime = pytz.UTC.localize(datetime.datetime.strptime(gameData["gameDate"], "%Y-%m-%dT%H:%M:%SZ"))
