# Simulating Impact — A New Look At Rating Footballers' Performance

## Project Overview
This project applies data analysis and data science techniques to data taken from the 2024-25 English Premier League season to create a rating system, called 'Impact'. I have utilised two separate models in order to compare the ways in which they rate performances, and to find the best way of quantifying Impact.

In this project, I solely used Python to extract, clean and explore the data and to answer questions such as:

- What **statistics are most impactful** to a game of football?
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
I created two separate models for this project, in order to compare and evaluate the different ways in which they could create the Impact rating, but also because each model offers a different strength. The first model I created, 'Simulate_Impact.py' (Model 1), has the strength of being completely personalisable. It is a very simple model; it takes every statistic that FBREF offers and puts them into three different categories: attack, defence and miscellaneous. From there I can choose exactly how I want each statistic to be used in the Impact rating, by adding multipliers to each one, based on my own personal experience of watching and playing football and how significant I deem the statistic to be. 
Another big positive for this model is that the defensive impact can be positively quantified, because there are plenty of positive defensive statistics, such as tackles won and clearances among others. These can be added up and the negative defensive statistics can be subtracted from this to get the definitive defensive impact, which will be positive for many strong defensive players. 
The split of attack and defence statistics means I can also see specifically how players are performing in both areas of the game, with miscellaneous comprising of the statistics that do not fit into attack or defence, but are still important to a player's performance.

The second model, 'Simulate_Impact_ML.py' (Model 2), is similar to the first model in the sense that it has three separate ratings contributing to an overall total Impact rating: attack, defence and miscellaneous. It also uses the exact same method to find the miscellaneous impact. The key differences are that this model uses machine-learning to find the optimal rating of attack and defence for each player. This is a big pro compared to the first model, especially for the attack, as it is much more accurate at finding the impact a player has on the attack. It is obvious that a player who has a higher number of team goals when on the pitch compared to goals scored when not on the pitch has a higher attacking impact, but defenders and goalkeepers who are usually on the pitch when goals are scored, even when they play no part in the goals being scored. Because of this I added goals and assists to the attacking target, which worked well in giving a more accurate attacking Impact score, although players like Alisson and Van Dijk still scored highly for attacking Impact as a goalkeeper and defender, respectively.
The defensive Impact target was determined by the goals and xG conceded whilst on pitch and the number of tackles made. This number will almost always be a negative since the goals and xG conceded whilst on pitch are both negative statistics, and so the players with the closest to zero, or any players with a slight positive score, are likely the best defensive players. However, this was a much harder thing to quantify than attack, because a good defender plays a lot of their game without any statistics. For example, the positioning and presence that Van Dijk has is often enough to put an attacker off, which is a huge part of his defensive game that cannot be quantified.
Both the attacking and defensive targets are modelled using only attacking or defensive stats, respectively.

## Results
Taking a look at the Attacking Impact ratings in both Attacking_Impact_24-25.csv (Model 1) and Attacking_Impact_ML_24-25.csv (Model 2) we see the top player is Mohamed Salah, who was chosen the best player of the season, scoring the most goals and giving the most assists. 

Here are the top 20 from Model 1:
- Mohamed Salah, Liverpool - 9.36 
- Bukayo Saka, Arsenal - 8.58 
- James Maddison, Tottenham - 7.95 
- Jeremy Doku, Manchester City - 7.88 
- Brajan Gruda, Brighton - 7.87 
- Ryan Sessegnon, Fulham - 7.75 
- Amad Diallo, Manchester Utd - 7.3 
- Dwight McNeil, Everton - 7.25 
- Son Heung-min, Tottenham - 6.79 
- Kevin De Bruyne, Manchester City - 6.74 
- Luis Díaz, Liverpool - 6.64 
- Sávio, Manchester City - 6.63 
- Jacob Murphy, Newcastle Utd - 6.58 
- Bryan Mbeumo, Brentford - 6.45 
- Jack Grealish, Manchester City - 6.36 
- Martin Ødegaard, Arsenal - 6.25 
- João Pedro, Brighton - 6.17 
- Cole Palmer, Chelsea - 6.11
- Justin Kluivert, Bournemouth - 6.09
- Bruno Fernandes, Manchester Utd - 6.02 

