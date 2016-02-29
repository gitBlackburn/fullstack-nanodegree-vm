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
    db = connect()
    c =  db.cursor()
    QUERY ="delete from matches;"
    c.execute(QUERY)
    db.commit()
    db.close()
    

def deletePlayers():
    """Remove all the player records from the database."""
    db = connect()
    c = db.cursor()
    QUERY ="delete from players;"
    c.execute(QUERY)
    db.commit()
    db.close()

def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    c = db.cursor()
    QUERY ="select count(*) as num from players;"
    c.execute(QUERY)
    for row in c.fetchall():
        return row[0]
    db.close()
    
def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    db = connect()
    c = db.cursor()
    c.execute("insert into players (name) values (%s)", (name,))
    db.commit()
    db.close()

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
    db = connect()
    c = db.cursor()
    QUERY = '''
    select players.id, players.name, 
    count((select matches.winner from matches where matches.winner = players.id)) as wins, 
    count(matches.winner) as matches
    from players left join matches 
        on players.id = matches.winner or players.id = matches.loser
    group by players.id;
    '''
    c.execute(QUERY)
    return c.fetchall()
    db.close()

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db = connect()
    c = db.cursor()
    c.execute("insert into matches (winner, loser) values ((%s), (%s))", (winner, loser))
    db.commit()
    db.close()
    
 
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
    db = connect()
    c = db.cursor()
    c.execute( '''create view standings as
    select players.id, players.name, 
    count((select matches.winner from matches where matches.winner = players.id)) as wins, 
    count(matches.winner) as matches
    from players left join matches 
        on players.id = matches.winner or players.id = matches.loser
    group by players.id;
    ''')
    db.commit()
    c.execute('''
    select standings_a.id, standings_a.name, standings_b.id, standings_b.name
    from standings as standings_a, standings as standings_b
    where standings_a.wins = standings_b.wins and standings_a.id > standings_b.id
    ''')    
    pairs = c.fetchall()
    c.execute("drop view standings")
    db.commit()
    db.close
    return pairs
    


