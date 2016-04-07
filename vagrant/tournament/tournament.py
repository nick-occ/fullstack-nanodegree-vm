#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import sys

def connect(db="tournament"):
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        conn = psycopg2.connect("dbname={}".format(db))
        c = conn.cursor()
        return conn, c
    except:
        print("unable to connect to db")
        sys.exit()


def deleteMatches():
    """Remove all the match records from the database."""
    conn,c = connect()
    c.execute("delete from matches")
    conn.commit()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    conn,c = connect()
    c.execute("delete from players")
    conn.commit()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""
    conn,c = connect()
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
    
    conn,c = connect()
    sql = "insert into players (player_name) values (%s)"
    data = (name,)
    c.execute(sql,data)    
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
    conn,c = connect()
    c.execute("select * from standings")
    playerStandings = c.fetchall()
    conn.close()
    return playerStandings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn,c = connect()
        
    sql = "insert into matches (winner, loser) values (%s,%s)"
    data = (str(winner),str(loser),)
    c.execute(sql,data)

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
    
    pairings = playerStandings()
    id1 = None
    name1 = None
    id2 = None
    name2 = None
    teamPairings = []
    
    for x in xrange(0,len(pairings),2):
        id1 = pairings[x][0] 
        name1 = pairings[x][1] 
        id2 = pairings[x+1][0] 
        name2 = pairings[x+1][1]
        teamPairings.append((id1,name1,id2,name2))

    return teamPairings
