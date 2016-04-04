-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
DROP DATABASE tournament;

CREATE DATABASE tournament;

DROP TABLE players;

CREATE TABLE players (player_id SERIAL UNIQUE, player_name text, wins integer, matches integer);

DROP TABLE matches;

CREATE TABLE matches (match_id SERIAL UNIQUE, winner integer, loser integer);