And here are the top 20 from Model 2: 
- Mohamed Salah, Liverpool - 8.55
- Luis Díaz, Liverpool - 8.21 
- Trent Alexander-Arnold, Liverpool - 7.68 
- Diogo Jota, Liverpool - 7.55 
- Darwin Núñez, Liverpool - 7.52 
- Alexis Mac Allister, Liverpool - 7.44 
- Cody Gakpo, Liverpool - 7.27 
- Alexander Isak, Newcastle Utd - 7.15 
- Rodrigo Muniz, Fulham - 7.12 
- Dominik Szoboszlai, Liverpool - 7.11 
- Michael Kayode, Brentford - 7.04 
- Jacob Murphy, Newcastle Utd - 7.01 
- Riccardo Calafiori, Arsenal - 6.94 
- Bukayo Saka, Arsenal - 6.93 
- Adam Webster, Brighton - 6.85 
- Jeremy Doku, Manchester City - 6.81 
- Virgil van Dijk, Liverpool - 6.79 
- Alisson, Liverpool - 6.78 
- Ryan Gravenberch, Liverpool - 6.77 
- Ryan Sessegnon, Fulham - 6.59 

Comparing these two top 20 lists we see the number of Liverpool players in Model 2 is significantly larger than in Model 1, at 11 to 2. This is because Liverpool were the best attacking team and the method used to find the attacking Impact in Model 2 gives more weight to players who were a part of a strong attacking team rather than players who were strong attackers individually. There are 5 players who appear in both lists: Mohamed Salah, Bukayo Saka, Luis Diaz, Jeremy Doku, and Ryan Sessegnon. Out of these 5, 4 are well-renowned forwards with high pedigree. Ryan Sessegnon is not usually considered to be in the top attacking talent in the Premier League, however, often playing as a full back. He was a highly touted young player but did not quite reach the level expected of him, until 2024-25 apparently. Whilst he did not score or assist loads of goals (4 goals and 2 assists in 16 games), he was clearly on the pitch when Fulham were playing better, and was off the pitch when Fulham were playing worse, and so we can deduce he had a major impact on the team. Sessegnon was a top player in the 2024-25 season when looking more closely at his stats on Fotmob: he was in the top 4% for goals per 90 with 0.62, and the top 17% for assists per 90 with 0.31, and performed very well all round in an attacking sense. I think this shows that players with a lot of impact can be unearthed using these models, especially when utilised together and cross-examined, especially using an outside source like Fotmob to verify. 

There are a few more names in which I would take a closer look at, as they are not so well known for their attacking prowess as some others on these lists: Brajan Gruda, Michael Kayode, Adam Webster. Gruda is a forward player, although did not have a tremendous 2024-25 season, with 1 goal and 4 assists in 21 games. This means he was performing fairly strongly in many other attacking aspects however, whilst his output was not necessarily strong enough. Using stats from Fotmob, I can see he is excellent at dribbling, crossing and chance creation, having some of the highest in each of these stats per 90 in the league, along with being in the top 2% for assists per 90 at 0.53. I believe this should earn him more game time as he averaged 32 minutes per game, and usually coming on as a substitute, only starting 8 of the 21 games he played.
Michael Kayode is a defender, a right back specifically, and so his attacking Impact is surprisingly high, although since he scores highly in Model 2 it may mean that he simply happened to be on the pitch a lot of the time that Brentford scored. Let us take a look at his attacking performance: again Kayode is excellent at dribbling, crossing, and chance creation, whilst also being in the top 17% for assists per 90 at 0.17. He also has good long ball accuracy and touches in the opposition box, as does Gruda, so we are seeing similarities in players here. Neither player scores highly in terms of goal output and shooting and neither player is an excellent passer of the ball, but they both are well equipped to run down the line, beat the defenders and put a good cross into the box, and create chances while they're at it.
Now Adam Webster is a centre back, usually the least attacking players of the outfield 10, yet he has managed to get into the top 20 in Model 2. Again the reason could be he was simply on the pitch when Brighton scored a lot of goals, but let us see. Webster has a good passing ability, having a high success rate and accuracy, especially for long passes forward. He also has a good number of shots per 90, chances created and touches in the opposition box. Clearly he is a different type of player to Gruda and Kayode, who are wide players who like to run down the line and create chances that way, Webster seems to be creating chances with his long range of passing, and his ability in the box, which must come from corners and free kicks. This is important to know as Webster clearly possesses strong attacking presence when in the box, and could be used by to scout centre backs who are good at converting set plays.

