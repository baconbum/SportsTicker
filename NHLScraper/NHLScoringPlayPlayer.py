#!/usr/bin/env python3

class NHLScoringPlayPlayer:
	'Details of a player who took part in a scoring play'

	def __init__(self, scoringPlayPlayerData):
		self.fullName =		scoringPlayPlayerData["player"]["fullName"]
		self.playerType =	scoringPlayPlayerData["playerType"]

		if (self.playerType != "Goalie"):
			self.seasonTotal =	scoringPlayPlayerData["seasonTotal"]
