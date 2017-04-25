import sqlite3

from NHLScraper.NHLConference import NHLConference
from NHLScraper.NHLDivision import NHLDivision
from NHLScraper.NHLFranchise import NHLFranchise
from NHLScraper.NHLTeam import NHLTeam

def initializeDatabase():

	connection =	sqlite3.connect("SportsTicker.db")
	cursor =		connection.cursor()

	# Drop all tables (if they exist)
	tableDeletionSQLPath = open('Data/DropTables.sql','r')
	tableDeletionSQL = tableDeletionSQLPath.read()
	connection.executescript(tableDeletionSQL)

	# Create all tables
	tableCreationSQLPath = open('Data/CreateTables.sql','r')
	tableCreationSQL = tableCreationSQLPath.read()
	connection.executescript(tableCreationSQL)

	connection.close()

	# Populate tables with data from API
	NHLConference.populateConferencesTableFromAPI()
	NHLDivision.populateDivisionsTableFromAPI()
	NHLFranchise.populateFranchisesTableFromAPI()
	NHLTeam.populateTeamsTableFromAPI()

initializeDatabase()
