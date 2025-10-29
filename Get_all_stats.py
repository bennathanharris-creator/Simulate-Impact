#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 16:16:53 2024

@author: benharris
"""

from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time

# Generate year strings in the format 'YYYY-YYYY'
years = [f"{year}-{year+1}" for year in range(2024, 2025)]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
}


# Safely extract text with a check for None
def safe_get_text(element):
    if element:
        return element.get_text(strip=True)
    return '0'  

# Function to clean up the stats
def clean_stat(value):
    if isinstance(value, str):
        # Remove commas inside strings and then convert to float
        value = value.replace(",", "")
        try:
            return float(value)  # Try converting to float
        except ValueError:
            return value  # Return the value as is if it's not a valid number (like player names)
    return value

def get_standard_stats(year):
    # URL for the stats page
    web = f'https://fbref.com/en/comps/9/{year}/stats/{year}-Premier-League-Stats'
    print(f"Loading URL: {web}")

    # Set up Selenium WebDriver
    driver = webdriver.Chrome()
    
    try:
        # Open the webpage
        driver.get(web)

        # Extract the HTML content
        content = driver.page_source
        
    finally:
        # Close the browser window
        driver.quit()

    # Parse the content with BeautifulSoup
    soup = BeautifulSoup(content, 'lxml')
    
    # Locate the correct table within 'all_stats_standard'
    stats_table = soup.find('div', {'id': 'all_stats_standard'}).find('table')
    
    if not stats_table:
        print("No table found in 'all_stats_standard'")
        return pd.DataFrame()

    # Extract data from the table
    rows = stats_table.find('tbody').find_all('tr')
    
    player_name = []
    team = []
    minutes_played = []
    goals = []
    assists = []
    goals_plus_assists = []
    non_pen_goals = []
    pens_scored = []
    pens_attempted = []
    prog_carries = []
    prog_passes = []
    prog_passes_received = []
    yellows = []
    reds = []
    xG = []
    non_pen_xG = []
    xAG = []
    non_pen_xG_plus_xA = []
    
    
    # Extract the data from the html code at 'data-stat' = stat to be extracted
    for row in rows:
        player_name_element = row.find('td', {'data-stat': 'player'})
        # Skip rows with no player name
        if player_name_element is None or not player_name_element.get_text(strip=True):
            continue  # Skip empty rows
        team_element = row.find('td', {'data-stat': 'team'})
        minutes_played_element = row.find('td', {'data-stat': 'minutes'})
        goals_element = row.find('td', {'data-stat': 'goals'})
        assists_element = row.find('td', {'data-stat': 'assists'})
        goals_plus_assists_element = row.find('td', {'data-stat': 'goals_assists'})
        non_pen_goals_element = row.find('td', {'data-stat': 'goals_pens'})
        pens_made_element = row.find('td', {'data-stat': 'pens_made'})
        pens_attempted_element = row.find('td', {'data-stat': 'pens_att'})
        prog_carries_element = row.find('td', {'data-stat': 'progressive_carries'})
        prog_passes_element = row.find('td', {'data-stat': 'progressive_passes'})
        prog_passes_received_element = row.find('td', {'data-stat': 'progressive_passes_received'})
        yellows_element = row.find('td', {'data-stat': 'cards_yellow'})
        reds_element = row.find('td', {'datat-stat': 'cards_red'})
        xG_element = row.find('td', {'data-stat': 'xg'})
        non_pen_xG_element = row.find('td', {'data-stat': 'npxg'})
        xA_element = row.find('td', {'data-stat': 'xg_assist'})
        non_pen_xG_plus_xA_element = row.find('td', {'data-stat': 'npxg_xg_assist'})
        
        # Clean the data
        player = clean_stat(safe_get_text(player_name_element))
        team1 = clean_stat(safe_get_text(team_element))
        minutes = clean_stat(safe_get_text(minutes_played_element))
        G = clean_stat(safe_get_text(goals_element))
        A = clean_stat(safe_get_text(assists_element))
        G_plus_A = clean_stat(safe_get_text(goals_plus_assists_element))
        npG = clean_stat(safe_get_text(non_pen_goals_element))
        pens = clean_stat(safe_get_text(pens_made_element))
        pens_att = clean_stat(safe_get_text(pens_attempted_element))
        progC = clean_stat(safe_get_text(prog_carries_element))
        progP = clean_stat(safe_get_text(prog_passes_element))
        progPR = clean_stat(safe_get_text(prog_passes_received_element))
        yellow_cards = clean_stat(safe_get_text(yellows_element))
        red_cards = clean_stat(safe_get_text(reds_element))
        xg = clean_stat(safe_get_text(xG_element))
        npxg = clean_stat(safe_get_text(non_pen_xG_element))
        xa = clean_stat(safe_get_text(xA_element))
        npxg_plus_xa = clean_stat(safe_get_text(non_pen_xG_plus_xA_element))
        
        player_name.append(player)
        team.append(team1)
        minutes_played.append(minutes)
        goals.append(G)
        assists.append(A)
        goals_plus_assists.append(G_plus_A)
        non_pen_goals.append(npG)
        pens_scored.append(pens)
        pens_attempted.append(pens_att)
        prog_carries.append(progC)
        prog_passes.append(progP)
        prog_passes_received.append(progPR)
        yellows.append(yellow_cards)
        reds.append(red_cards)
        xG.append(xg)
        non_pen_xG.append(npxg)
        xAG.append(xa)
        non_pen_xG_plus_xA.append(npxg_plus_xa)
        
    # Send to dataframe as long as there is a player's name
    if player_name:
        dict_football = {'Player': player_name, 'Team': team, 'Minutes': minutes_played, 'Goals': goals,
                         'Assists': assists, 'Goals + Assists': goals_plus_assists,
                         'Non Pen Goals': non_pen_goals, 'Pens Scored': pens_scored,
                         'Pens Attempted': pens_attempted, 'Prog Carries': prog_carries,
                         'Prog Passes': prog_passes, 'Prog Passes Received': prog_passes_received,
                         'Yellows': yellows, 'Reds': reds, 'xG': xG, 'Non Pen xG': non_pen_xG,
                         'xAG': xAG, 'Non Pen xG + xA': non_pen_xG_plus_xA}
        df_football = pd.DataFrame(dict_football)
        df_football.fillna(0, inplace=True)
        print(f"Data extracted for {year}")
        return df_football
    else:
        print(f"No data extracted for {year}")
        return pd.DataFrame()
    
# Repeat same process for every other table to get all stats 
def get_shooting_stats(year):
    web = f'https://fbref.com/en/comps/9/{year}/shooting/{year}-Premier-League-Stats'
    print(f"Requesting URL: {web}")
    
    driver = webdriver.Chrome()
    
    try:
        driver.get(web)
        

        content = driver.page_source
        
    finally:
        driver.quit()

    soup = BeautifulSoup(content, 'lxml')
    
    stats_table = soup.find('div', {'id': 'all_stats_shooting'}).find('table')
    
    if not stats_table:
        print("No table found in 'all_stats_shooting'")
        return pd.DataFrame()

    rows = stats_table.find('tbody').find_all('tr')
    
    player_name = []
    shots = []
    shots_on_target = []
    npxG_per_shot = []
    G_minus_xG = []
    npG_minus_npxG = []
    
    for row in rows:
        player_name_element = row.find('td', {'data-stat': 'player'})
        if player_name_element is None or not player_name_element.get_text(strip=True):
            continue  
        shots_element = row.find('td', {'data-stat': 'shots'})
        shots_on_target_element = row.find('td', {'data-stat': 'shots_on_target'})
        non_pen_xG_per_shot_element = row.find('td', {'data-stat': 'npxg_per_shot'})
        goals_minus_xG_element = row.find('td', {'data-stat': 'xg_net'})
        non_pen_goals_minus_non_pen_xG_element = row.find('td', {'data-stat': 'npxg_net'})

        player = clean_stat(safe_get_text(player_name_element))
        shot = clean_stat(safe_get_text(shots_element))
        SoT = clean_stat(safe_get_text(shots_on_target_element))
        npxg_per_shot = clean_stat(safe_get_text(non_pen_xG_per_shot_element))
        g_minus_xg = clean_stat(safe_get_text(goals_minus_xG_element))
        npg_minus_npxg = clean_stat(safe_get_text(non_pen_goals_minus_non_pen_xG_element))
        
        player_name.append(player)
        shots.append(shot)
        shots_on_target.append(SoT)
        npxG_per_shot.append(npxg_per_shot)
        G_minus_xG.append(g_minus_xg)
        npG_minus_npxG.append(npg_minus_npxg)
        
    if player_name:
        dict_football = {'Player': player_name, 'Shots': shots, 'Shots on Target': shots_on_target,
                         'Non Pen xG per Shot': npxG_per_shot, 'Goals minus xG': G_minus_xG,
                         'Non Pen Goals minus Non Pen xG': npG_minus_npxG}
        df_football = pd.DataFrame(dict_football)
        df_football.fillna(0, inplace=True)
        print(f"Data extracted for {year}")
        return df_football
    else:
        print(f"No data extracted for {year}")
        return pd.DataFrame()
        
    
def get_passing_stats(year):
    web = f'https://fbref.com/en/comps/9/{year}/passing/{year}-Premier-League-Stats'
    print(f"Requesting URL: {web}")
    
    driver = webdriver.Chrome()
    
    try:
        driver.get(web)
        

        content = driver.page_source
        
    finally:
        driver.quit()

    soup = BeautifulSoup(content, 'lxml')
    
    stats_table = soup.find('div', {'id': 'all_stats_passing'}).find('table')
    
    if not stats_table:
        print("No table found in 'all_stats_passing'")
        return pd.DataFrame()

    rows = stats_table.find('tbody').find_all('tr')
    
    player_name = []
    short_passes_completed = []
    short_passes_attempted = []
    medium_passes_completed = []
    medium_passes_attempted = []
    long_passes_completed =[]
    long_passes_attempted = []
    xA = []
    assists_minus_xAG = []
    key_passes = []
    pass_into_final_third = []
    pass_into_pen_area = []
    cross_into_pen_area = []
    
    
    for row in rows:
        player_name_element = row.find('td', {'data-stat': 'player'})
        if player_name_element is None or not player_name_element.get_text(strip=True):
            continue  
        short_passes_completed_element = row.find('td', {'data-stat': 'passes_completed_short'})
        short_passes_attempted_element = row.find('td', {'data-stat': 'passes_short'})
        medium_passes_completed_element = row.find('td', {'data-stat': 'passes_completed_medium'})
        medium_passes_attempted_element = row.find('td', {'data-stat': 'passes_medium'})
        long_passes_completed_element = row.find('td', {'data-stat': 'passes_completed_long'})
        long_passes_attempted_element = row.find('td', {'data-stat': 'passes_long'})
        xA_element = row.find('td', {'data-stat': 'pass_xa'})
        assists_minus_xAG_element = row.find('td', {'data-stat': 'xg_assist_net'})
        key_passes_element = row.find('td', {'data-stat': 'assisted_shots'})
        pass_into_final_third_element = row.find('td', {'data-stat': 'passes_into_final_third'})
        pass_into_pen_area_element = row.find('td', {'data-stat': 'passes_into_penalty_area'})
        cross_into_pen_area_element = row.find('td', {'data-stat': 'crosses_into_penalty_area'})
        
        player_name1 = clean_stat(safe_get_text(player_name_element))
        short_passes_completed1 = clean_stat(safe_get_text(short_passes_completed_element))
        short_passes_attempted1 = clean_stat(safe_get_text(short_passes_attempted_element))
        medium_passes_completed1 = clean_stat(safe_get_text(medium_passes_completed_element))
        medium_passes_attempted1 = clean_stat(safe_get_text(medium_passes_attempted_element))
        long_passes_completed1 = clean_stat(safe_get_text(long_passes_completed_element))
        long_passes_attempted1 = clean_stat(safe_get_text(long_passes_attempted_element))
        xA1 = clean_stat(safe_get_text(xA_element))
        assists_minus_xAG1 = clean_stat(safe_get_text(assists_minus_xAG_element))
        key_passes1 = clean_stat(safe_get_text(key_passes_element))
        pass_into_final_third1 = clean_stat(safe_get_text(pass_into_final_third_element))
        pass_into_pen_area1 = clean_stat(safe_get_text(pass_into_pen_area_element))
        cross_into_pen_area1 = clean_stat(safe_get_text(cross_into_pen_area_element))
        
        player_name.append(player_name1)
        short_passes_completed.append(short_passes_completed1)
        short_passes_attempted.append(short_passes_attempted1)
        medium_passes_completed.append(medium_passes_completed1)
        medium_passes_attempted.append(medium_passes_attempted1)
        long_passes_completed.append(long_passes_completed1)
        long_passes_attempted.append(long_passes_attempted1)
        xA.append(xA1)
        assists_minus_xAG.append(assists_minus_xAG1)
        key_passes.append(key_passes1)
        pass_into_final_third.append(pass_into_final_third1)
        pass_into_pen_area.append(pass_into_pen_area1)
        cross_into_pen_area.append(cross_into_pen_area1)
        
    if player_name:
        dict_football = {'Player': player_name, 'Short Pass': short_passes_completed, 'Short Pass Attempted': short_passes_attempted,
                         'Medium Pass': medium_passes_completed, 'Medium Pass Attempted': medium_passes_attempted,
                         'Long Pass': long_passes_completed, 'Long Pass Attempted': long_passes_attempted,
                         'xA': xA, 'Assists minus xAG': assists_minus_xAG, 'Key Passes': key_passes,
                         'Pass into final third': pass_into_final_third, 'Pass into Pen Area': pass_into_pen_area,
                         'Cross into Pen Area': cross_into_pen_area}
        df_football = pd.DataFrame(dict_football)
        df_football.fillna(0, inplace=True)
        print(f"Data extracted for {year}")
        return df_football
    else:
        print(f"No data extracted for {year}")
        return pd.DataFrame() 

def get_gca_stats(year):
    web = f'https://fbref.com/en/comps/9/{year}/gca/{year}-Premier-League-Stats'
    print(f"Requesting URL: {web}")
    
    driver = webdriver.Chrome()
    
    try:
        driver.get(web)
        

        content = driver.page_source
        
    finally:
        driver.quit()

    soup = BeautifulSoup(content, 'lxml')
    
    stats_table = soup.find('div', {'id': 'all_stats_gca'}).find('table')
    
    if not stats_table:
        print("No table found in 'all_stats_gca'")
        return pd.DataFrame()

    rows = stats_table.find('tbody').find_all('tr')
    
    player_name = []
    sca = []
    gca = []
    
    for row in rows:
        player_name_element = row.find('td', {'data-stat': 'player'})
        if player_name_element is None or not player_name_element.get_text(strip=True):
            continue  
        sca_element = row.find('td', {'data-stat': 'sca'})
        gca_element = row.find('td', {'data-stat': 'gca'})
        
        player_name1 = clean_stat(safe_get_text(player_name_element))
        sca1 = clean_stat(safe_get_text(sca_element))
        gca1 = clean_stat(safe_get_text(gca_element))
        
        player_name.append(player_name1)
        sca.append(sca1)
        gca.append(gca1)
        
    if player_name:
        dict_football = {'Player': player_name, 'Shot Creation Actions': sca,
                         'Goal Creation Actions': gca}
        df_football = pd.DataFrame(dict_football)
        df_football.fillna(0, inplace=True)
        print(f"Data extracted for {year}")
        return df_football
    else:
        print(f"No data extracted for {year}")
        return pd.DataFrame() 
    
def get_defence_stats(year):
    web = f'https://fbref.com/en/comps/9/{year}/defense/{year}-Premier-League-Stats'
    print(f"Requesting URL: {web}")
    
    driver = webdriver.Chrome()
    
    try:
        driver.get(web)
        

        content = driver.page_source
        
    finally:
        driver.quit()

    soup = BeautifulSoup(content, 'lxml')
    
    stats_table = soup.find('div', {'id': 'all_stats_defense'}).find('table')
    
    if not stats_table:
        print("No table found in 'all_stats_defense'")
        return pd.DataFrame()

    rows = stats_table.find('tbody').find_all('tr')
    
    player_name = []
    tackles = []
    tackles_def_3rd = []
    tackles_won = []
    dribblers_tackled = []
    dribbles_challenged =[]
    blocked_shots = []
    blocked_passes = []
    interceptions = []
    clearances = []
    errors = []
    
    for row in rows:
        player_name_element = row.find('td', {'data-stat': 'player'})
        if player_name_element is None or not player_name_element.get_text(strip=True):
            continue  
        tackles_element = row.find('td', {'data-stat': 'tackles'})
        tackles_def_3rd_element = row.find('td', {'data-stat': 'tackles_def_3rd'})
        tackles_won_element = row.find('td', {'data-stat': 'tackles_won'})
        dribblers_tackled_element = row.find('td', {'data-stat': 'challenge_tackles'})
        dribbles_challenged_element = row.find('td', {'data-stat': 'challenges'})
        blocked_shots_element = row.find('td', {'data-stat': 'blocked_shots'})
        blocked_passes_element = row.find('td', {'data-stat': 'blocked_passes'})
        interceptions_element = row.find('td', {'data-stat': 'interceptions'})
        clearances_element = row.find('td', {'data-stat': 'clearances'})
        errors_element = row.find('td', {'data-stat': 'errors'})
        
        player_name1 = clean_stat(safe_get_text(player_name_element))
        tackles1 = clean_stat(safe_get_text(tackles_element))
        tackles_def_3rd1 = clean_stat(safe_get_text(tackles_def_3rd_element))
        tackles_won1 = clean_stat(safe_get_text(tackles_won_element))
        dribblers_tackled1 = clean_stat(safe_get_text(dribblers_tackled_element))
        dribbles_challenged1 = clean_stat(safe_get_text(dribbles_challenged_element))
        blocked_shots1 = clean_stat(safe_get_text(blocked_shots_element))
        blocked_passes1 = clean_stat(safe_get_text(blocked_passes_element))
        interceptions1 = clean_stat(safe_get_text(interceptions_element))
        clearances1 = clean_stat(safe_get_text(clearances_element))
        errors1 = clean_stat(safe_get_text(errors_element))
        
        player_name.append(player_name1)
        tackles.append(tackles1)
        tackles_def_3rd.append(tackles_def_3rd1)
        tackles_won.append(tackles_won1)
        dribblers_tackled.append(dribblers_tackled1)
        dribbles_challenged.append(dribbles_challenged1)
        blocked_shots.append(blocked_shots1)
        blocked_passes.append(blocked_passes1)
        interceptions.append(interceptions1)
        clearances.append(clearances1)
        errors.append(errors1)
        
    if player_name:
        dict_football = {'Player': player_name, 'Tackles': tackles, 'Tackles in Def 3rd': tackles_def_3rd, 'Tackles Won': tackles_won,
                         'Dribblers Tackled': dribblers_tackled, 'Dribbles Challenged': dribbles_challenged,
                         'Blocked Shots': blocked_shots, 'Blocked Passes': blocked_passes,
                         'Interceptions': interceptions, 'Clearances': clearances, 'Errors': errors}
        df_football = pd.DataFrame(dict_football)
        df_football.fillna(0, inplace=True)
        print(f"Data extracted for {year}")
        return df_football
    else:
        print(f"No data extracted for {year}")
        return pd.DataFrame() 
    
def get_possession_stats(year):
    web = f'https://fbref.com/en/comps/9/{year}/possession/{year}-Premier-League-Stats'
    print(f"Requesting URL: {web}")
    
    driver = webdriver.Chrome()
    
    try:
        driver.get(web)
        

        content = driver.page_source
        
    finally:
        driver.quit()

    soup = BeautifulSoup(content, 'lxml')
    
    stats_table = soup.find('div', {'id': 'all_stats_possession'}).find('table')
    
    if not stats_table:
        print("No table found in 'all_stats_possession'")
        return pd.DataFrame()

    rows = stats_table.find('tbody').find_all('tr')
    
    player_name = []
    touches_attacking_third = []
    touches_pen = []
    take_ons_attempted = []
    take_ons_won = []
    carries = []
    carries_into_final_third = []
    carries_into_pen = []
    miscontrols = []
    dispossessed = []
    
    for row in rows:
        player_name_element = row.find('td', {'data-stat': 'player'})
        if player_name_element is None or not player_name_element.get_text(strip=True):
            continue  
        touches_attacking_third_element = row.find('td', {'data-stat': 'touches_att_3rd'})
        touches_pen_element = row.find('td', {'data-stat': 'touches_att_pen_area'})
        take_ons_attempted_element = row.find('td', {'data-stat': 'take_ons'})
        take_ons_won_element = row.find('td', {'data-stat': 'take_ons_won'})
        carries_element = row.find('td', {'data-stat': 'carries'})
        carries_into_final_third_element = row.find('td', {'data-stat': 'carries_into_final_third'})
        carries_into_pen_element = row.find('td', {'data-stat': 'carries_into_penalty_area'})
        miscontrols_element = row.find('td', {'data-stat': 'miscontrols'})
        dispossessed_element = row.find('td', {'data-stat': 'dispossessed'})
        
        player_name1 = clean_stat(safe_get_text(player_name_element))
        touches_attacking_third1 = clean_stat(safe_get_text(touches_attacking_third_element))
        touches_pen1 = clean_stat(safe_get_text(touches_pen_element))
        take_ons_attempted1 = clean_stat(safe_get_text(take_ons_attempted_element))
        take_ons_won1 = clean_stat(safe_get_text(take_ons_won_element))
        carries1 = clean_stat(safe_get_text(carries_element))
        carries_into_final_third1 = clean_stat(safe_get_text(carries_into_final_third_element))
        carries_into_pen1 = clean_stat(safe_get_text(carries_into_pen_element))
        miscontrols1 = clean_stat(safe_get_text(miscontrols_element))
        dispossessed1 = clean_stat(safe_get_text(dispossessed_element))
        
        player_name.append(player_name1)
        touches_attacking_third.append(touches_attacking_third1)
        touches_pen.append(touches_pen1)
        take_ons_attempted.append(take_ons_attempted1)
        take_ons_won.append(take_ons_won1)
        carries.append(carries1)
        carries_into_final_third.append(carries_into_final_third1)
        carries_into_pen.append(carries_into_pen1)
        miscontrols.append(miscontrols1)
        dispossessed.append(dispossessed1)
        
    if player_name:
        dict_football = {'Player': player_name, 'Touches in Attacking Third': touches_attacking_third, 
                         'Touches in Pen Area': touches_pen, 'Take Ons Attempted': take_ons_attempted,
                         'Take Ons Won': take_ons_won, 'Carries': carries,
                         'Carries into Final Third': carries_into_final_third, 'Carries into Penalty Area': carries_into_pen,
                         'Miscontrols': miscontrols, 'Dispossessed': dispossessed}
        df_football = pd.DataFrame(dict_football)
        df_football.fillna(0, inplace=True)
        print(f"Data extracted for {year}")
        return df_football
    else:
        print(f"No data extracted for {year}")
        return pd.DataFrame() 
        
        
def get_playingtime_stats(year):
    web = f'https://fbref.com/en/comps/9/{year}/playingtime/{year}-Premier-League-Stats'
    print(f"Requesting URL: {web}")
    
    driver = webdriver.Chrome()
    
    try:
        driver.get(web)
        

        content = driver.page_source
        
    finally:
        driver.quit()

    soup = BeautifulSoup(content, 'lxml')
    
    stats_table = soup.find('div', {'id': 'all_stats_playing_time'}).find('table')
    
    if not stats_table:
        print("No table found in 'all_stats_playing_time'")
        return pd.DataFrame()

    rows = stats_table.find('tbody').find_all('tr')
    
    player_name = []
    ppm = []
    onG = []
    onGA = []
    onxG = []
    onxGA = []
    on_off_per_90 = []
    on_off_xG_per_90 = []
    
    for row in rows:
        player_name_element = row.find('td', {'data-stat': 'player'})
        if player_name_element is None or not player_name_element.get_text(strip=True):
            continue  
        ppm_element = row.find('td', {'data-stat': 'points_per_game'})
        onG_element = row.find('td', {'data-stat': 'on_goals_for'})
        onGA_element = row.find('td', {'data-stat': 'on_goals_against'})
        onxG_element = row.find('td', {'data-stat': 'on_xg_for'})
        onxGA_element = row.find('td', {'data-stat': 'on_xg_against'})
        on_off_per_90_element = row.find('td', {'data-stat': 'plus_minus_wowy'})
        on_off_xG_per_90_element = row.find('td', {'data-stat': 'xg_plus_minus_wowy'})
        
        player_name1 = clean_stat(safe_get_text(player_name_element))
        ppm1 = clean_stat(safe_get_text(ppm_element))
        onG1 = clean_stat(safe_get_text(onG_element))
        onGA1 = clean_stat(safe_get_text(onGA_element))
        onxG1 = clean_stat(safe_get_text(onxG_element))
        onxGA1 = clean_stat(safe_get_text(onxGA_element))
        on_off_per_901 = clean_stat(safe_get_text(on_off_per_90_element))
        on_off_xG_per_901 = clean_stat(safe_get_text(on_off_xG_per_90_element))
        
        player_name.append(player_name1)
        ppm.append(ppm1)
        onG.append(onG1)
        onGA.append(onGA1)
        onxG.append(onxG1)
        onxGA.append(onxGA1)
        on_off_per_90.append(on_off_per_901)
        on_off_xG_per_90.append(on_off_xG_per_901)
        
    if player_name:
        dict_football = {'Player': player_name, 'Points Per Match': ppm, 'Goals whilst on Pitch': onG,
                         'Goals Conceded whilst on Pitch': onGA, 'xG whilst on Pitch': onxG,
                         'xG Conceded whilst on Pitch': onxGA, 'Net Goals On or Off Pitch per 90': on_off_per_90,
                         'Net xG On or Off Pitch per 90': on_off_xG_per_90}
        df_football = pd.DataFrame(dict_football)
        df_football.fillna(0, inplace=True)
        print(f"Data extracted for {year}")
        return df_football
    else:
        print(f"No data extracted for {year}")
        return pd.DataFrame() 
        
        
def get_misc_stats(year):
    web = f'https://fbref.com/en/comps/9/{year}/misc/{year}-Premier-League-Stats'
    print(f"Requesting URL: {web}")
    
    driver = webdriver.Chrome()
    
    try:
        driver.get(web)
        

        content = driver.page_source
        
    finally:
        driver.quit()

    soup = BeautifulSoup(content, 'lxml')
    
    stats_table = soup.find('div', {'id': 'all_stats_misc'}).find('table')
    
    if not stats_table:
        print("No table found in 'all_stats_misc'")
        return pd.DataFrame()

    rows = stats_table.find('tbody').find_all('tr')
    
    player_name = []
    fouls_comitted = []
    fouls_drawn = []
    offsides = []
    pens_won = []
    pens_conceded = []
    own_goals = []
    recoveries = []
    aerials_won = []
    aerials_lost = []
    
    for row in rows:
        player_name_element = row.find('td', {'data-stat': 'player'})
        if player_name_element is None or not player_name_element.get_text(strip=True):
            continue  
        fouls_comitted_element = row.find('td', {'data-stat': 'fouls'})
        fouls_drawn_element = row.find('td', {'data-stat': 'fouled'})
        offsides_element = row.find('td', {'data-stat': 'offsides'})
        pens_won_element = row.find('td', {'data-stat': 'pens_won'})
        pens_conceded_element = row.find('td', {'data-stat': 'pens_conceded'})
        own_goals_element = row.find('td', {'data-stat': 'own_goals'})
        recoveries_element = row.find('td', {'data-stat': 'ball_recoveries'})
        aerials_won_element = row.find('td', {'data-stat': 'aerials_won'})
        aerials_lost_element = row.find('td', {'data-stat': 'aerials_lost'})
    
        player_name1 = clean_stat(safe_get_text(player_name_element))
        fouls_comitted1 = clean_stat(safe_get_text(fouls_comitted_element))
        fouls_drawn1 = clean_stat(safe_get_text(fouls_drawn_element))
        offsides1 = clean_stat(safe_get_text(offsides_element))
        pens_won1 = clean_stat(safe_get_text(pens_won_element))
        pens_conceded1 = clean_stat(safe_get_text(pens_conceded_element))
        own_goals1 = clean_stat(safe_get_text(own_goals_element))
        recoveries1 = clean_stat(safe_get_text(recoveries_element))
        aerials_won1 = clean_stat(safe_get_text(aerials_won_element))
        aerials_lost1 = clean_stat(safe_get_text(aerials_lost_element))
        
        player_name.append(player_name1)
        fouls_comitted.append(fouls_comitted1)
        fouls_drawn.append(fouls_drawn1)
        offsides.append(offsides1)
        pens_won.append(pens_won1)
        pens_conceded.append(pens_conceded1)
        own_goals.append(own_goals1)
        recoveries.append(recoveries1)
        aerials_won.append(aerials_won1)
        aerials_lost.append(aerials_lost1)
        
    if player_name:
        dict_football = {'Player': player_name, 'Fouls Comitted': fouls_comitted, 'Fouls Drawn': fouls_drawn,
                         'Offsides': offsides, 'Penalties Won': pens_won,
                         'Penalties Conceded': pens_conceded, 'Own Goals': own_goals, 'Recoveries': recoveries,
                         'Aerial Duels Won': aerials_won, 'Aerial Duels Lost': aerials_lost}
        df_football = pd.DataFrame(dict_football)
        df_football.fillna(0, inplace=True)
        print(f"Data extracted for {year}")
        return df_football
    else:
        print(f"No data extracted for {year}")
        return pd.DataFrame() 

# These are players who moved team after playing for another team initially,
# thus giving them two different player profiles, so I ignore them if they
# appear as having played for the team that they started at
players_to_ignore = 'James Ward-Prowse', 'Joachim Andersen', 'Jordan Ayew', 'Odsonne Édouard', 'Reiss Nelson'
teams_to_ignore = 'Crystal Palace', 'West Ham', 'Arsenal'

all_data = []  # List to store combined data for each year

for year in years:
    # Collect data from each function for the current year
    standard_stats = get_standard_stats(year)
    shooting_stats = get_shooting_stats(year)
    passing_stats = get_passing_stats(year)
    gca_stats = get_gca_stats(year)
    defence_stats = get_defence_stats(year)
    possession_stats = get_possession_stats(year)
    playingtime_stats = get_playingtime_stats(year)
    misc_stats = get_misc_stats(year)
    
    # Filter out players who are in the 'players_to_ignore' list and played for teams in 'teams_to_ignore'
    standard_stats = standard_stats[~((standard_stats['Player'].isin(players_to_ignore)) & 
                                      (standard_stats['Team'].isin(teams_to_ignore)))]

    
    # Sort and drop duplicates in the main 'standard_stats' DataFrame
    base_df = standard_stats
    # Merge other datasets after deduplication
    for df in [shooting_stats, passing_stats, gca_stats, defence_stats, possession_stats, playingtime_stats, misc_stats]:
        base_df = base_df.merge(df, on='Player', how='left')  # Merge without introducing new duplicates
    
    # Fill NaN values with zeros
    base_df.fillna(0, inplace=True)
    base_df['year'] = year



        
    # Add the year's combined DataFrame to the list
    all_data.append(base_df)
    
    # Delay to avoid rate limiting
    time.sleep(5)


# After collecting and merging data for all years
if all_data:
    # Concatenate all yearly DataFrames into one
    df_final_combined = pd.concat(all_data, ignore_index=True)
    
    # Sort the DataFrame by 'Player' and 'Minutes' (descending order)
    df_final_sorted = df_final_combined.sort_values(by=['Player', 'Minutes'], ascending=[True, False])
    
    # Keep only the last row for each player (based on most recent/maximum 'Minutes')
    df_final_sorted = df_final_sorted.drop_duplicates(subset='Player', keep='last')
    
    # Reset index after removing duplicates
    df_final_sorted.reset_index(drop=True, inplace=True)
    
    # Save the final combined DataFrame to a CSV
    df_final_sorted.to_csv('all_player_stats_24-25.csv', index=False)
    print("CSV file created successfully")
else:
    print("No data available to save.")

    
    
    
    
    
    
    
        
        
        
        
        
        