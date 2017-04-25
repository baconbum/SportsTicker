BEGIN;

CREATE TABLE IF NOT EXISTS NHLConferences(
	ID						INTEGER	PRIMARY KEY	NOT NULL,
	Name					TEXT,
	ShortName			TEXT,
	Abbreviation	TEXT,
	Active				BOOLEAN
);

CREATE TABLE IF NOT EXISTS NHLDivisions(
	ID						INTEGER	PRIMARY KEY	NOT NULL,
	ConferenceID	INTEGER,
	Name					TEXT,
	Abbreviation	TEXT,
	Active				BOOLEAN,
	FOREIGN KEY(ConferenceID) REFERENCES NHLConferences(ID)
);

CREATE TABLE IF NOT EXISTS NHLFranchises(
	ID						INTEGER	PRIMARY KEY	NOT NULL,
	LocationName	TEXT,
	TeamName			TEXT
);

CREATE TABLE IF NOT EXISTS NHLTeams(
	ID						INTEGER	PRIMARY KEY	NOT NULL,
	FranchiseID		INTEGER,
	DivisionID		INTEGER,
	ConferenceID	INTEGER,
	Name					TEXT,
	LocationName	TEXT,
	TeamName			TEXT,
	ShortName			TEXT,
	Abbreviation	TEXT,
	Active				BOOLEAN,
	FOREIGN KEY(FranchiseID)	REFERENCES NHLFranchises(ID),
	FOREIGN KEY(DivisionID)		REFERENCES NHLDivisions(ID)
);

CREATE TABLE IF NOT EXISTS NHLScoringPlays(
	ID						INTEGER	PRIMARY KEY	NOT NULL,
	EventCode			TEXT,
	APITimeStamp	TEXT,
	Displayed			BOOLEAN
);

COMMIT;
