#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 12:15:16 2024

@author: benharris
"""

import pandas as pd

# Load the dataset 
df = pd.read_csv('all_player_stats_24-25.csv')

# Ensure 'Minutes' column has numeric values and avoid division by zero
df['Minutes'] = pd.to_numeric(df['Minutes'], errors='coerce').replace(0, pd.NA)

df['Pens Missed'] = df['Pens Attempted'] - df['Pens Scored']
df['Short Pass Missed'] = df['Short Pass Attempted'] - df['Short Pass']
df['Medium Pass Missed'] = df['Medium Pass Attempted'] - df['Medium Pass']
df['Long Pass Missed'] = df['Long Pass Attempted'] - df['Long Pass']
df['Tackles Lost'] = df['Tackles'] - df['Tackles Won']
df['Challenges Lost'] = df['Dribbles Challenged'] - df['Dribblers Tackled']
df['Take Ons Lost'] = df['Take Ons Attempted'] - df['Take Ons Won']
df['Shots Missed Target'] = df['Shots'] - df['Shots on Target']
df['Shots on Target Missed Goal'] = df['Shots on Target'] - df['Goals']

# Columns to divide by 'Minutes'
columns_to_normalise = ['Goals','Assists','Goals + Assists','Non Pen Goals',
                        'Pens Scored','Pens Attempted','Pens Missed','Prog Carries','Prog Passes',
                        'Prog Passes Received','Yellows','Reds','xG','Non Pen xG','xAG',
                        'Non Pen xG + xA','Shots','Shots on Target','Shots Missed Target',
                        'Shots on Target Missed Goal','Non Pen xG per Shot',
                        'Goals minus xG','Non Pen Goals minus Non Pen xG','Short Pass',
                        'Short Pass Attempted','Short Pass Missed','Medium Pass',
                        'Medium Pass Attempted','Medium Pass Missed',
                        'Long Pass','Long Pass Attempted','Long Pass Missed','xA',
                        'Assists minus xAG','Key Passes',
                        'Pass into final third','Pass into Pen Area','Cross into Pen Area',
                        'Shot Creation Actions','Goal Creation Actions','Tackles','Tackles in Def 3rd','Tackles Won',
                        'Tackles Lost','Dribblers Tackled','Dribbles Challenged','Challenges Lost','Blocked Shots',
                        'Blocked Passes','Interceptions','Clearances','Errors',
                        'Touches in Attacking Third','Touches in Pen Area','Take Ons Attempted','Take Ons Won',
                        'Take Ons Lost','Carries','Carries into Final Third','Carries into Penalty Area',
                        'Miscontrols','Dispossessed','Goals whilst on Pitch',
                        'Goals Conceded whilst on Pitch','xG whilst on Pitch',
                        'xG Conceded whilst on Pitch','Fouls Comitted','Fouls Drawn',
                        'Offsides','Penalties Won','Penalties Conceded','Own Goals','Recoveries',
                        'Aerial Duels Won','Aerial Duels Lost'
]


for col in columns_to_normalise:
    new_col_name = f'{col} per 90'
    df[new_col_name] = (df[col] / df['Minutes']) * 90  # Adjusts stats to per-90-minutes format
    
    
    
# Save the updated DataFrame
df.to_csv('all_player_stats_24-25_normalised.csv', index=False)



