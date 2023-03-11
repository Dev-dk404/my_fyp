# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 07:36:37 2023

@author: Devendra
"""

import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
# import numpy as np

# Create a SQL connection to our SQLite database
con = sqlite3.connect("archive/database.sqlite")

cur = con.cursor()

# drop unimportant tables
cur.execute("DROP TABLE IF EXISTS Country;")
# print("Country table dropped")
# print("-----------------------------------")

# # The result of a "cursor.execute" can be iterated over by row
# for row in cur.execute('SELECT * FROM Country;'):
#     print(row)
    
# print()

# # Return all results of query
# cur.execute('SELECT team_long_name FROM Team')
# print(cur.fetchall())

# print()

# # Return first result of query
# cur.execute('SELECT * FROM player_attributes WHERE id=7')
# print(cur.fetchone())

# print()
def get_players_attr():
    players = pd.read_sql("SELECT p.player_api_id, p.player_name,pa.overall_rating, pa.preferred_foot, pa.crossing, pa.stamina, pa.positioning, pa.sprint_speed, pa.long_passing, pa.free_kick_accuracy, pa.dribbling, p.height  from Player p  left Join Player_Attributes pa on p.player_api_id = pa.player_api_id;", con)
    players = players.drop_duplicates()
    players = players.reset_index(drop=True)
    
    # nan_count = match_result.isna().sum()
    # print(nan_count)
    # print()
    
    # nan_count.plot(kind='bar')
    # plt.xlabel('Columns')
    # plt.ylabel('Number of NaN values')
    # plt.title('NaN values in Match Results')
    # plt.show()
    
    # players = players.drop_duplicates(subset='player_api_id',keep='first')
    # players = players.dropna()
    return players

# players = players.rename(columns={'player_api_id':'player'})
# print(players)
# found duplicates in the dataset, so removing duplicate entries and keeping the first entry only
# players = players.drop_duplicates(subset=['player_api_id'], keep= 'last')
# print(players.info())
# print("-----------------------------------")

# home_players = pd.read_sql_query("SELECT home_team_api_id,home_player_1, home_player_2,home_player_3,home_player_4,home_player_5,home_player_6, home_player_7, home_player_8, home_player_9,home_player_10,home_player_11 FROM Match", con)
# home_players = home_players.drop_duplicates(keep="last")
# home_players = home_players.dropna()
# print(home_players.isna().sum())
# print("-----------------------------------")

# away_players = pd.read_sql_query("SELECT away_team_api_id,away_player_1, away_player_2,away_player_3,away_player_4,away_player_5,away_player_6, away_player_7, away_player_8, home_player_9,away_player_10,away_player_11 FROM Match", con)
# away_players = away_players.drop_duplicates(keep="last")
# away_players = away_players.dropna()
# print(away_players.info())
# print("-----------------------------------")

def get_match_results():
    match_result = pd.read_sql_query("SELECT home_team_api_id,home_player_1, home_player_2,home_player_3,home_player_4,home_player_5,home_player_6, home_player_7, home_player_8, home_player_9,home_player_10,home_player_11,away_team_api_id,away_player_1, away_player_2,away_player_3,away_player_4,away_player_5,away_player_6, away_player_7, away_player_8, away_player_9,away_player_10,away_player_11, home_team_goal, away_team_goal FROM Match", con)
 
    # nan_count = match_result.isna().sum()
    # print(nan_count)
    # print()
    
    # nan_count.plot(kind='bar')
    # plt.xlabel('Columns')
    # plt.ylabel('Number of NaN values')
    # plt.title('NaN values in Match Results')
    # plt.show()
    
    # match_result = match_result.drop_duplicates()
    # match_result = match_result.dropna()
    
    # if home team wins, 1, if loses, -1, if draw 0
    def MatchResult(row):
        if row['home_team_goal'] > row['away_team_goal']:
            return 1
        elif row['home_team_goal'] < row['away_team_goal']:
            return -1
        return 0
    
    match_result['result'] = match_result.apply(lambda row: MatchResult(row), axis=1)
    match_result = match_result.reset_index(drop=True)
    # print(match_result.head().to_string())
    return match_result

match_result = get_match_results()
print("length of match_result" ,len(match_result))

# print(match_result.info())
# print(match_result.info())
print("-----------------------------------")
# print(match_result.columns)
# print("-----------------------------------")
# print(match_result['home_player_8'])


for i in range(1, 12):
    home_players = match_result['home_player_{}'.format(i)]
    players = get_players_attr()
    count = 0
    for player_id in home_players:
        if player_id not in players.player_api_id:
            # row = players[players['player_api_id']== a]
            count+=1 
            match_result.drop(match_result.index[match_result['home_player_{}'.format(i)]==player_id],inplace= True)
        # else:
    print("Players id not in ", 'home_player_{}'.format(i), "is ",count)

print(match_result)
print(match_result.isna().sum())
print("-----------------------------------")

# for i in range(1, 12):
#     away_player = list(match_result['away_player_{}'.format(i)])
#     players = get_players_attr()
#     count = 0
#     for player_id in away_player:
#         if player_id not in players.player_api_id:
#             # row = players[players['player_api_id']== a]
#             count+=1   
#         # else:
#         #     count+=1
#         #     match_result = match_result[match_result.home_player_8 != float(a)]
#     print("Players id not in ", 'away_player_{}'.format(i), "is ",count)


# stats = players[players.player_api_id== x]
# print(stats)
# print(x)
# for a in x:
#     y = players.loc(players['player_api_id'] == a)
#     print(y)
# for i in range (1,12):
#     player_id = match_result["home_player_{}".format(i)]
#     print(player_id)
   
    # merged_df = pd.merge(match_result, players, left_on="home_player_{}".format(i),right_on="player_api_id", suffixes=("_left","_home_player{i}"))
    

    

    
# join_tables = players.join(home_players.set_index('home_player_1'), on = "player_api_id")
# print(join_tables.info())

# #testing
# print(join_tables.loc[join_tables['player_api_id']==396884.0])

# Read sqlite query results into a pandas DataFrame
# df = pd.read_sql_query("SELECT * from Match ", con)

# print(df.head())


# Be sure to close the connection
con.close()