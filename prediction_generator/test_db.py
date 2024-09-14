import xgboost as xgb
import database
import numpy as np
import pandas as pd
import pickle
from tensorflow.keras.models import load_model
import pandas as pd
import json
from bs4 import BeautifulSoup
import regex as re
from tabulate import tabulate
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import time


# Load the saved model


def update_dfs():
       

        driver = webdriver.Chrome()
        url = 'https://stats.wnba.com/players/boxscores-advanced/'
        driver.get(url)
        driver1 = webdriver.Chrome()
        url = 'https://stats.wnba.com/players/boxscores-scoring/'
        driver1.get(url)

        driver2 = webdriver.Chrome()
        url = 'https://stats.wnba.com/players/boxscores-traditional/'
        driver2.get(url)

        driver3 = webdriver.Chrome()
        url = 'https://stats.wnba.com/teams/boxscores-advanced/'
        driver3.get(url)


        driver4= webdriver.Chrome()
        url = 'https://stats.wnba.com/teams/boxscores-scoring/'
        driver4.get(url)


        driver5= webdriver.Chrome()
        url = 'https://stats.wnba.com/teams/boxscores-traditional/'
        driver5.get(url)




        input('press enter when all pages are set, advanced,scoring,traditional')


        html_content = driver.page_source


        soup = BeautifulSoup(html_content, 'html.parser')

        # Extract the table row data
        rows = soup.find_all('tr', {'data-ng-repeat': True})


        columns = [
        "Player", "Team", "Match Up", "Game Date", "Season", "W/L", "MIN", 
        "OffRtg", "DefRtg", "NetRtg", "AST%", "AST/TO", "AST Ratio", 
        "OREB%", "DREB%", "REB%", "TO Ratio", "eFG%", "TS%", "USG%", 
        "PACE", "PACE/40", "PIE"
        ]

        # Extracting the data
        data = []
        for row in rows:
                cols = row.find_all('td')
                cols = [col.get_text(strip=True) for col in cols]
                data.append(cols)

        # Creating the DataFrame
        df = pd.DataFrame(data, columns=columns)

        html_content = driver1.page_source


        soup = BeautifulSoup(html_content, 'html.parser')

        # Extract the table row data
        rows = soup.find_all('tr', {'data-ng-repeat': True})

        # Define the column names
        columns = [
        "Player", "Team", "Match Up", "Game Date", "Season", "W/L", "MIN", 
        "%FGA 2PT", "%FGA 3PT", "%PTS 2PT", "%PTS 2PT MR", "%PTS 3PT", 
        "%PTS FBPs", "%PTS FT", "%PTS OffTO", "%PTS PITP", "2FGM %AST", 
        "2FGM %UAST", "3FGM %AST", "3FGM %UAST", "FGM %AST", "FGM %UAST"
        ]
        data = []
        for row in rows:
                cols = row.find_all('td')
                cols = [col.get_text(strip=True) for col in cols]
                data.append(cols)

        # Creating the DataFrame
        tdf = pd.DataFrame(data, columns=columns)

        merged_df = pd.merge(df, tdf, on=['Player', 'Game Date'], suffixes=('', '_duplicate'))

        for col in merged_df.columns:
                if '_duplicate' in col:
                        original_col = col.replace('_duplicate', '')
                        merged_df[original_col] = merged_df[original_col].combine_first(merged_df[col])
                        merged_df.drop(columns=[col], inplace=True)

        html_content = driver2.page_source

        soup = BeautifulSoup(html_content, 'html.parser')

        # Extract the table row data
        rows = soup.find_all('tr', {'data-ng-repeat': True})

        columns = [
        "Player", "Team", "Match Up", "Game Date", "Season", "W/L", "MIN", 
        "PTS", "FGM", "FGA", "FG%", "3PM", "3PA", "3P%", "FTM", "FTA", "FT%", 
        "OREB", "DREB", "REB", "AST", "STL", "BLK", "TOV", "PF", "+/-"
        ]

        # Extracting the data
        data = []
        for row in rows:
                cols = row.find_all('td')
                cols = [col.get_text(strip=True) for col in cols]
                data.append(cols)

        # Creating the DataFrame
        df = pd.DataFrame(data, columns=columns)



        
        merged_df = pd.merge(merged_df, df, on = ['Player', 'Game Date'], suffixes=('', '_duplicate'))

        # Drop duplicate columns
        for col in merged_df.columns:
                if '_duplicate' in col:
                        original_col = col.replace('_duplicate', '')
                        merged_df[original_col] = merged_df[original_col].combine_first(merged_df[col])
                        merged_df.drop(columns=[col], inplace=True)
        player_df = merged_df.drop(columns=['Season']).dropna()


        ###########TEAM##################

        html_content = driver3.page_source


        soup = BeautifulSoup(html_content, 'html.parser')

        # Extract the table row data
        rows = soup.find_all('tr', {'data-ng-repeat': True})


        columns = [
                 "Team", "Match Up", "Game Date", "Season", "W/L", "MIN", 
        "OffRtg", "DefRtg", "NetRtg", "AST%", "AST/TO", "AST Ratio", 
        "OREB%", "DREB%", "REB%", "TOV%", "eFG%", "TS%",
        "PACE", "PACE/40", "PIE"
        ]

        # Extracting the data
        data = []
        for row in rows:
                cols = row.find_all('td')
                cols = [col.get_text(strip=True) for col in cols]
                data.append(cols)

        # Creating the DataFrame
        df = pd.DataFrame(data, columns=columns)

        html_content = driver4.page_source


        soup = BeautifulSoup(html_content, 'html.parser')

        # Extract the table row data
        rows = soup.find_all('tr', {'data-ng-repeat': True})

        # Define the column names
        columns = [
         "Team", "Match Up", "Game Date", "Season", "W/L", "MIN", 
        "%FGA 2PT", "%FGA 3PT", "%PTS 2PT", "%PTS 2PT MR", "%PTS 3PT", 
        "%PTS FBPs", "%PTS FT", "%PTS OffTO", "%PTS PITP", "2FGM %AST", 
        "2FGM %UAST", "3FGM %AST", "3FGM %UAST", "FGM %AST", "FGM %UAST"
        ]
        data = []
        for row in rows:
                cols = row.find_all('td')
                cols = [col.get_text(strip=True) for col in cols]
                data.append(cols)

        # Creating the DataFrame
        tdf = pd.DataFrame(data, columns=columns)

        merged_df = pd.merge(df, tdf, on=['Team', 'Game Date'], suffixes=('', '_duplicate'))

        for col in merged_df.columns:
                if '_duplicate' in col:
                        original_col = col.replace('_duplicate', '')
                        merged_df[original_col] = merged_df[original_col].combine_first(merged_df[col])
                        merged_df.drop(columns=[col], inplace=True)
        html_content = driver5.page_source

        soup = BeautifulSoup(html_content, 'html.parser')

        # Extract the table row data
        rows = soup.find_all('tr', {'data-ng-repeat': True})

        columns = [
        "Team", "Match Up", "Game Date", "Season", "W/L", "MIN", 
        "PTS", "FGM", "FGA", "FG%", "3PM", "3PA", "3P%", "FTM", "FTA", "FT%", 
        "OREB", "DREB", "REB", "AST", "STL", "BLK", "TOV", "PF", "+/-"
        ]

        # Extracting the data
        data = []
        for row in rows:
                cols = row.find_all('td')
                cols = [col.get_text(strip=True) for col in cols]
                data.append(cols)

        # Creating the DataFrame
        df = pd.DataFrame(data, columns=columns)



        
        merged_df = pd.merge(merged_df, df, on = ['Team', 'Game Date'], suffixes=('', '_duplicate'))

        # Drop duplicate columns
        for col in merged_df.columns:
                if '_duplicate' in col:
                        original_col = col.replace('_duplicate', '')
                        merged_df[original_col] = merged_df[original_col].combine_first(merged_df[col])
                        merged_df.drop(columns=[col], inplace=True)

                        
        return player_df ,merged_df.drop(columns=['Season']).dropna() 
player_df,teams_df= update_dfs()
db = database.Database()

player_df, team_stat_df, pos_team_df = db.get_updates(player_df,teams_df,'2024-09-13') #up to date
db.allinsert_stats(player_df,team_stat_df, pos_team_df)

