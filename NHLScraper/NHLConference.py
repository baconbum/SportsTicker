#!/usr/bin/env python3

import requests
import sqlite3

class NHLConference:
	'Details of an NHL Conference'

	def __init__(self, conferenceData=None, idForDatabase=None, idForAPI=None):
		if (conferenceData != None):
			self.__constructConferenceFromJSON(conferenceData)
		elif (idForDatabase != None):
			self.__constructConferenceFromDatabase(idForDatabase)
		elif (idForAPI != None):
			self.__constructConferenceFromAPI(idForAPI)
		else:
			print("No NHLConference object created, need to specify at least one parameter.")

	def __constructConferenceFromJSON(self, conferenceData):
		self.id =			conferenceData["id"]
		self.name =			conferenceData["name"]
		self.shortName =	conferenceData["shortName"]
		self.abbreviation =	conferenceData["abbreviation"]
		self.active =		conferenceData["active"]

	def __constructConferenceFromDatabase(self, id):
		connection =	sqlite3.connect("SportsTicker.db")
		cursor =		connection.cursor()

		try:
			cursor.execute("SELECT ID, Name, ShortName, Abbreviation, Active FROM NHLConferences WHERE ID=?", (id,))
		except sqlite3.OperationalError:
			print("Error executing NHLConferences SELECT query in NHLConference.__constructConferenceFromDatabase, exiting method")
			connection.close()
			return

		row = cursor.fetchone()

		if (row != None):
			self.id =			row[0]
			self.name =			row[1]
			self.shortName =	row[2]
			self.abbreviation =	row[3]
			self.active =		row[4] != 0
		else:
			print("No records exist in NHLConferences with ID {0}".format(id))

		connection.close()

	def __constructConferenceFromAPI(self, id):
		conferencesData = NHLConference.__getConferencesDataFromAPI(idFilter=id)

		if (conferencesData!= None and len(conferencesData) > 0):
			self.__constructConferenceFromJSON(conferencesData[0])
		else:
			print("No NHL Conference exists in the API with ID {0}".format(id))

	def getConferencesFromAPI(idFilter=None):
		conferencesData = NHLConference.__getConferencesDataFromAPI(idFilter)

		conferences = list()

		if (conferencesData!= None):
			for conferenceData in conferencesData:
				conferences.append(NHLConference(conferenceData=conferenceData))

		return conferences

	def __getConferencesDataFromAPI(idFilter=None):
		conferencesUrl = "https://statsapi.web.nhl.com/api/v1/conferences"

		if (idFilter != None):
			conferencesUrl += "/{0}".format(idFilter)

		response = requests.get(conferencesUrl)
		data = response.json()

		if ("conferences" in data):
			return data["conferences"]
		else:
			print("Error retrieving NHL Conferences from API in NHLConference.__getConferencesDataFromAPI, exiting method")
			return

	def populateConferencesTableFromAPI(emptyTable=False):
		conferences = NHLConference.getConferencesFromAPI()

		if (conferences != None and len(conferences) > 0):
			if (emptyTable):
				NHLConference.emptyConferencesTable()

			connection =	sqlite3.connect("SportsTicker.db")
			cursor =		connection.cursor()

			for conference in conferences:
				try:
					cursor.execute("INSERT INTO NHLConferences (ID, Name, ShortName, Abbreviation, Active) VALUES (?, ?, ?, ?, ?)", (conference.id, conference.name, conference.shortName, conference.abbreviation, 1 if conference.active else 0))
				except sqlite3.IntegrityError:
					print("Record with ID {0} already exists in NHLConferences table".format(conference.id))
				except sqlite3.OperationalError:
					print("Error inserting record with ID {0} into NHLConferences table".format(conference.id))

			connection.commit()
			connection.close()
		else:
			print("No conferences returned from NHLConference.getConferencesFromAPI.")

	def emptyConferencesTable():
		connection =	sqlite3.connect("SportsTicker.db")
		cursor =		connection.cursor()

		try:
			cursor.execute("DELETE FROM NHLConferences")
		except sqlite3.OperationalError:
			print("Error executing NHLConferences DELETE query in NHLConference.emptyConferencesTable, exiting method")
			connection.close()
			return

		connection.commit()
		connection.close()
