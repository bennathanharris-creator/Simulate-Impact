# Simulating Impact — A New Look At Rating Footballers' Performance

## Project Overview
This project applies data analysis and data science techniques to data taken from the 2024-25 English Premier League season to create a rating system, called 'Impact'. I have utilised two separate models in order to compare the ways in which they rate performances, and to find the best way of quantifying Impact.

In this project, I solely used Python to extract, clean and explore the data and to answer questions such as:

- What **statistics are most impactful** to a game of football?
- How **important are the "hidden" statistics** (such as key passes or blocks)?
- Is it possible to **unearth overlooked players** based on their Impact?
- What are the **best techniques and models** to define Impact?

---

## Data & Cleaning
The dataset was extracted completely from FBREF, at the URL of 'https://fbref.com/en/comps/9/2024-2025/stats/2024-2025-Premier-League-Stats', where there are many statistics for every player in the Premier League going throughout the entire season. 
In order to extract the data, I used Selenium because I was initially facing the problem of being kicked off the website for accessing too much data all at once, which Selenium helped solve. I then would access the html and extract the data directly from there. 
I faced many problems extracting this data because there are multiple tables for all of the different statistics, and in order to extract the data I was initially trying to take the data from the table, as I had done before, which worked fine for the 'standard stats' but not any of the other tables of stats. I tried using a switcher within my code which would switch the table on the website automatically and would then extract the data but this also did not work.
What I ended up doing was creating different functions to extract the data from each separate table, by calling the different URLs for each table and then accessing the html and extracting the data from inside the html code.
There were a few players who had moved to a different club within the Premier League after having already played part of the season with one club, and thus resulted in this player having two different rows, which I didn't like and so I removed these players' time from the club that they had played less for from the dataset.
I then merged all of data together, making sure that the year(or season) were the same and merged on the player column to avoid any duplicate columns being created.

In order to clean the data once it had been extracted, I removed any commas from inside the numerical values and turned them into floats. I then wanted to normalise them, so I could have every statistic being in 90 minute increments. This way there is no room for bias for players who were on the pitch for shorter or longer periods of time, and we can see simply the average performance of a player within the 90 minutes a game of football is played.
I also created a few new columns such as 'Shots on Target Missed Goal' which is just the number of shots on target minus the number of goals a player scores. This means we can see more clearly the finishing ability of the player. For example, rather than have a player who scores 10 goals yet takes 100 shots on target to score said goals look excellent, and a player who scores 3 goals with 3 shots on target look poor, we can more fairly and accurately rate their abilities.

A final  little alteration  I made in the model was to filter purely for players who had played a minimum of 500 minutes in the Premier League, because I found when I filtered for players who had played at least 90 minutes I was getting a lot of players who had played maybe 100-300 minutes coming off the bench in the last few minutes of games and had been on the pitch for a lot of impactful moments, which skewed their stats and so I wanted to remove these players.

This same project could be repeated for any league or competition that FBREF has statistics for by simply changing the URL in my 'Get_all_stats.py' file.

---

## Tools
**Python**(using Spyder): Selenium, BeautifulSoup, pandas, time, sci-kit learn, xgboost

## Models
I created two separate models for this project, in order to compare and evaluate the different ways in which they could create the Impact rating, but also because each model offers a different strength. The first model I created, 'Simulate_Impact.py', has the strength of being completely personalisable. It is a very simple model; it takes every statistic that FBREF offers and puts them into three different categories: attack, defence and miscellaneous. From there I can choose exactly how I want each statistic to be used in the Impact rating, by adding multipliers to each one, based on my own personal experience of watching and playing football and how significant I deem the statistic to be. 
Another big positive for this model is that the defensive impact can be positively quantified, because there are plenty of positive defensive statistics, such as tackles won and clearances among others. These can be added up and the negative defensive statistics can be subtracted from this to get the definitive defensive impact, which will be positive for many strong defensive players. 
The split of attack and defence statistics means I can also see specifically how players are performing in both areas of the game, with miscellaneous comprising of the statistics that do not fit into attack or defence, but are still important to a player's performance.

The second model, 'Simulate_Impact_ML.py', is similar to the first model in the sense that it has three separate ratings contributing to an overall total Impact rating: attack, defence and miscellaneous. It also uses the exact same method to find the miscellaneous impact. The key differences are that this model uses machine-learning to find the optimal rating of attack and defence for each player.
