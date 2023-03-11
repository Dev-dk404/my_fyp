# -*- coding: utf-8 -*-
"""
Created on Sat Oct  8 10:20:30 2022

@author: Devendra
"""
import pandas as pd
import sqlite3

# Create a SQL connection to our SQLite database
con = sqlite3.connect("database.sqlite")

cur = con.cursor()

# The result of a "cursor.execute" can be iterated over by row
for row in cur.execute('SELECT * FROM Country;'):
    print(row)
    
# Return all results of query
cur.execute('SELECT team_long_name FROM Team')
print(cur.fetchall())

print()

# Return first result of query
cur.execute('SELECT * FROM player_attributes WHERE id=7')
print(cur.fetchone())

print()

# Read sqlite query results into a pandas DataFrame
df = pd.read_sql_query("SELECT * from Match ", con)

print(df.head())


# Be sure to close the connection
con.close()