Now looking at Defensive Impact we have from Model 1:
- Casemiro, Manchester Utd - 6.84
- Michael Kayode, Brentford - 4.56 
- Neco Williams, Nott'ham Forest - 4.31 
- Patrick Dorgu, Manchester Utd - ,4.02 
- Cristian Romero, Tottenham - 4.0 
- Riccardo Calafiori, Arsenal - 3.91 
- James Tarkowski, Everton - 3.91 
- Idrissa Gana Gueye, Everton - 3.86 
- Oliver Scarles, West Ham - 3.61 
- Kenny Tete, Fulham - 3.54 
- Alexis Mac Allister, Liverpool - 3.53 
- Kostas Tsimikas, Liverpool - 3.49 
- Mats Wieffer, Brighton - 3.47 
- Marcos Senesi, Bournemouth - 3.37 
- Elliot Anderson, Nott'ham Forest - 3.29 
- Noussair Mazraoui, Manchester Utd - 3.26 
- Alex Scott, Bournemouth - 3.23 
- Daniel Muñoz, Crystal Palace - 3.23 
- Trent Alexander-Arnold, Liverpool - 3.14 
- Tyler Adams, Bournemouth - 3.14

And from Model 2 we have:
- Casemiro, Manchester Utd - 0.62 
- Kostas Tsimikas, Liverpool - 0.48 
- Alexis Mac Allister, Liverpool - 0.47 
- Trent Alexander-Arnold, Liverpool - 0.19 
- Idrissa Gana Gueye, Everton - 0.04 
- Michael Kayode, Brentford - (-0.14)
- Jesper Lindstrøm, Everton - (-0.26)
- Jurriën Timber, Arsenal - (-0.28)
- Ethan Nwaneri, Arsenal - (-0.38)
- Riccardo Calafiori, Arsenal - (-0.46)
- Daniel Muñoz, Crystal Palace - (-0.49)
- Jeremy Doku, Manchester City - (-0.58)
- Moisés Caicedo, Chelsea - (-0.58)
- Neco Williams, Nott'ham Forest - (-0.61)
- James Garner, Everton - (-0.62)
- Tyler Adams, Bournemouth - (-0.62)
- Diego Gómez, Brighton - (-0.65)
- Alex Scott, Bournemouth - (-0.71)
- Oliver Scarles, West Ham - (-0.79)
- Oleksandr Zinchenko, Arsenal - (-0.83)

Here we can see 12 of the same players appearing in both top 20 lists. This means that the models are both returning pretty accurate ratings for strong defensive players. Of course many of the best defenders, such as Van Dijk and Saliba, do not appear. These lists seem to reward defensive midfielders and full backs more for their defensive duties. I think this is often because these players are the protective layer in front of centre backs, so they usually have more tackles and defensive contributions even if they aren't necessarily as strong defensively as the centre backs.

Many of these players are well knwon for being good players and sound defensively, but none of these players are talked about the best defensively minded players in the Premier League, so I do think that this is a good way of seeing exactly what the data says about defensive ability. I do think I would need to create a different rating system for centre backs and also goalkeepers. Of course there are players like Van Dijk and Saliba who are excellent, but for looking at defensive actions from players who are not centre backs, I think this is an excellent way of weeding out players who are not so well known for being strong defensively.

There are a few names that appeared in both the attacking and defensive Impact top 20s, so let us see what the full lists of Total Impact look like. Here is Model 1:
Player, Team, Attacking Impact, Defensive Impact, Misc Impact, Total Impact
- Casemiro, Manchester Utd, 1.85,6.84, 0.74, 9.43
- Trent Alexander-Arnold, Liverpool, 4.7, 3.14, 1.24, 9.08
- Alexis Mac Allister, Liverpool, 5.07, 3.53, 0.24, 8.84
- Kostas Tsimikas, Liverpool, 3.73, 3.49, 1.26, 8.48
- Kieran Trippier, Newcastle Utd, 4.73, 2.02, 1.63, 8.38
- Bukayo Saka, Arsenal, 8.58, -0.42, 0.2, 8.36
- Jeremy Doku, Manchester City, 7.88, 0.63, -0.35, 8.16
- Michael Kayode, Brentford, 4.13, 4.56, -0.53, 8.16
- Mats Wieffer, Brighton, 4.75, 3.47, -0.11, 8.11
- Ryan Sessegnon, Fulham, 7.75, 1.64, -1.81, 7.58
- Cristian Romero, Tottenham, 1.27, 4.0, 2.29, 7.56
- James Maddison, Tottenham, 7.95, -2.04, 1.49, 7.4
- Bruno Fernandes, Manchester Utd, 6.02, 0.37, 0.96, 7.35
- Amad Diallo, Manchester Utd, 7.3, 0.01, -0.06, 7.25
- Antonee Robinson, Fulham, 3.93, 2.83, 0.47, 7.23
- Lewis Hall, Newcastle Utd, 3.36, 2.6, 1.19, 7.15
- Mohamed Salah, Liverpool, 9.36, -1.85, -0.53, 6.98
- Moisés Caicedo, Chelsea, 2.8, 3.14, 0.96, 6.9
- Pedro Porro, Tottenham, 4.26, 1.59, 0.99, 6.84
- Youri Tielemans, Aston Villa, 4.19, 1.25, 1.27, 6.71

