#!/usr/bin/env python3

import requests
import sqlite3
from .NHLConference import NHLConference

class NHLDivision:
	'Details of an NHL Division'

	def __init__(self, divisionData=None, idForDatabase=None, idForAPI=None):
		if (divisionData != None):
			self.__constructDivisionFromJSON(divisionData)
		elif (idForDatabase != None):
			self.__constructDivisionFromDatabase(idForDatabase)
		elif (idForAPI != None):
			self.__constructDivisionFromAPI(idForAPI)
		else:
			print("No NHLDivision object created, need to specify at least one parameter.")

	def __constructDivisionFromJSON(self, divisionData):
		self.id =			divisionData["id"]
		self.name =			divisionData["name"]
		self.abbreviation =	divisionData["abbreviation"]
		self.conference =	NHLConference(conferenceData=divisionData["conference"])
		self.active =		divisionData["active"]

	def __constructDivisionFromDatabase(self, id):
		connection =	sqlite3.connect("SportsTicker.db")
		cursor =		connection.cursor()

		try:
			cursor.execute("SELECT ID, Name, Abbreviation, ConferenceID, Active FROM Divisions WHERE ID=?", (id,))
		except sqlite3.OperationalError:
			print("Error executing Divisions SELECT query in NHLDivision.__constructDivisionFromDatabase, exiting method")
			connection.close()
			return

		row = cursor.fetchone()

		if (row != None):
			self.id =			row[0]
			self.name =			row[1]
			self.abbreviation =	row[2]
			self.conference =	NHLConference(idForDatabase=row[3])
			self.active =		row[4] != 0
		else:
			print("No Divisions exist in the database with ID {0}".format(id))

		connection.close()

	def __constructDivisionFromAPI(self, id):
		divisionsData = NHLDivision.__getDivisionsDataFromAPI(idFilter=id)

		if (divisionsData!= None and len(divisionsData) > 0):
			self.__constructDivisionFromJSON(divisionsData[0])
		else:
			print("No Divisions exist in the API with ID {0}".format(id))

	def getDivisionsFromAPI(idFilter=None):
		divisionsData = NHLDivision.__getDivisionsDataFromAPI(idFilter)

		divisions = list()

		if (divisionsData!= None):
			for divisionData in divisionsData:
				divisions.append(NHLDivision(divisionData=divisionData))

		return divisions

	def __getDivisionsDataFromAPI(idFilter=None):
		divisionsUrl = "https://statsapi.web.nhl.com/api/v1/divisions"

		if (idFilter != None):
			divisionsUrl += "/{0}".format(idFilter)

		divisionsUrl += "?expand=division.conference"

		response = requests.get(divisionsUrl)
		data = response.json()

		if ("divisions" in data):
			return data["divisions"]
		else:
			print("Error retrieving Divisions from API in NHLDivision.__getDivisionsDataFromAPI, exiting method")
			return

	def populateDivisionsTableFromAPI(emptyTable=False):
		divisions = NHLDivision.getDivisionsFromAPI()

		if (divisions != None and len(divisions) > 0):
			if (emptyTable):
				NHLDivision.emptyDivisionsTable()

			connection =	sqlite3.connect("SportsTicker.db")
			cursor =		connection.cursor()

			for division in divisions:
				try:
					cursor.execute("INSERT INTO Divisions (ID, Name, Abbreviation, ConferenceID, Active) VALUES (?, ?, ?, ?, ?)", (division.id, division.name, division.abbreviation, division.conference.id, 1 if division.active else 0))
				except sqlite3.IntegrityError:
					print("Record with ID {0} already exists in Divisions table".format(division.id))
				except sqlite3.OperationalError:
					print("Error inserting record with ID {0} into Divisions table".format(division.id))

			connection.commit()
			connection.close()
		else:
			print("No divisions returned from NHLDivision.getDivisionsFromAPI.")

	def emptyDivisionsTable():
		connection =	sqlite3.connect("SportsTicker.db")
		cursor =		connection.cursor()

		try:
			cursor.execute("DELETE FROM Divisions")
		except sqlite3.OperationalError:
			print("Error executing Divisions DELETE query in NHLDivision.emptyDivisionsTable, exiting method")
			connection.close()
			return

		connection.commit()
		connection.close()
