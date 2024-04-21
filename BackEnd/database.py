import sqlite3
from PlayerList import PlayerList, Player, hitRateList, hitRate, avgPlayerList, pastPlayerList
from oauth2client.service_account import ServiceAccountCredentials
from updateList import openSpreadsheet

#read the necessary information to record to the database
spreadsheet = openSpreadsheet()
prevList = spreadsheet.worksheet('prevNBAHitRate')

nbaList = pastPlayerList() #create list
nbaList.load_prev_data(prevList, 'nba') #read from previous list and add it to the back of the existing list

conn = sqlite3.connect('Database/ranking.db')

cursor = conn.cursor()

# Create a new table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT,
        age INTEGER
    )
''')

# Insert some data into the table
cursor.execute('''
    INSERT INTO users (name, age) VALUES (?, ?)
''', ('Alice', 30))

cursor.execute('''
    INSERT INTO users (name, age) VALUES (?, ?)
''', ('Bob', 25))

conn.commit()

conn.close()