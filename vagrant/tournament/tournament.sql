-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
DROP DATABASE IF EXISTS tournament;

CREATE DATABASE tournament;

\c tournament;

DROP TABLE IF EXISTS players;

CREATE TABLE players (player_id SERIAL UNIQUE, player_name text);

DROP TABLE IF EXISTS matches;

CREATE TABLE matches (match_id SERIAL UNIQUE, winner integer REFERENCES players(player_id), loser integer REFERENCES players(player_id));

DROP VIEW IF EXISTS wintracker;

CREATE VIEW wintracker
AS
  SELECT players.player_id,
         players.player_name,
         COUNT(matches.winner) AS wins
  FROM   players
         LEFT JOIN matches
                ON players.player_id = matches.winner
  GROUP  BY players.player_id,players.player_name;
  
DROP VIEW IF EXISTS matchtracker;

CREATE VIEW matchtracker
AS
  SELECT players.player_id,
         players.player_name,
         COUNT(matches) AS matchesplayed
  FROM   players
         LEFT JOIN matches
                ON players.player_id = matches.winner
                    OR players.player_id = matches.loser
  GROUP  BY players.player_id,players.player_name;
  

DROP VIEW IF EXISTS standings;

CREATE VIEW standings
AS
SELECT wintracker.player_id, wintracker.player_name, wintracker.wins, matchtracker.matchesplayed
from wintracker join matchtracker on wintracker.player_id = matchtracker.player_id order by wintracker.wins desc;