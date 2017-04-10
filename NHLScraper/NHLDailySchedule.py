#!/usr/bin/env python3

import requests
from .NHLGame import NHLGame

class NHLDailySchedule:
	'The collection of games on particular day'

	def __init__(self, date):
		self.date = date
		self.games = self.getGames()

	def getGames(self):
		gamesList = list()

		scheduleUrl = "https://statsapi.web.nhl.com/api/v1/schedule?startDate={0}&endDate={0}&expand=schedule.scoringplays"

		response = requests.get(scheduleUrl.format(self.date.strftime("%Y-%m-%d")))
		print(response)
		data = response.json()

		for gameData in data["dates"][0]["games"]:
			gamesList.append(NHLGame(gameData))

		return gamesList
