-- Table definitions for the tournament project.

DROP DATABASE IF EXISTS tournament;

CREATE DATABASE tournament;

\c tournament

CREATE TABLE players (
			 name TEXT,
			 id SERIAL PRIMARY KEY);
			 
CREATE TABLE matches (
             winner INT REFERENCES players(id),
			 loser INT REFERENCES players(id),
			 match_id SERIAL PRIMARY KEY);
	


\c vagrant






