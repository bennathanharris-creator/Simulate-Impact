#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 13:58:07 2024

@author: benharris
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn
from scipy.stats import poisson,skellam
import statsmodels.api as sm
import statsmodels.formula.api as smf

# Load in normalised stats
df = pd.read_csv('all_player_stats_24-25_normalised.csv')

df = df[['Player','Team','Minutes','Goals','Assists','Goals + Assists','Non Pen Goals','Pens Scored',
       'Pens Attempted','Prog Carries','Prog Passes','Prog Passes Received','Yellows','Reds','xG',
       'Non Pen xG','xAG','Non Pen xG + xA','Shots','Shots on Target','Non Pen xG per Shot',
       'Goals minus xG','Non Pen Goals minus Non Pen xG','Short Pass','Short Pass Attempted',
       'Medium Pass','Medium Pass Attempted','Long Pass','Long Pass Attempted','xA',
       'Assists minus xAG','Key Passes','Pass into final third','Pass into Pen Area',
       'Cross into Pen Area','Shot Creation Actions','Goal Creation Actions','Tackles','Tackles in Def 3rd',
       'Tackles Won','Dribblers Tackled','Dribbles Challenged','Blocked Shots','Blocked Passes',
       'Interceptions','Clearances','Errors','Touches in Attacking Third','Touches in Pen Area','Take Ons Attempted',
       'Take Ons Won','Carries','Carries into Final Third','Carries into Penalty Area',
       'Miscontrols','Dispossessed','Points Per Match','Goals whilst on Pitch',
       'Goals Conceded whilst on Pitch','xG whilst on Pitch','xG Conceded whilst on Pitch',
       'Net Goals On or Off Pitch per 90','Net xG On or Off Pitch per 90',
       'Fouls Comitted','Fouls Drawn','Offsides','Penalties Won','Penalties Conceded',
       'Own Goals','Recoveries','Aerial Duels Won','Aerial Duels Lost','year','Pens Missed',
       'Short Pass Missed','Medium Pass Missed','Long Pass Missed','Tackles Lost',
       'Challenges Lost','Take Ons Lost','Shots Missed Target','Shots on Target Missed Goal',
       'Goals per 90','Assists per 90','Goals + Assists per 90','Non Pen Goals per 90',
       'Pens Scored per 90','Pens Attempted per 90','Pens Missed per 90',
       'Prog Carries per 90','Prog Passes per 90','Prog Passes Received per 90',
       'Yellows per 90','Reds per 90','xG per 90','Non Pen xG per 90','xAG per 90',
       'Non Pen xG + xA per 90','Shots per 90','Shots on Target per 90',
       'Shots Missed Target per 90','Shots on Target Missed Goal per 90',
       'Non Pen xG per Shot per 90','Goals minus xG per 90',
       'Non Pen Goals minus Non Pen xG per 90','Short Pass per 90',
       'Short Pass Attempted per 90','Short Pass Missed per 90',
       'Medium Pass per 90','Medium Pass Attempted per 90',
       'Medium Pass Missed per 90','Long Pass per 90','Long Pass Attempted per 90',
       'Long Pass Missed per 90','xA per 90','Assists minus xAG per 90',
       'Key Passes per 90','Pass into final third per 90','Pass into Pen Area per 90',
       'Cross into Pen Area per 90','Shot Creation Actions per 90',
       'Goal Creation Actions per 90','Tackles per 90','Tackles in Def 3rd per 90','Tackles Won per 90',
       'Tackles Lost per 90','Dribblers Tackled per 90','Dribbles Challenged per 90',
       'Challenges Lost per 90','Blocked Shots per 90','Blocked Passes per 90',
       'Interceptions per 90','Clearances per 90','Errors per 90',
       'Touches in Attacking Third per 90','Touches in Pen Area per 90','Take Ons Attempted per 90',
       'Take Ons Won per 90','Take Ons Lost per 90','Carries per 90',
       'Carries into Final Third per 90','Carries into Penalty Area per 90',
       'Miscontrols per 90','Dispossessed per 90','Goals whilst on Pitch per 90',
       'Goals Conceded whilst on Pitch per 90','xG whilst on Pitch per 90',
       'xG Conceded whilst on Pitch per 90','Fouls Comitted per 90',
       'Fouls Drawn per 90','Offsides per 90','Penalties Won per 90',
       'Penalties Conceded per 90','Own Goals per 90','Recoveries per 90',
       'Aerial Duels Won per 90','Aerial Duels Lost per 90'
]]

