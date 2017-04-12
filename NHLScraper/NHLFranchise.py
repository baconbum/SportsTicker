#!/usr/bin/env python3

import requests
import sqlite3

class NHLFranchise:
	'Details of an NHL Franchise'

	def __init__(self, franchiseData=None, idForDatabase=None, idForAPI=None):
		if (franchiseData != None):
			self.__constructFranchiseFromJSON(franchiseData)
		elif (idForDatabase != None):
			self.__constructFranchiseFromDatabase(idForDatabase)
		elif (idForAPI != None):
			self.__constructFranchiseFromAPI(idForAPI)

	def __constructFranchiseFromJSON(self, franchiseData):
		self.id =			franchiseData["franchiseId"]
		self.locationName =	franchiseData["locationName"]
		self.teamName =		franchiseData["teamName"]

	def __constructFranchiseFromDatabase(self, id):
		connection =	sqlite3.connect("SportsTicker.db")
		cursor =		connection.cursor()

		cursor.execute("SELECT ID, LocationName, TeamName FROM Franchises WHERE ID=?", (id,))

		row = cursor.fetchone()

		if (row != None):
			self.id =			row[0]
			self.locationName =	row[1]
			self.teamName =		row[2]

		connection.close()

	def __constructFranchiseFromAPI(self, id):
		franchisesData =  NHLFranchise.__getFranchisesDataFromAPI(idFilter=id)

		if (len(franchisesData) > 0):
			self.__constructFranchiseFromJSON(franchisesData[0])

	def getFranchisesFromAPI(idFilter=None):
		franchisesData = NHLFranchise.__getFranchisesDataFromAPI(idFilter)

		franchises = list()

		for franchiseData in franchisesData:
			franchises.append(NHLFranchise(franchiseData=franchiseData))

		return franchises

	def __getFranchisesDataFromAPI(idFilter=None):
		franchisesUrl = "https://statsapi.web.nhl.com/api/v1/franchises"

		if (idFilter != None):
			franchisesUrl += "/{0}".format(idFilter)

		response = requests.get(franchisesUrl)
		data = response.json()

		return data["franchises"]

	def populateDatabaseWithFranchisesFromAPI():
		connection =	sqlite3.connect("SportsTicker.db")
		cursor =		connection.cursor()

		cursor.execute("DELETE FROM Franchises")

		franchises = NHLFranchise.getFranchisesFromAPI()

		for franchise in franchises:
			cursor.execute("INSERT INTO Franchises (ID, TeamName, LocationName) VALUES (?, ?, ?)", (franchise.id, franchise.teamName, franchise.locationName))

		connection.commit()
		connection.close()
