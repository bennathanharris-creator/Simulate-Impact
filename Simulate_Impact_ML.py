#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 24 11:28:45 2025

@author: benharris
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import xgboost as xgb


# --- Load data ----------------------------------------------------------------
df = pd.read_csv('all_player_stats_24-25_normalised.csv')

cols_keep = [
 'Player','Team','Minutes','Goals','Assists','Goals + Assists','Non Pen Goals','Pens Scored',
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
]

# keep only columns present
cols_keep = [c for c in cols_keep if c in df.columns]
df = df[cols_keep].copy()

# filter to players with meaningful minutes
df = df[df['Minutes'] > 500].reset_index(drop=True)

# ---------------------- Attacking Impact model -----------------------------------

# Define the Attacking Target with the important statistics that decide a 
# player's attacking quality
df['Attacking_Target'] = (
    df['Goals whilst on Pitch per 90']
    + df['xG whilst on Pitch per 90']
    + df['Goals per 90']
    + df['Assists per 90']
)
cols = ['Goals whilst on Pitch per 90', 'xG whilst on Pitch per 90', 'Goals per 90', 'Assists per 90']
df[cols] = df[cols].apply(pd.to_numeric, errors='coerce').fillna(0)

# ---------------------- Feature Selection ------------------------------------
# Choose attack-related per-90 features.
feature_cols = ['xG per 90','xAG per 90',
    'Pens Missed per 90',
    'Prog Carries per 90','Prog Passes per 90','Prog Passes Received per 90',
    'Shots on Target per 90','Shots Missed Target per 90',
    'Shots on Target Missed Goal per 90','Goals minus xG per 90','xA per 90',
    'Assists minus xAG per 90','Key Passes per 90','Pass into final third per 90',
    'Pass into Pen Area per 90','Cross into Pen Area per 90','Shot Creation Actions per 90',
    'Goal Creation Actions per 90','Touches in Attacking Third per 90','Touches in Pen Area per 90',
    'Take Ons Won per 90','Take Ons Lost per 90','Carries into Final Third per 90',
    'Carries into Penalty Area per 90','Carries per 90','Offsides per 90','Penalties Won per 90'
]


# Set X and y
X = df[feature_cols].fillna(0).copy()
y = df['Attacking_Target'].copy()

# ---------------------- Train / Test split -----------------------------------
# Keep a test split for evaluation
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)

# Train XGBoost model
xgb_model = xgb.XGBRegressor(
        n_estimators=500,
        learning_rate=0.05,
        max_depth=5,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
        n_jobs=-1,
        eval_metric="rmse"
    )

# Fit the model
xgb_model.fit(
        X_train, y_train,
        eval_set=[(X_test, y_test)],
        verbose=False
    )
ml_model = xgb_model


# ---------------------- Evaluate ML model -----------------------------------
y_pred = ml_model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print(f"ML model test MSE: {mse:.5f}, R2: {r2:.4f}")


# Apply ml_model to full dataset
X_full = X.copy()

df['Attacking Impact ML'] = ml_model.predict(X_full) * 1.5


# ---------------------- Defensive Impact Model -----------------------------------
# The only two statistics that effectively define a player's defensive
# impact are the goals and xG conceded whilst they are on the pitch.
# This does mean that there will be many midfielders and forwards 
# that are rated similarly to defenders for defensive impact, but 
# there is little way around this.
# By adding in Tackles Won per 90 this does mean the better defensive
# players can be rated higher but it is not as accurate as the attacking impact
df['Defensive Target'] = (- df['Goals Conceded whilst on Pitch per 90'] 
                          - df['xG Conceded whilst on Pitch per 90']
                          + df['Tackles Won per 90'])

def_cols = ['Goals Conceded whilst on Pitch per 90', 'xG Conceded whilst on Pitch per 90', 'Tackles Won per 90']
df[def_cols] = df[def_cols].apply(pd.to_numeric, errors='coerce').fillna(0)

# Use only the defensive statistics
def_feature_cols = ['Tackles in Def 3rd per 90', 'Tackles Lost per 90',
                    'Dribblers Tackled per 90', 'Challenges Lost per 90',
                    'Blocked Shots per 90', 'Blocked Passes per 90',
                    'Interceptions per 90', 'Clearances per 90', 
                    'Errors per 90', 'Penalties Conceded per 90',
                    'Own Goals per 90', 'Recoveries per 90',
                    'Aerial Duels Won per 90', 'Aerial Duels Lost per 90']

# Keep only columns that exist
def_feature_cols = [c for c in def_feature_cols if c in df.columns]
if len(def_feature_cols) < 8:
    raise ValueError("Too few feature columns found - check CSV column names or update def_feature_cols.")

X_def = df[def_feature_cols].fillna(0).copy()
y_def = df['Defensive Target'].copy()

X_train_def, X_test_def, y_train_def, y_test_def = train_test_split(X_def, y_def, test_size=0.20, random_state=42)

xgb_model_def = xgb.XGBRegressor(
        n_estimators=500,
        learning_rate=0.05,
        max_depth=5,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
        n_jobs=-1,
        eval_metric="rmse"
    )
    
xgb_model_def.fit(
        X_train_def, y_train_def,
        eval_set=[(X_test_def, y_test_def)],
        verbose=False
    )
ml_model_def = xgb_model_def


X_full_def = X_def.copy()
df['Defensive Impact ML'] = ml_model_def.predict(X_full_def) * 1.5


# ---------------------- Misc Impact model -----------------------------------

# There is no way of defining a 'miscellaneous' target for us to use machine
# learning on, and so I have used the same system, except I have divided by
# a factor of 1.5 in order to have the miscellaneous impact to scale with
# the attacking and defensive impact
def create_misc_impact(df):
    df = df.copy()
    df['Misc Impact'] = (
    - 0.5*df['Yellows per 90'] - 5*df['Reds per 90'] + 0.01*df['Short Pass per 90']
    - 0.05*df['Short Pass Missed per 90'] + 0.05*df['Medium Pass per 90'] 
    - 0.05*df['Medium Pass Missed per 90'] + 0.1*df['Long Pass per 90'] - 0.01*df['Long Pass Missed per 90']
    + 0.005*df['Carries per 90'] - 0.25*df['Miscontrols per 90'] - 0.25*df['Dispossessed per 90']
    - 0.5*df['Fouls Comitted per 90'] + 0.5*df['Fouls Drawn per 90'])
    
    return df['Misc Impact']

# ---------------------- Build final impact DataFrame ---------------------------
player = df['Player']
team = df['Team']

attack_impact_ml = df['Attacking Impact ML'].round(2)
defend_impact = df['Defensive Impact ML'].round(2)
miscellaneous_impact = create_misc_impact(df).round(2)
total_impact_ml = (attack_impact_ml + defend_impact + miscellaneous_impact).round(4)

impact_stats = {
    'Player': player, 'Team': team,
    'Attacking Impact ML': attack_impact_ml,
    'Defensive Impact ML': defend_impact,
    'Misc Impact': miscellaneous_impact,
    'Total Impact (ML)': total_impact_ml
}

impact_df = pd.DataFrame(impact_stats)
impact_df = impact_df.sort_values(by='Total Impact (ML)', ascending=False)

impact_df.to_csv('Player_Impact_ML_24-25.csv', index=False)
print("Saved Player_Impact_ML_24-25.csv and models/ directory.")



