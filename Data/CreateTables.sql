BEGIN;

CREATE TABLE IF NOT EXISTS Conferences(
	ID						INTEGER	PRIMARY KEY	NOT NULL,
	Name					TEXT,
	ShortName			TEXT,
	Abbreviation	TEXT,
	Active				BOOLEAN
);

CREATE TABLE IF NOT EXISTS Divisions(
	ID						INTEGER	PRIMARY KEY	NOT NULL,
	ConferenceID	INTEGER,
	Name					TEXT,
	Abbreviation	TEXT,
	Active				BOOLEAN,
	FOREIGN KEY(ConferenceID) REFERENCES Conferences(ID)
);

CREATE TABLE IF NOT EXISTS Franchises(
	ID						INTEGER	PRIMARY KEY	NOT NULL,
	LocationName	TEXT,
	TeamName			TEXT
);

CREATE TABLE IF NOT EXISTS Teams(
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
	FOREIGN KEY(FranchiseID)	REFERENCES Franchises(ID),
	FOREIGN KEY(DivisionID)		REFERENCES Divisions(ID)
);

CREATE TABLE IF NOT EXISTS ScoringPlays(
	ID						INTEGER	PRIMARY KEY	NOT NULL,
	EventCode			TEXT,
	APITimeStamp	TEXT,
	Displayed			BOOLEAN
);

COMMIT;
