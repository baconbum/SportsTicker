#!/usr/bin/env python3

import requests

class NHLTeam:
	'Details of a team'

	def __init__(self, teamID):
		self.ID = teamID

		teamData = self.getTeamJSON()

		self.name = teamData["name"]
		self.abbreviation = teamData["abbreviation"]

	def getTeamJSON(self):
		teamURL = "https://statsapi.web.nhl.com/api/v1/teams/{0}"

		response = requests.get(teamURL.format(self.ID))
		data = response.json()

		return data["teams"][0]
