#!/usr/bin/env python3

import requests
import sqlite3
from .NHLDivision import NHLDivision
from .NHLFranchise import NHLFranchise

class NHLTeam:
	'Details of an NHL Team'

	def __init__(self, teamData=None, idForDatabase=None, idForAPI=None):
		if (teamData != None):
			self.__constructTeamFromJSON(teamData)
		elif (idForDatabase != None):
			self.__constructTeamFromDatabase(idForDatabase)
		elif (idForAPI != None):
			self.__constructTeamFromAPI(idForAPI)
		else:
			print("No NHLTeam object created, need to specify at least one parameter.")

	def __constructTeamFromJSON(self, teamData):
		self.id =			teamData["id"]
		self.name =			teamData["name"]
		self.locationName =	teamData["locationName"]
		self.teamName =		teamData["teamName"]
		self.shortName =	teamData["shortName"]
		self.abbreviation =	teamData["abbreviation"]
		self.division =		NHLDivision(divisionData=teamData["division"])
		self.franchise =	NHLFranchise(franchiseData=teamData["franchise"])
		self.active =		teamData["active"]

	def __constructTeamFromDatabase(self, id):
		connection =	sqlite3.connect("SportsTicker.db")
		cursor =		connection.cursor()

		try:
			cursor.execute("SELECT ID, Name, LocationName, TeamName, ShortName, Abbreviation, FranchiseID, DivisionID, Active FROM Teams WHERE ID=?", (id,))
		except sqlite3.OperationalError:
			print("Error executing Teams SELECT query in NHLTeam.__constructTeamFromDatabase, exiting method")
			connection.close()
			return

		row = cursor.fetchone()

		if (row != None):
			self.id =			row[0]
			self.name =			row[1]
			self.locationName =	row[2]
			self.teamName =		row[3]
			self.shortName =	row[4]
			self.abbreviation =	row[5]
			self.franchise =	NHLFranchise(idForDatabase=row[6])
			self.division =		NHLDivision(idForDatabase=row[7])
			self.active =		row[8] != 0
		else:
			print("No Teams exist in the database with ID {0}".format(id))

		connection.close()

	def __constructTeamFromAPI(self, id):
		teamsData = NHLTeam.__getTeamsDataFromAPI(idFilter=id)

		if (teamsData!= None and len(teamsData) > 0):
			self.__constructTeamFromJSON(teamsData[0])
		else:
			print("No Teams exist in the API with ID {0}".format(id))

	def getTeamsFromAPI(idFilter=None):
		teamsData = NHLTeam.__getTeamsDataFromAPI(idFilter)

		teams = list()

		if (teamsData!= None):
			for teamData in teamsData:
				teams.append(NHLTeam(teamData=teamData))

		return teams

	def __getTeamsDataFromAPI(idFilter=None):
		teamsUrl = "https://statsapi.web.nhl.com/api/v1/teams"

		if (idFilter != None):
			teamsUrl += "/{0}".format(idFilter)

		teamsUrl += "?expand=team.division,division.conference,team.franchise"

		response = requests.get(teamsUrl)
		data = response.json()

		if ("teams" in data):
			return data["teams"]
		else:
			print("Error retrieving Teams from API in NHLTeam.__getTeamsDataFromAPI, exiting method")
			return

	def populateTeamsTableFromAPI(emptyTable=False):
		teams = NHLTeam.getTeamsFromAPI()

		if (teams != None and len(teams) > 0):
			if (emptyTable):
				NHLTeam.emptyTeamsTable()

			connection =	sqlite3.connect("SportsTicker.db")
			cursor =		connection.cursor()

			for team in teams:
				try:
					cursor.execute("INSERT INTO Teams (ID, Name, LocationName, TeamName, ShortName, Abbreviation, FranchiseID, DivisionID, Active) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (team.id, team.name, team.locationName, team.teamName, team.shortName, team.abbreviation, team.franchise.id, team.division.id, 1 if team.active else 0))
				except sqlite3.IntegrityError:
					print("Record with ID {0} already exists in Teams table".format(team.id))
				except sqlite3.OperationalError:
					print("Error inserting record with ID {0} into Teams table".format(team.id))

			connection.commit()
			connection.close()
		else:
			print("No teams returned from NHLTeam.getTeamsFromAPI.")

	def emptyTeamsTable():
		connection =	sqlite3.connect("SportsTicker.db")
		cursor =		connection.cursor()

		try:
			cursor.execute("DELETE FROM Teams")
		except sqlite3.OperationalError:
			print("Error executing Teams DELETE query in NHLTeam.emptyTeamsTable, exiting method")
			connection.close()
			return

		connection.commit()
		connection.close()