And Model 2: 
Player, Team, Attacking Impact ML, Defensive Impact ML, Misc Impact, Total Impact (ML)
- Trent Alexander-Arnold, Liverpool, 7.68, 0.19, 1.34, 9.21
- Alexis Mac Allister, Liverpool, 7.44, 0.47, 0.34, 8.25
- Virgil van Dijk, Liverpool, 6.79, -2.2, 2.57, 7.16
- Kostas Tsimikas, Liverpool, 5.3, 0.48, 1.37, 7.15
- Ibrahima Konaté, Liverpool, 6.35, -1.56, 2.07, 6.86
- Mateo Kovačić, Manchester City, 6.34, -1.29, 1.72, 6.77
- William Saliba, Arsenal, 5.26, -0.89, 2.24, 6.61
- Luis Díaz, Liverpool, 8.21, -1.15, -0.51, 6.55
- Michael Kayode, Brentford, 7.04, -0.14, -0.36, 6.54
- Riccardo Calafiori, Arsenal, 6.94, -0.46, 0.05, 6.53
- Rúben Dias, Manchester City, 5.71, -2.33, 2.99, 6.37
- Tosin Adarabioyo, Chelsea, 5.82, -1.96, 2.5, 6.36
- Kieran Trippier, Newcastle Utd, 6.06, -1.44, 1.67, 6.29
- Cristian Romero, Tottenham, 5.8, -1.99, 2.38, 6.19
- Ryan Gravenberch, Liverpool, 6.77, -1.42, 0.82, 6.17
- Joe Gomez, Liverpool, 5.65, -1.92, 2.24, 5.97
- Joško Gvardiol, Manchester City, 5.83, -1.91, 2.02, 5.94
- Adam Webster, Brighton, 6.85, -2.94, 2.03, 5.94
- Jeremy Doku, Manchester City, 6.81, -0.58, -0.32, 5.91
- Moisés Caicedo, Chelsea, 5.31, -0.58, 1.1, 5.83

There are 8 players who appear on both lists, meaning that both lists show many of the best players, while also having room to showcase other abilities in their top 20s. The Model 1 list is, in my opinion, less accurate to the list of best performing players from my point of view compared the list of Model 2. However, Model 2 does not contain Mohamed Salah in the top 20 (he is placed 28th), who won all the accolades there were to win in the 2024-25 season and was widely considered to be the best player in the league with arguable the best ever individual season the Premier League has ever seen. This does mean that Mohamed Salah, whilst being superb going forward, has much to improve upon when looking at his defensive game. His miscellaneous Impact, which is made up of things like yellow and red cards and passing and fouls, could also be improved.

Looking at both lists I would say the player who has certainly come out of this looking the best is Trent Alexander-Arnold. He had a tremendous season and was excellent going forward and also one of the best defensive players. To many he does not have great defensive skills, mainly down to positioning and awareness, which I could not quantify for this rating, but what he has that is quantifiable is excellent, and that deserves praise. He would not have been in the top 10 players for the majority of fans and pundits, but I think when people watch football the attacking players tend to overshadow other players, and I tried to overcome that with this rating system. I want this rating system to shed light on players who have the most impact on a game of football and are the best all round players for their team, and I believe this is what has been achieved when looking at the likes of the players that are getting high ratings. Midfielders, wide players, full backs and wingers, players who can do it all and go up and down the pitch helping in every area of it.

It is also apparent that there is one player who appeared in every list so far but is not widely spoken about: Michael Kayode. I believe I have successfully unearthed a top quality player, and someone who should be being looked at by bigger clubs and should be getting more plaudits and definitely more game time. He has shown quality in every area of the pitch and whenever he plays he delivers impactful performances. 
