import sqlite3
from PlayerList import PlayerList, Player, hitRateList, hitRate, avgPlayerList, pastPlayerList
from oauth2client.service_account import ServiceAccountCredentials
from updateList import openSpreadsheet

#read the necessary information to record to the database
nbaList = pastPlayerList() #create list
spreadsheet = openSpreadsheet() #open the spreadsheeet

prevList = spreadsheet.worksheet('prevNBAHitRate')
nbaList.load_prev_data(prevList, 'nba') #read from previous list and add it to the back of the existing list

# Connect to the SQLite database
conn = sqlite3.connect('Database/ranking.db')
c = conn.cursor()

# Create a table to store player data
c.execute('''CREATE TABLE IF NOT EXISTS players
                (name TEXT, stat TEXT, projection REAL, rank INTEGER, hit INTEGER)''')

    # Iterate over the list of pastPlayer objects
for player in nbaList.players:
    # Extract data from the pastPlayer object
    name = player.name
    stat = ','.join(player.stat)
    projection = player.projection
    rank = player.rank
    hit = player.hit

    # Insert the player data into the database
    c.execute("INSERT INTO players VALUES (?, ?, ?, ?, ?)", (name, stat, projection, rank, hit))

conn.commit()

conn.close()