# Filter for players who have played over 500 minutes.
# This ensures no players who have played well but only briefly do not skew
# the ratings. We only want players who are consistently good over a prolonged
# period of the season
df = df[df['Minutes'] > 500]

# Create the attacking impact with multiplication coefficients that are 
# created by me. This is purely done by what I consider important and how 
# important I consider the statistic to be
def create_attacking_impact(df):
     df = df.copy()
     df['Attacking Impact'] = (3*df['Goals per 90'] + 3*df['Assists per 90'] - 3*df['Pens Missed per 90']
         + 0.01*df['Prog Carries per 90'] + 0.01*df['Prog Passes per 90'] + 0.01*df['Prog Passes Received per 90']
         + 0.5*df['xG per 90'] + 0.5*df['xAG per 90'] + 0.1*df['Shots on Target per 90']
         - 0.75*df['Shots Missed Target per 90'] - 0.5*df['Shots on Target Missed Goal per 90']
         + 1*df['Goals minus xG per 90'] + 0.5*df['xA per 90'] + 1*df['Assists minus xAG per 90']
         + 0.2*df['Key Passes per 90'] + 0.01*df['Pass into final third per 90']
         + 0.1*df['Pass into Pen Area per 90'] + 0.1*df['Cross into Pen Area per 90']
         + 0.5*df['Shot Creation Actions per 90'] + 0.75*df['Goal Creation Actions per 90']
         + 0.001*df['Touches in Attacking Third per 90'] + 0.01*df['Touches in Pen Area per 90'] + 0.1*df['Take Ons Won per 90']
         - 0.1*df['Take Ons Lost per 90'] + 0.025*df['Carries into Final Third per 90']
         + 0.1*df['Carries into Penalty Area per 90'] + 0.1*df['Goals whilst on Pitch per 90']
         + 0.05*df['xG whilst on Pitch per 90'] - 0.25*df['Offsides per 90'] + 2*df['Penalties Won per 90'])
     return df['Attacking Impact']

# Do the same for the defensive statistics
def create_defending_impact(df):
    df = df.copy()
    df['Defensive Impact'] = (1.25*df['Tackles Won per 90'] + 0.75*df['Tackles in Def 3rd per 90'] - 0.75*df['Tackles Lost per 90']
    + 0.5*df['Dribblers Tackled per 90'] - 0.25*df['Challenges Lost per 90']
    + df['Blocked Shots per 90'] + 0.5*df['Blocked Passes per 90'] + 0.25*df['Interceptions per 90']
    + 0.1*df['Clearances per 90'] - 3*df['Errors per 90'] 
    - 1.5*df['Goals Conceded whilst on Pitch per 90'] - 0.75*df['xG Conceded whilst on Pitch per 90']
    - 3*df['Penalties Conceded per 90'] - 3*df['Own Goals per 90']
    + 0.1*df['Recoveries per 90'] + 0.5*df['Aerial Duels Won per 90']
    - 0.25*df['Aerial Duels Lost per 90'])
    
    return df['Defensive Impact']

# Repeat again for miscellaneous statistics that fit neither in the attacking
# nor defensive impact rating
def create_misc_impact(df):
    df = df.copy()
    df['Misc Impact'] = (
    - df['Yellows per 90'] - 5*df['Reds per 90'] + 0.01*df['Short Pass per 90']
    - 0.05*df['Short Pass Missed per 90'] + 0.05*df['Medium Pass per 90'] 
    - 0.05*df['Medium Pass Missed per 90'] + 0.1*df['Long Pass per 90'] - 0.01*df['Long Pass Missed per 90']
    + 0.005*df['Carries per 90'] - 0.25*df['Miscontrols per 90'] - 0.25*df['Dispossessed per 90']
    - 0.5*df['Fouls Comitted per 90'] + 0.5*df['Fouls Drawn per 90'])
    
    return df['Misc Impact']


player = df['Player']
team = df['Team'] 
# Round to 2 decimal places to better see the ratings
attack_impact = create_attacking_impact(df).round(2)
defend_impact = create_defending_impact(df).round(2)
miscellaneous_impact = create_misc_impact(df).round(2)
# Add together to create the total impact
total_impact = (attack_impact + defend_impact + miscellaneous_impact).round(2)

impact_stats = {'Player': player, 'Team': team, 'Attacking Impact': attack_impact,
                'Defensive Impact': defend_impact, 'Misc Impact': miscellaneous_impact, 
                'Total Impact': total_impact}


# Create CSV file
impact_df = pd.DataFrame(impact_stats)
impact_df = impact_df.sort_values(by='Total Impact', ascending=False)
impact_df.to_csv('Player_Impact_24-25.csv', index=False)

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    