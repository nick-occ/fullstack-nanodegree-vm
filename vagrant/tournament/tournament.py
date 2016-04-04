#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    c = conn.cursor()
    c.execute("delete from matches")
    c.execute("update players set wins = 0, matches = 0")
    conn.commit()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    c = conn.cursor()
    c.execute("delete from players")
    conn.commit()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    c = conn.cursor()
    c.execute("select count(*) from players")
    count = c.fetchone()
    count = count[0]
    conn.close()
    return count

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    
    conn = connect()
    c = conn.cursor()
    c.execute("insert into players (player_name,matches,wins) values ('" + name.replace("'","''") + "',0,0)")    
    conn.commit()
    conn.close()

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
      id: the player's unique id (assigned by the database)
      name: the player's full name (as registered)
      wins: the number of matches the player has won
      matches: the number of matches the player has played
    """
    conn = connect()
    c = conn.cursor()
    c.execute("select player_id, player_name, wins, matches from players")
    playerStandings = c.fetchall()
    playerStandings = sorted(playerStandings,key=lambda x:x[1], reverse=True)
    conn.close()
    return playerStandings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect()
    c = conn.cursor()
    c.execute("insert into matches (winner, loser) values (" + str(winner) + ", " + str(loser) + ")")

    c.execute("update players set matches = (select sum(matches) + 1 from players" + 
    " where player_id = " + str(winner) + ") where player_id = " + str(winner))

    c.execute("update players set matches = (select sum(matches) + 1 from players" + 
    " where player_id = " + str(loser) + ") where player_id = " + str(loser))

    c.execute("update players set wins = (select sum(wins) + 1 from players" + 
    " where player_id = " + str(winner) + ") where player_id = " + str(winner))

    conn.commit()
    conn.close()
    
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    conn = connect()
    c = conn.cursor()
    c.execute("select player_id, player_name from players order by wins")
    pairings = c.fetchall()
    conn.close()
    id1 = None
    name1 = None
    id2 = None
    name2 = None
    teamPairings = []
    x = 0
    while x < len(pairings):
        if x % 2 == 0:
            id1 = pairings[x][0] 
            name1 = pairings[x][1] 
        else:
            id2 = pairings[x][0] 
            name2 = pairings[x][1] 
            teamPairings.append((id1,name1,id2,name2))
        x=x+1

    return teamPairings