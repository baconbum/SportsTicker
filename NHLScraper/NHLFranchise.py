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
		else:
			print("No NHLFranchise object created, need to specify at least one parameter.")

	def __constructFranchiseFromJSON(self, franchiseData):
		self.id =			franchiseData["franchiseId"]
		self.locationName =	franchiseData["locationName"]
		self.teamName =		franchiseData["teamName"]

	def __constructFranchiseFromDatabase(self, id):
		connection =	sqlite3.connect("SportsTicker.db")
		cursor =		connection.cursor()

		try:
			cursor.execute("SELECT ID, LocationName, TeamName FROM Franchises WHERE ID=?", (id,))
		except sqlite3.OperationalError:
			print("Error executing Franchises SELECT query in NHLFranchise.__constructFranchiseFromDatabase, exiting method")
			connection.close()
			return

		row = cursor.fetchone()

		if (row != None):
			self.id =			row[0]
			self.locationName =	row[1]
			self.teamName =		row[2]
		else:
			print("No Franchises exist in the database with ID {0}".format(id))

		connection.close()

	def __constructFranchiseFromAPI(self, id):
		franchisesData =  NHLFranchise.__getFranchisesDataFromAPI(idFilter=id)

		if (franchisesData != None and len(franchisesData) > 0):
			self.__constructFranchiseFromJSON(franchisesData[0])
		else:
			print("No Franchises exist in the API with ID {0}".format(id))

	def getFranchisesFromAPI(idFilter=None):
		franchisesData = NHLFranchise.__getFranchisesDataFromAPI(idFilter)

		franchises = list()

		if (franchisesData != None):
			for franchiseData in franchisesData:
				franchises.append(NHLFranchise(franchiseData=franchiseData))

		return franchises

	def __getFranchisesDataFromAPI(idFilter=None):
		franchisesUrl = "https://statsapi.web.nhl.com/api/v1/franchises"

		if (idFilter != None):
			franchisesUrl += "/{0}".format(idFilter)

		response = requests.get(franchisesUrl)
		data = response.json()

		if ("franchises" in data):
			return data["franchises"]
		else:
			print("Error retrieving Franchises from API in NHLFranchise.__getFranchisesDataFromAPI, exiting method")
			return

	def populateFranchisesTableFromAPI(emptyTable=False):
		franchises = NHLFranchise.getFranchisesFromAPI()

		if (franchises != None and len(franchises) > 0):
			if (emptyTable):
				NHLFranchise.emptyFranchisesTable()

			connection =	sqlite3.connect("SportsTicker.db")
			cursor =		connection.cursor()

			for franchise in franchises:
				try:
					cursor.execute("INSERT INTO Franchises (ID, TeamName, LocationName) VALUES (?, ?, ?)", (franchise.id, franchise.teamName, franchise.locationName))
				except sqlite3.IntegrityError:
					print("Record with ID {0} already exists in Franchises table".format(franchise.id))
				except sqlite3.OperationalError:
					print("Error inserting record with ID {0} into Franchises table".format(franchise.id))

			connection.commit()
			connection.close()
		else:
			print("No franchises returned from NHLFranchise.getFranchisesFromAPI.")

	def emptyFranchisesTable():
		connection =	sqlite3.connect("SportsTicker.db")
		cursor =		connection.cursor()

		try:
			cursor.execute("DELETE FROM Franchises")
		except sqlite3.OperationalError:
			print("Error executing Franchises DELETE query in NHLFranchise.emptyFranchisesTable, exiting method")
			connection.close()
			return

		connection.commit()
		connection.close()
