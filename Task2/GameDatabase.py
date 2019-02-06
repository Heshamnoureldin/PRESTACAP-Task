import sqlite3
import time
import datetime

# Creat Database File If Not Exist And Connect to Database
#conn = sqlite3.connect('Game_Database.db')
# Create Cursor to Do Things In Database
#c = conn.cursor()

#This Method is Responsible for Returning the data from the database as dectionary not a List
#So the data become more readable
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

# This Method is Resopnsible For Creating The Table If Not Exist to Store The Data 
def Create_Results_Table():
    # Creat Database File If Not Exist And Connect to Database
    conn = sqlite3.connect('Game_Database.db')
    # Create Cursor to Do Things In Database
    c = conn.cursor()
    #This Query is Responsible For Creating The TAble for Data If Not Exist 
    c.execute("CREATE TABLE IF NOT EXISTS Mario_Game(GRID_SIZE TEXT,GRID TEXT ,REQUEST_TIME TEXT, GAME_RESULT TEXT)")
    conn.commit()
    c.close
    conn.close()
    
# This Method is Resopnsible For Storing Game Result In The Database 
def Insert_Into_Game_Database(Grid_Size , Grid , Game_Result):
    # Create Mario_Game Table if not Exist
    Create_Results_Table()
    # Create Database File If Not Exist And Connect to Database
    conn = sqlite3.connect('Game_Database.db')
    # Create Cursor to Do Things In Database
    c = conn.cursor()
    # convert Grid List to String to save it in the Database
    Grid = ','.join(Grid)
    print(Grid)
    # convert Result List to String to save it in the Database
    Game_Result = str(Game_Result)
    # Get The Timestamp of The Request
    Request_Timestamp = int(time.time())
    # Convert The Timestamp to Date and Time Format
    Request_Time = str(datetime.datetime.fromtimestamp(Request_Timestamp).strftime('%Y-%m-%d %H:%M:%S'))
    #This Query is Responsible For Inserting Data To Database 
    c.execute("INSERT INTO Mario_Game (GRID_SIZE, GRID , REQUEST_TIME, GAME_RESULT) VALUES (?, ?, ?, ?)",
          (Grid_Size, Grid,Request_Time, Game_Result))
    conn.commit()
    c.close
    conn.close()

# This Method is Resopnsible For Reading Game Result From The Database 
def Read_From_Game_Database():
    # Creat Database File If Not Exist And Connect to Database
    conn = sqlite3.connect('Game_Database.db')
    conn.row_factory = dict_factory
    # Create Cursor to Do Things In Database
    c = conn.cursor()
    data = c.execute('SELECT * FROM Mario_Game;').fetchall()
    #data = c.fetchall()
    #This Loop TO Print The Table Row By Row
    c.close
    conn.close()
    return data
