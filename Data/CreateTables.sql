BEGIN;

CREATE TABLE Conferences(
	ID						INTEGER	PRIMARY KEY	NOT NULL,
	Name					TEXT,
	ShortName			TEXT,
	Abbreviation	TEXT,
	Active				BOOLEAN
);

CREATE TABLE Divisions(
	ID						INTEGER	PRIMARY KEY	NOT NULL,
	ConferenceID	INTEGER,
	Name					TEXT,
	Abbreviation	TEXT,
	Active				BOOLEAN,
	FOREIGN KEY(ConferenceID) REFERENCES Conferences(ID)
);

CREATE TABLE Franchises(
	ID						INTEGER	PRIMARY KEY	NOT NULL,
	LocationName	TEXT,
	TeamName			TEXT
);

CREATE TABLE Teams(
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

CREATE TABLE ScoringPlays(
	ID						INTEGER	PRIMARY KEY	NOT NULL,
	EventCode			TEXT,
	APITimeStamp	TEXT,
	Displayed			BOOLEAN
);

COMMIT;
