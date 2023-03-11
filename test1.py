import pandas as pd
import sqlite3

con = sqlite3.connect("archive/database.sqlite")

matches = pd.read_sql("select * from Match", con)

#players_attributes
pa = pd.read_sql("select * from Player_Attributes", con)

players = pd.read_sql("select * from Player", con)

# get player attributes based on the season/year of the match
def get_player_attributes_df(pa, player_id,match_season):    
    pd.options.mode.chained_assignment = None  
    df = pa[pa["player_api_id"]==player_id]
    df.loc[:,'date'] = pd.to_datetime(df['date']).dt.year
    
    if int(match_season[0]) in df['date'].values:
        df = df[df['date']==int(match_season[0])].iloc[0]
    elif int(match_season[1]) in df['date'].values:
        df = df[df['date']==int(match_season[1])].iloc[0]
    else:
        return None
    pd.options.mode.chained_assignment = 'warn'
    
    return df  
    
index = 0
count = 0
my_row_dict = {}   
df = pd.DataFrame({})
for match in matches.index:
    break_flag = False
   
    for i in range(1, 11):
        which_hp = "home_player_%s"%(i)
        which_ap = "away_player_%s"%(i)
        
        hp_id = matches[which_hp][match]
        ap_id = matches[which_ap][match]
        if len(pa[pa["player_api_id"]==hp_id]) == 0:
            break_flag = True
            break
            # my_row_dict[which_hp] = pa[pa["player_api_id"]==hp_id].iloc[0]
        else:
            if len(pa[pa["player_api_id"]==ap_id])==0:
                break_flag = True
                break
        match_season = matches['season'][match].split('/')
        
        hp_pa = get_player_attributes_df(pa, hp_id, match_season)
        ap_pa = get_player_attributes_df(pa, ap_id, match_season)
        
        if(hp_pa is None or ap_pa is None):
            break_flag = True
            break
            
        # creating a dict that stores values for each row/match in out final df
        
        my_row_dict[which_hp+'_overall_rating'] = hp_pa['overall_rating']
        my_row_dict[which_hp+'_stamina'] = hp_pa['stamina']
        my_row_dict[which_hp+'_dribbling'] = hp_pa['dribbling']
        my_row_dict[which_hp+'_ball_control'] = hp_pa['ball_control']
        my_row_dict[which_hp+'_agility'] = hp_pa['agility']
        my_row_dict[which_hp+'_preferred_foot'] = hp_pa['preferred_foot']
        my_row_dict[which_hp+'_crossing'] = hp_pa['crossing']
        my_row_dict[which_hp+'_free_kick_accuracy'] = hp_pa['free_kick_accuracy']
        my_row_dict[which_hp+'_acceleration'] = hp_pa['acceleration']
        my_row_dict[which_hp+'_interceptions'] = hp_pa['interceptions']
        my_row_dict[which_hp+'_positioning'] = hp_pa['positioning']
        my_row_dict[which_hp+'_gk_handling'] = hp_pa['gk_handling']




                
        my_row_dict[which_ap+'_overall_rating'] = ap_pa['overall_rating']
        my_row_dict[which_ap+'_stamina'] = ap_pa['stamina']
        my_row_dict[which_ap+'_dribbling'] = ap_pa['dribbling']
        my_row_dict[which_ap+'_ball_control'] = ap_pa['ball_control']
        my_row_dict[which_ap+'_agility'] = ap_pa['agility']
        my_row_dict[which_ap+'_preferred_foot'] = ap_pa['preferred_foot']
        my_row_dict[which_ap+'_crossing'] = ap_pa['crossing']
        my_row_dict[which_ap+'_free_kick_accuracy'] = ap_pa['free_kick_accuracy']
        my_row_dict[which_ap+'_acceleration'] = ap_pa['acceleration']
        my_row_dict[which_ap+'_interceptions'] = ap_pa['interceptions']
        my_row_dict[which_ap+'_positioning'] = ap_pa['positioning']
        my_row_dict[which_ap+'_gk_handling'] = ap_pa['gk_handling']

        
    if break_flag:
        # next iteration i.e. next match
        continue
    count+=1
     
    # results logic
    home_team_score = matches['home_team_goal'][match]
    away_team_score = matches['away_team_goal'][match]
    
    if (home_team_score > away_team_score):
        result = 1 #win
    elif (home_team_score < away_team_score):
        result = -1 #lose
    elif (home_team_score is None or away_team_score is None):
        result = None
    else:
        result = 0 # draw by default
        
    my_row_dict['home_team_score'] = home_team_score
    my_row_dict['away_team_score'] = away_team_score
    my_row_dict['result'] = result
    
    # print(my_row_dict)
              
    # my_df_dict[index] = my_row_dict

    # making a df from my_row_dict 
    my_df = pd.DataFrame(my_row_dict, index =[index])
    # index += 1
    df = pd.concat([df, my_df],ignore_index=True)
    
    # if(count == 100):
    #     break
    
df.to_csv('my_dataframe.csv')  
df = pd.read_csv('my_dataframe.csv')
