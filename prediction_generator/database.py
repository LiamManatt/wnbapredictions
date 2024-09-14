import pandas as pd
import psycopg2
from psycopg2 import sql
import warnings
import pandas as pd

# Suppress the specific warning
warnings.filterwarnings("ignore", category=UserWarning, message="pandas only supports SQLAlchemy")
import json
from bs4 import BeautifulSoup
import regex as re
from tabulate import tabulate
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import time
import numpy as np

class Database:

    def __init__(self, conn =psycopg2.connect(
            dbname="wnbaall",
            user="postgres",
            password="5111",
            host="localhost",
            port="5432")):
        self.conn =conn
    def close_db(self):
        self.conn.close()
    def get_row(self,player,team,opp,home, stats,season=28, close = False):
        conn = self.conn
        final_dct = {'home':home, 'season':season}

        query = f"SELECT pos FROM pos_player WHERE player = '{player}'"

        df = pd.read_sql_query(query, conn)
        pos = df['pos'][0]


        final_dct['position'] = pos


        query = f"SELECT * FROM pos_allowed_lag WHERE pos = '{pos}' and team = '{opp}' ORDER BY games_since asc;"

        # Execute the query and load the data into a DataFrame
        df = pd.read_sql_query(query, conn)

        df = df[['pts','reb','oreb','dreb','fga','ast']]


        df = df.mean(axis=0)


        for col in df.index:
            final_dct[f'avg5_{col}_allowed_opp_pos'] = df[col]

        query = f"SELECT * FROM pos_allowed WHERE pos = '{pos}' and team = '{opp}';"

        # Execute the query and load the data into a DataFrame
        df = pd.read_sql_query(query, conn)

        
        for col in df.columns[3:]:
             final_dct[f'opp_{col}_allowed_pos'] = df[col][0]


        # Define the query
        query = f"SELECT * FROM stat_lag_opp WHERE player = '{player}' and opp = '{opp}'"

        # Execute the query and load the data into a DataFrame
        df = pd.read_sql_query(query, conn)






        for col in df.columns[2:]:
            real = col
            col = col.replace('threea','3pa')
            col = col.replace('threem','3pm')
            col = col.replace('_per_','/')
            col = col.replace('three','3')
            col = col.replace('two','2')
            col = col.replace('plus_minus','+/-')
            col = col.replace('percentage','%')
            final_dct[f'against{col}_lag_1'] = df[real][0]

        query = f"SELECT * FROM stat_lag WHERE player = '{player}' ORDER BY games_since asc;"

        df = pd.read_sql_query(query, conn)

        df = df.drop('player',axis=1)

        for stat in stats:
            pts_df = df[stat]

            for lag in range(5):
                        final_dct[f'{stat}_lag_{lag+1}'] = pts_df[lag]
        df = df.mean(axis=0)
        for col in df.index[1:]:
            real = col
            col = col.replace('threea','3pa')
            col = col.replace('threem','3pm')
            col = col.replace('_per_','/')
            col = col.replace('three','3')
            col = col.replace('two','2')
            col = col.replace('plus_minus','+/-')
            col = col.replace('percentage','%')
            final_dct[f'avg10_{col}_player'] = df[real]

        

        query = f"SELECT * FROM stat_avg_season WHERE player = '{player}';"



        # Execute the query and load the data into a DataFrame
        df = pd.read_sql_query(query, conn)

        for col in df.columns[1:]:
            if 'games' in col:
                continue
            real = col
            col = col.replace('threea','3pa')
            col = col.replace('threem','3pm')
            col = col.replace('_per_','/')
            col = col.replace('three','3')
            col = col.replace('two','2')
            col = col.replace('plus_minus','+/-')
            col = col.replace('percentage','%')
            final_dct[f'player_{col}_for'] = df[real][0]

        query = f"SELECT * FROM team_avg WHERE team = '{team}';"
        # Execute the query and load the data into a DataFrame
        df = pd.read_sql_query(query, conn)

        for col in df.columns[2:]:
            real = col
            col = col.replace('threea','3pa')
            col = col.replace('_per_','/')
            col = col.replace('threem','3pm')
            col = col.replace('_per_','/')
            col = col.replace('three','3')
            col = col.replace('two','2')
            col = col.replace('plus_minus','+/-')
            col = col.replace('percentage','%')
            final_dct[f'{col}_for'] = df[real][0]

        query = f"SELECT * FROM team_avg WHERE team = '{opp}';"
        # Execute the query and load the data into a DataFrame
        df = pd.read_sql_query(query, conn)

        for col in df.columns[2:]:
            real = col
            col = col.replace('threea','3pa')
            col = col.replace('threem','3pm')
            col = col.replace('_per_','/')
            col = col.replace('three','3')
            col = col.replace('two','2')
            col = col.replace('plus_minus','+/-')
            col = col.replace('percentage','%')
            final_dct[f'opp_{col}_for'] = df[real][0]


        query = f"SELECT * FROM team_allowed_avg WHERE team = '{team}';"
        # Execute the query and load the data into a DataFrame
        df = pd.read_sql_query(query, conn)



        for col in df.columns[2:]:
            real = col
            col = col.replace('threea','3pa')
            col = col.replace('threem','3pm')
            col = col.replace('_per_','/')
            col = col.replace('three','3')
            col = col.replace('two','2')
            col = col.replace('plus_minus','+/-')
            col = col.replace('percentage','%')
            final_dct[f'team_{col}_allowed'] = df[real]


        query = f"SELECT * FROM team_allowed_avg WHERE team = '{opp}';"
        # Execute the query and load the data into a DataFrame
        df = pd.read_sql_query(query, conn)

        for col in df.columns[2:]:
            real = col
            col = col.replace('threea','3pa')
            col = col.replace('threem','3pm')
            col = col.replace('_per_','/')
            col =col.replace('three','3')
            col = col.replace('two','2')
            col =col.replace('plus_minus','+/-')
            col = col.replace('percentage','%')
            final_dct[f'opp_{col}_allowed'] = df[real][0]

        
        query = f"SELECT * FROM team_allowed_lag WHERE team = '{team}' ORDER BY games_since asc;"
        # Execute the query and load the data into a DataFrame
        df = pd.read_sql_query(query, conn)

        df = df.drop('team',axis=1)


        df= df.mean(axis=0)
    


        for col in df.index[1:]:
            real = col
            col = col.replace('threea','3pa')
            col = col.replace('threem','3pm')
            col = col.replace('three','3')
            col = col.replace('_per_','/')
            col = col.replace('two','2')
            col = col.replace('plus_minus','+/-')
            col = col.replace('percentage','%')
            final_dct[f'avg5_{col}_allowed_team'] = df[real]

        query = f"SELECT * FROM team_allowed_lag WHERE team = '{opp}' ORDER BY games_since asc;"
        # Execute the query and load the data into a DataFrame
        df = pd.read_sql_query(query, conn)
        df = df.drop('team',axis=1)
        df= df.mean(axis=0)



        for col in df.index[1:]:
            real = col
            col = col.replace('threea','3pa')
            col = col.replace('threem','3pm')
            col = col.replace('three','3')
            col = col.replace('_per_','/')
            col = col.replace('two','2')
            col = col.replace('plus_minus','+/-')
            col = col.replace('percentage','%')
            final_dct[f'avg5_{col}_allowed_opp'] = df[real]



        query = f"SELECT * FROM team_for_lag WHERE team = '{team}' ORDER BY games_since asc;"
        # Execute the query and load the data into a DataFrame
        df = pd.read_sql_query(query, conn)

        df = df.drop('team',axis=1)

        df= df.mean(axis=0)
    


        for col in df.index[1:]:
            real = col
            col = col.replace('threea','3pa')
            col = col.replace('threem','3pm')
            col = col.replace('three','3')
            col = col.replace('_per_','/')
            col = col.replace('two','2')
            col = col.replace('plus_minus','+/-')
            col = col.replace('percentage','%')
            final_dct[f'avg5_{col}_for_team'] = df[real]

        query = f"SELECT * FROM team_for_lag WHERE team = '{opp}' ORDER BY games_since asc;"
        # Execute the query and load the data into a DataFrame
        df = pd.read_sql_query(query, conn)
        df = df.drop('team',axis=1)

        df= df.mean(axis=0)
    


        for col in df.index[1:]:
            real = col
            col = col.replace('threea','3pa')
            col = col.replace('threem','3pm')
            col = col.replace('three','3')
            col = col.replace('_per_','/')
            col = col.replace('two','2')
            col = col.replace('plus_minus','+/-')
            col = col.replace('percentage','%')
            final_dct[f'avg5_{col}_for_opp'] = df[real]
        


        query = f"SELECT * FROM matchup WHERE team = '{team}' and opp = '{opp}' ORDER BY games_since asc;"

        # Execute the query and load the data into a DataFrame
        df = pd.read_sql_query(query, conn)

        stat_df = df[stats]

        for stat in stats:
            for i in range(4):
                    final_dct[f'team_{stat}_against_lag_'+str(i+1)] = stat_df[stat][i]
        for col in df.columns[3:]:
            real = col
            col = col.replace('threea','3pa')
            col = col.replace('threem','3pm')
            col = col.replace('three','3')
            col = col.replace('_per_','/')
            col = col.replace('two','2')
            col = col.replace('plus_minus','+/-')
            col = col.replace('percentage','%')
            final_dct[f'team_avg4_{col}_against'] = (df[real][0] +  df[real][1] + df[real][2] +  df[real][3])/4


     
        

        if close:
            conn.close()
        index = [0]


        return pd.DataFrame(final_dct, index=index)
        

    def realign_df(self, x):
        x.columns = [col.replace(' ','_').lower() for col in x.columns]
        x= x[sorted(x.columns)]
        return x
    
    def opp(self, df):
        df['opp'] = df['Match Up'].apply(lambda x: x.split()[-1])
        df['home'] = df['Match Up'].apply(lambda x: 1 if '@' not in x.split() else 0)
        return 1


    def get_updates(self, df,team_df, last_date):
        conn = self.conn
        
        df = self.type_maker(df)
        self.opp(df)
        df['Game Date'] = pd.to_datetime(df['Game Date'], format='%m/%d/%Y')
        df['PLAYER'] = df['Player'].str.replace("'",'')
        all_df_att = df.sort_values('Game Date')
        all_df_att['Date'] = all_df_att['Game Date']
        all_df_att.drop(columns=['Game Date','Player'],inplace =True)
        all_df_att = all_df_att[all_df_att['Date']> last_date].dropna()

        player_df = all_df_att



        df = self.type_maker(team_df)
        self.opp(df)
        df['Game Date'] = pd.to_datetime(df['Game Date'], format='%m/%d/%Y')
        all_df_att = df.sort_values('Game Date')
        all_df_att['Date'] = all_df_att['Game Date']
        all_df_att.drop(columns=['Game Date'],inplace =True)
        all_df_att = all_df_att[all_df_att['Date']> last_date].dropna()


        team_stat_df = all_df_att

        query = f"SELECT * FROM pos_player;"

                # Execute the query and load the data into a DataFrame
        zdf = pd.read_sql_query(query, conn)

        zdf['PLAYER'] = zdf['player'].str.replace("'",'')
        zdf.drop(columns=['player'],inplace=True)


        all_df_att = pd.merge(player_df,zdf, how='left', on=['PLAYER'])


        pos_team_df = all_df_att.groupby(['Team', 'opp', 'Date','pos'])[['PTS', 'REB', 'OREB', 'DREB', 'FGA', 'AST']].sum().reset_index()



        return player_df.sort_values('Date'), team_stat_df.sort_values('Date'), pos_team_df.sort_values('Date')

    def type_maker(self, df):
        columns = [
             'OffRtg', 'DefRtg', 'NetRtg', 'AST%', 'AST/TO', 'AST Ratio',
                'OREB%', 'DREB%', 'REB%', 'TO Ratio', 'eFG%', 'TS%', 'USG%', 'PACE', 'PACE/40', 'PIE', '%FGA 2PT',
                '%FGA 3PT', '%PTS 2PT', '%PTS 2PT MR', '%PTS 3PT', '%PTS FBPs', '%PTS FT', '%PTS OffTO', '%PTS PITP',
                '2FGM %AST', '2FGM %UAST', '3FGM %AST', '3FGM %UAST', 'FGM %AST', 'FGM %UAST', 'PTS', 'FGM', 'FGA',
                'FG%', '3PM', '3PA', '3P%', 'FTM', 'FTA', 'FT%', 'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TOV','TOV%',
                'PF', '+/-'
            ]
        
        for col in columns:
            if col in df.columns:  # Check if the column exists in the DataFrame
                if df[col].dtype == 'object':
                    df[col] = df[col].str.replace(',', '')
                try:
                    df[col] = df[col].astype(float)
                except ValueError:
                    print(f"Warning: Column '{col}' contains non-numeric values that could not be converted.")
    
        return df
    
    def rebinsert_stats(self,df,team_df, close = False):
        conn = self.rebconn
        with conn.cursor() as cur:

            for index, row in df.iterrows():

                player = row['PLAYER']

            # Retrieve the current values from the table
                cur.execute(
                    sql.SQL("""
                        SELECT FGA, FGM, ThreeA, ThreeM, FTA, FTM, PTS, REB, OREB, DREB, AST, TOV, PF, STL, BLK, PACE, PACE_per_40, PIE, PercentageFGA_2PT, OREBPercentage, DREBPercentage, REBPercentage, games_played 
                        FROM stat_avg_season 
                        WHERE player = %s
                    """),
                    [player]
                )

                result = cur.fetchone()
                if result:

                    if result:
                        current_fga, current_fgm, current_threea, current_threem, current_fta, current_ftm, current_pts, current_reb, current_oreb, current_dreb, current_ast, current_tov, current_pf, current_stl, current_blk, current_pace, current_pace_per_40, current_pie, current_percentage_fga_2pt, current_oreb_percentage, current_dreb_percentage, current_reb_percentage, games_played = result

                        # Calculate new averages
                        games_played += 1
                        updated_row = [
                            (current_fga * (games_played - 1) + row['FGA']) / games_played,
                            (current_fgm * (games_played - 1) + row['FGM']) / games_played,
                            (current_threea * (games_played - 1) + row['3PA']) / games_played,
                            (current_threem * (games_played - 1) + row['3PM']) / games_played,
                            (current_fta * (games_played - 1) + row['FTA']) / games_played,
                            (current_ftm * (games_played - 1) + row['FTM']) / games_played,
                            (current_pts * (games_played - 1) + row['PTS']) / games_played,
                            (current_reb * (games_played - 1) + row['REB']) / games_played,
                            (current_oreb * (games_played - 1) + row['OREB']) / games_played,
                            (current_dreb * (games_played - 1) + row['DREB']) / games_played,
                            (current_ast * (games_played - 1) + row['AST']) / games_played,
                            (current_tov * (games_played - 1) + row['TOV']) / games_played,
                            (current_pf * (games_played - 1) + row['PF']) / games_played,
                            (current_stl * (games_played - 1) + row['STL']) / games_played,
                            (current_blk * (games_played - 1) + row['BLK']) / games_played,
                            (current_pace * (games_played - 1) + row['PACE']) / games_played,
                            (current_pace_per_40 * (games_played - 1) + row['PACE/40']) / games_played,
                            (current_pie * (games_played - 1) + row['PIE']) / games_played,
                            (current_percentage_fga_2pt * (games_played - 1) + row['%FGA 2PT']) / games_played,
                            (current_oreb_percentage * (games_played - 1) + row['OREB%']) / games_played,
                            (current_dreb_percentage * (games_played - 1) + row['DREB%']) / games_played,
                            (current_reb_percentage * (games_played - 1) + row['REB%']) / games_played,
                            games_played
                        ]


                        # Update the table with the new averages
                        update_query = sql.SQL("""
                            UPDATE stat_avg_season
                            SET FGA = %s, FGM = %s, ThreeA = %s, ThreeM = %s, FTA = %s, FTM = %s, PTS = %s, REB = %s, 
                                OREB = %s, DREB = %s, AST = %s, TOV = %s,  PF = %s, STL = %s, BLK = %s, PACE = %s, PACE_per_40 = %s, 
                                PIE = %s, PercentageFGA_2PT = %s, OREBPercentage = %s, DREBPercentage = %s, REBPercentage = %s, 
                                games_played = %s
                            WHERE player = %s
                        """)
                        
                        cur.execute(update_query, updated_row + [player])
                    
                    player_name = row['PLAYER']
                    opp = row['opp']

                    # Step 2: Find the minimum games_since for the player, if any
                    cur.execute(
                        sql.SQL("SELECT MIN(games_since) FROM stat_lag WHERE player = %s"),
                        [player_name]
                    )
                    
                    min_games_since = cur.fetchone()[0]- 1


                    cur.execute(
                        sql.SQL("DELETE FROM stat_lag WHERE player = %s AND games_since = %s"),
                        [player_name, min_games_since+5]
                    )

                    # Step 4: Insert the new row into the table
                    insert_query = sql.SQL("""
                        INSERT INTO stat_lag (
                            player, games_since, FGA, FGM, ThreeA, ThreeM, FTA, FTM, PTS,PF, REB, OREB, DREB, AST, TOV, STL, BLK, PACE, PACE_per_40, PIE, PercentageFGA_2PT, OREBPercentage, DREBPercentage, REBPercentage
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s,
                                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)
                    """)

                    cur.execute(insert_query, [
                        row['PLAYER'], min_games_since, 
                        row['FGA'], row['FGM'], row['3PA'], row['3PM'], row['FTA'], 
                        row['FTM'], row['PTS'], row['PF'], row['REB'],row['OREB'],row['DREB'], row['AST'], row['TOV'], 
                        row['STL'], row['BLK'], row['PACE'], row['PACE/40'], row['PIE'], 
                        row['%FGA 2PT'], row['OREB%'],row['DREB%'], row['REB%']
                    ])

                    

                    #STAT_LAG_OPP
                    #select * from stat_lag_opp where player = 'Caitlin Clark' and opp = 'dal' and games_since = (SELECT MAX(games_since) FROM stat_lag_opp WHERE player = 'Caitlin Clark' and opp = 'dal');


                    # Step 2: Find the minimum games_since for the player, if any

                    cur.execute(
                        sql.SQL("DELETE FROM stat_lag_opp WHERE player = %s AND opp = %s"),
                        [player_name, opp]
                    )



                    # Step 4: Insert the new row into the table
                    insert_query = sql.SQL("""
                        INSERT INTO stat_lag_opp (
                            player, opp, FGA, FGM, ThreeA, ThreeM, FTA, FTM, PTS,PF, REB, OREB, DREB, AST, TOV, STL, BLK, PACE, PACE_per_40, PIE, PercentageFGA_2PT, OREBPercentage, DREBPercentage, REBPercentage
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s,
                                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)
                    """)

                    cur.execute(insert_query, [
                        row['PLAYER'], opp, 
                        row['FGA'], row['FGM'], row['3PA'], row['3PM'], row['FTA'], 
                        row['FTM'], row['PTS'], row['PF'], row['REB'],row['OREB'],row['DREB'], row['AST'], row['TOV'], 
                        row['STL'], row['BLK'], row['PACE'], row['PACE/40'], row['PIE'], 
                        row['%FGA 2PT'], row['OREB%'],row['DREB%'], row['REB%']
                    ])
            for index,row in team_df.iterrows():
            # Step 1: Find the minimum games_since for the team, if any
            
                team = row['Team']
            
            # Retrieve the current values from the table
                cur.execute(
                    sql.SQL("SELECT games_played, PTS, REB, OREB, DREB, AST, PF, STL, TOV, BLK, FGA, FGM, threeA, threeM, FTA, FTM FROM team_avg WHERE team = %s"),
                    [team]
                )
                
                result = cur.fetchone()
                
                if result:
                    games_played, current_pts, current_reb, current_oreb,current_dreb, current_ast, current_pf, current_stl, current_tov, current_bs, current_fga, current_fgm, current_threea, current_threem, current_fta, current_ftm = result

                    # Calculate new averages
                    games_played += 1
                    updated_row = [
                        (current_pts * (games_played - 1) + row['PTS']) / games_played,
                        (current_reb * (games_played - 1) + row['REB']) / games_played,
                        (current_oreb * (games_played - 1) + row['OREB']) / games_played,
                        (current_dreb * (games_played - 1) + row['DREB']) / games_played,
                        (current_ast * (games_played - 1) + row['AST']) / games_played,
                        (current_pf * (games_played - 1) + row['PF']) / games_played,
                        (current_stl * (games_played - 1) + row['STL']) / games_played,
                        (current_tov * (games_played - 1) + row['TOV']) / games_played,
                        (current_bs * (games_played - 1) + row['BLK']) / games_played,
                        (current_fga * (games_played - 1) + row['FGA']) / games_played,
                        (current_fgm * (games_played - 1) + row['FGM']) / games_played,
                        (current_threea * (games_played - 1) + row['3PA']) / games_played,
                        (current_threem * (games_played - 1) + row['3PM']) / games_played,
                        (current_fta * (games_played - 1) + row['FTA']) / games_played,
                        (current_ftm * (games_played - 1) + row['FTM']) / games_played
                    ]

                    # Update the table with the new averages
                    update_query = sql.SQL("""
                        UPDATE team_avg
                        SET games_played = %s, PTS = %s, REB = %s, OREB = %s, DREB = %s, AST = %s, PF = %s, STL = %s, TOV = %s, BLK = %s,
                            FGA = %s, FGM = %s, threeA = %s, threeM = %s, FTA = %s, FTM = %s
                        WHERE team = %s
                    """)
                    
                    cur.execute(update_query, [games_played] + updated_row + [team])




                cur.execute(
                sql.SQL("SELECT games_played, PTS, REB, OREB, DREB, AST, PF, STL, TOV, BLK, FGA, FGM, threeA, threeM, FTA, FTM FROM team_allowed_avg WHERE team = %s"),
                [row['opp']]
            )
            
                result = cur.fetchone()
                
                if result:
                    games_played, current_pts, current_reb, current_oreb,current_dreb, current_ast, current_pf, current_stl, current_tov, current_bs, current_fga, current_fgm, current_threea, current_threem, current_fta, current_ftm = result

                    # Calculate new averages
                    games_played += 1
                    updated_row = [
                        (current_pts * (games_played - 1) + row['PTS']) / games_played,
                        (current_reb * (games_played - 1) + row['REB']) / games_played,
                        (current_oreb * (games_played - 1) + row['OREB']) / games_played,
                        (current_dreb * (games_played - 1) + row['DREB']) / games_played,
                        (current_ast * (games_played - 1) + row['AST']) / games_played,
                        (current_pf * (games_played - 1) + row['PF']) / games_played,
                        (current_stl * (games_played - 1) + row['STL']) / games_played,
                        (current_tov * (games_played - 1) + row['TOV']) / games_played,
                        (current_bs * (games_played - 1) + row['BLK']) / games_played,
                        (current_fga * (games_played - 1) + row['FGA']) / games_played,
                        (current_fgm * (games_played - 1) + row['FGM']) / games_played,
                        (current_threea * (games_played - 1) + row['3PA']) / games_played,
                        (current_threem * (games_played - 1) + row['3PM']) / games_played,
                        (current_fta * (games_played - 1) + row['FTA']) / games_played,
                        (current_ftm * (games_played - 1) + row['FTM']) / games_played
                    ]

                    # Update the table with the new averages
                    update_query = sql.SQL("""
                        UPDATE team_avg
                        SET games_played = %s, PTS = %s, REB = %s, OREB = %s, DREB = %s, AST = %s, PF = %s, STL = %s, TOV = %s, BLK = %s,
                            FGA = %s, FGM = %s, threeA = %s, threeM = %s, FTA = %s, FTM = %s
                        WHERE team = %s
                    """)
                    
                    cur.execute(update_query, [games_played] + updated_row + [row['opp']])


                cur.execute(
                    sql.SQL("SELECT MIN(games_since) FROM team_for_lag WHERE team = %s"),
                    [row['Team']]
                )
                min_games_since = cur.fetchone()[0] -1

                if min_games_since is not None:
                    # Step 2: Delete a specific record if needed (adjust logic as per requirements)
                    cur.execute(
                        sql.SQL("DELETE FROM team_for_lag WHERE team = %s AND games_since = %s"),
                        [row['Team'], min_games_since + 5]
                    )

                # Step 3: Insert the new row into the table
                insert_query = sql.SQL("""
                    INSERT INTO team_for_lag (
                            team, games_since, PTS, REB,OREB,DREB, AST, PF, STL, TOV, BLK, FGA, FGM, threeA, 
                            threeM, FTA, FTM
                        ) VALUES (
                            %s, %s, %s, 
                            %s, %s, %s, 
                            %s, %s, %s, 
                            %s, %s, %s, 
                            %s, %s, %s,
                                       %s,%s
                        )
                        ON CONFLICT (team, games_since) 
                        DO NOTHING
                """)
                
                cur.execute(insert_query, (
                    row['Team'], min_games_since, row['PTS'], 
                    row['REB'],row['OREB'],row['DREB'], row['AST'], row['PF'], 
                    row['STL'], row['TOV'], row['BLK'], 
                    row['FGA'], row['FGM'], row['3PA'], 
                    row['3PM'], row['FTA'], row['FTM']
                ))
                cur.execute(
                sql.SQL("SELECT MIN(games_since) FROM team_allowed_lag WHERE team = %s"),
                [row['opp']]
            )
                min_games_since = cur.fetchone()[0] -1 

                if min_games_since is not None:
                    # Step 2: Delete a specific record if needed (adjust logic as per requirements)
                    cur.execute(
                        sql.SQL("DELETE FROM team_allowed_lag WHERE team = %s AND games_since = %s"),
                        [row['opp'], min_games_since + 5]
                    )
                conn.commit()

                # Step 3: Insert the new row into the table
                insert_query = sql.SQL("""
                    INSERT INTO team_allowed_lag (
                            team, games_since, PTS, REB,OREB,DREB, AST, PF, STL, TOV, BLK, FGA, FGM, threeA, 
                            threeM, FTA, FTM
                        ) VALUES (
                            %s, %s, %s, 
                            %s, %s, %s, 
                            %s, %s, %s, 
                            %s, %s, %s, 
                            %s, %s, %s,
                                       %s,%s
                        )
                        ON CONFLICT (team, games_since) 
                        DO NOTHING
                """)
                
                cur.execute(insert_query, (
                    row['opp'], min_games_since, row['PTS'], 
                    row['REB'],row['OREB'],row['DREB'], row['AST'], row['PF'], 
                    row['STL'], row['TOV'], row['BLK'], 
                    row['FGA'], row['FGM'], row['3PA'], 
                    row['3PM'], row['FTA'], row['FTM']
                ))
                cur.execute(
                sql.SQL("SELECT MIN(games_since) FROM matchup WHERE team = %s AND opp = %s"),
                [row['Team'], row['opp']]
                )
                min_games_since = cur.fetchone()[0] -1 

                if min_games_since is not None:
                    # Step 2: Delete a specific record if needed (adjust logic as per requirements)
                    cur.execute(
                        sql.SQL("DELETE FROM matchup WHERE team = %s AND opp = %s AND games_since = %s"),
                        [row['Team'], row['opp'], min_games_since + 3]
                    )
                # Step 3: Insert the new row into the table
                insert_query = sql.SQL("""
                    INSERT INTO matchup (
                            team, opp, games_since, FGA, FGM, ThreeA, ThreeM, 
                            FTA, FTM, PTS, REB, OREB, DREB, AST, TOV
                        ) VALUES (
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s
                        )
                        ON CONFLICT (team, opp, games_since) 
                        DO NOTHING
                """)
                
                cur.execute(insert_query, (
                    row['Team'], row['opp'], min_games_since, row['FGA'], row['FGM'], row['3PA'], 
                    row['3PM'], row['FTA'], row['FTM'], row['PTS'], row['REB'], row['OREB'], row['DREB'], row['AST'], row['TOV']
                ))
            conn.commit()

        if close:
            cur.close()
            conn.close()
    def insert_stats(self,df,team_df, close = False):
        conn = self.conn
        with conn.cursor() as cur:

            for index, row in df.iterrows():

                player = row['PLAYER']

            # Retrieve the current values from the table
                cur.execute(sql.SQL("SELECT FGA, FGM, ThreeA, ThreeM, FTA, FTM, PTS, PF, REB, AST, TOV, STL, BLK, PACE, PACE_per_40, PIE, PercentageFGA_2PT, PercentageFGA_3PT, PercentagePTS_2PT, PercentagePTS_2PT_MR, PercentagePTS_3PT, PercentagePTS_FBPs, PercentagePTS_FT, PercentagePTS_OffTO, PercentagePTS_PITP, TwoFGM_PercentageAST, TwoFGM_PercentageUAST, ThreeFGM_PercentageAST, ThreeFGM_PercentageUAST, FGM_PercentageAST, FGM_PercentageUAST, games_played FROM stat_avg_season WHERE player = %s"), [player])
                result = cur.fetchone()
                if result:

                    if result:
                        (
                            current_fga, current_fgm, current_threea, current_threem, current_fta, current_ftm, 
                            current_pts, current_pf, current_reb, current_ast, current_tov, current_stl, current_blk, 
                            current_pace, current_pace_per_40, current_pie, current_percentage_fga_2pt, 
                            current_percentage_fga_3pt, current_percentage_pts_2pt, current_percentage_pts_2pt_mr, 
                            current_percentage_pts_3pt, current_percentage_pts_fbps, current_percentage_pts_ft, 
                            current_percentage_pts_offto, current_percentage_pts_pitp, current_twofgm_percentageast, 
                            current_twofgm_percentageuast, current_threefgm_percentageast, current_threefgm_percentageuast, 
                            current_fgm_percentageast, current_fgm_percentageuast, games_played
                        ) = result

                        # Calculate new averages
                        games_played += 1
                        updated_row = [
                            (current_fga * (games_played - 1) + row['FGA']) / games_played,
                            (current_fgm * (games_played - 1) + row['FGM']) / games_played,
                            (current_threea * (games_played - 1) + row['3PA']) / games_played,
                            (current_threem * (games_played - 1) + row['3PM']) / games_played,
                            (current_fta * (games_played - 1) + row['FTA']) / games_played,
                            (current_ftm * (games_played - 1) + row['FTM']) / games_played,
                            (current_pts * (games_played - 1) + row['PTS']) / games_played,
                            (current_pf * (games_played - 1) + row['PF']) / games_played,
                            (current_reb * (games_played - 1) + row['REB']) / games_played,
                            (current_ast * (games_played - 1) + row['AST']) / games_played,
                            (current_tov * (games_played - 1) + row['TOV']) / games_played,
                            (current_stl * (games_played - 1) + row['STL']) / games_played,
                            (current_blk * (games_played - 1) + row['BLK']) / games_played,
                            (current_pace * (games_played - 1) + row['PACE']) / games_played,
                            (current_pace_per_40 * (games_played - 1) + row['PACE/40']) / games_played,
                            (current_pie * (games_played - 1) + row['PIE']) / games_played,
                            (current_percentage_fga_2pt * (games_played - 1) + row['%FGA 2PT']) / games_played,
                            (current_percentage_fga_3pt * (games_played - 1) + row['%FGA 3PT']) / games_played,
                            (current_percentage_pts_2pt * (games_played - 1) + row['%PTS 2PT']) / games_played,
                            (current_percentage_pts_2pt_mr * (games_played - 1) + row['%PTS 2PT MR']) / games_played,
                            (current_percentage_pts_3pt * (games_played - 1) + row['%PTS 3PT']) / games_played,
                            (current_percentage_pts_fbps * (games_played - 1) + row['%PTS FBPs']) / games_played,
                            (current_percentage_pts_ft * (games_played - 1) + row['%PTS FT']) / games_played,
                            (current_percentage_pts_offto * (games_played - 1) + row['%PTS OffTO']) / games_played,
                            (current_percentage_pts_pitp * (games_played - 1) + row['%PTS PITP']) / games_played,
                            (current_twofgm_percentageast * (games_played - 1) + row['2FGM %AST']) / games_played,
                            (current_twofgm_percentageuast * (games_played - 1) + row['2FGM %UAST']) / games_played,
                            (current_threefgm_percentageast * (games_played - 1) + row['3FGM %AST']) / games_played,
                            (current_threefgm_percentageuast * (games_played - 1) + row['3FGM %UAST']) / games_played,
                            (current_fgm_percentageast * (games_played - 1) + row['FGM %AST']) / games_played,
                            (current_fgm_percentageuast * (games_played - 1) + row['FGM %UAST']) / games_played,
                            games_played
                        ]


                        # Update the table with the new averages
                        update_query = sql.SQL("""
                        UPDATE stat_avg_season
                        SET FGA = %s, FGM = %s, ThreeA = %s, ThreeM = %s, FTA = %s, FTM = %s, PTS = %s, PF = %s, REB = %s, AST = %s, 
                            TOV = %s, STL = %s, BLK = %s, PACE = %s, PACE_per_40 = %s, PIE = %s, 
                            PercentageFGA_2PT = %s, PercentageFGA_3PT = %s, PercentagePTS_2PT = %s, 
                            PercentagePTS_2PT_MR = %s, PercentagePTS_3PT = %s, PercentagePTS_FBPs = %s, 
                            PercentagePTS_FT = %s, PercentagePTS_OffTO = %s, PercentagePTS_PITP = %s, 
                            TwoFGM_PercentageAST = %s, TwoFGM_PercentageUAST = %s, ThreeFGM_PercentageAST = %s, 
                            ThreeFGM_PercentageUAST = %s, FGM_PercentageAST = %s, FGM_PercentageUAST = %s, 
                            games_played = %s
                        WHERE player = %s
                    """)
                        
                        cur.execute(update_query, updated_row + [player])
                    
                    player_name = row['PLAYER']
                    opp = row['opp']

                    # Step 2: Find the minimum games_since for the player, if any
                    cur.execute(
                        sql.SQL("SELECT MIN(games_since) FROM stat_lag WHERE player = %s"),
                        [player_name]
                    )
                    
                    min_games_since = cur.fetchone()[0]- 1


                    cur.execute(
                        sql.SQL("DELETE FROM stat_lag WHERE player = %s AND games_since = %s"),
                        [player_name, min_games_since+5]
                    )

                    # Step 4: Insert the new row into the table
                    insert_query = sql.SQL("""
                        INSERT INTO stat_lag (
                            player, games_since, FGA, FGM, ThreeA, ThreeM, FTA, FTM, PTS, PF, REB, AST, 
                            TOV, STL, BLK, PACE, PACE_per_40, PIE, 
                            PercentageFGA_2PT, PercentageFGA_3PT, PercentagePTS_2PT, PercentagePTS_2PT_MR, 
                            PercentagePTS_3PT, PercentagePTS_FBPs, PercentagePTS_FT, PercentagePTS_OffTO, 
                            PercentagePTS_PITP, TwoFGM_PercentageAST, TwoFGM_PercentageUAST, 
                            ThreeFGM_PercentageAST, ThreeFGM_PercentageUAST, FGM_PercentageAST, FGM_PercentageUAST
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """)

                    cur.execute(insert_query, [
                        row['PLAYER'], min_games_since, 
                        row['FGA'], row['FGM'], row['3PA'], row['3PM'], row['FTA'], 
                        row['FTM'], row['PTS'], row['PF'], row['REB'], row['AST'], row['TOV'], 
                        row['STL'], row['BLK'], row['PACE'], row['PACE/40'], row['PIE'], 
                        row['%FGA 2PT'], row['%FGA 3PT'], row['%PTS 2PT'], row['%PTS 2PT MR'], 
                        row['%PTS 3PT'], row['%PTS FBPs'], row['%PTS FT'], row['%PTS OffTO'], 
                        row['%PTS PITP'], row['2FGM %AST'], row['2FGM %UAST'], row['3FGM %AST'], 
                        row['3FGM %UAST'], row['FGM %AST'], row['FGM %UAST']
                    ])

                    

                    #STAT_LAG_OPP
                    #select * from stat_lag_opp where player = 'Caitlin Clark' and opp = 'dal' and games_since = (SELECT MAX(games_since) FROM stat_lag_opp WHERE player = 'Caitlin Clark' and opp = 'dal');


                    # Step 2: Find the minimum games_since for the player, if any

                    cur.execute(
                        sql.SQL("DELETE FROM stat_lag_opp WHERE player = %s AND opp = %s"),
                        [player_name, opp]
                    )



                    # Step 4: Insert the new row into the table
                    insert_query = sql.SQL("""
                        INSERT INTO stat_lag_opp (
                            player, opp, FGA, FGM, ThreeA, ThreeM, FTA, FTM, PTS, PF, REB, AST, 
                            TOV, STL, BLK, PACE, PACE_per_40, PIE, 
                            PercentageFGA_2PT, PercentageFGA_3PT, PercentagePTS_2PT, PercentagePTS_2PT_MR, 
                            PercentagePTS_3PT, PercentagePTS_FBPs, PercentagePTS_FT, PercentagePTS_OffTO, 
                            PercentagePTS_PITP, TwoFGM_PercentageAST, TwoFGM_PercentageUAST, 
                            ThreeFGM_PercentageAST, ThreeFGM_PercentageUAST, FGM_PercentageAST, FGM_PercentageUAST
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """)

                    cur.execute(insert_query, [
                        row['PLAYER'], row['opp'], 
                        row['FGA'], row['FGM'], row['3PA'], row['3PM'], row['FTA'], 
                        row['FTM'], row['PTS'], row['PF'], row['REB'], row['AST'], row['TOV'], 
                        row['STL'], row['BLK'], row['PACE'], row['PACE/40'], row['PIE'], 
                        row['%FGA 2PT'], row['%FGA 3PT'], row['%PTS 2PT'], row['%PTS 2PT MR'], 
                        row['%PTS 3PT'], row['%PTS FBPs'], row['%PTS FT'], row['%PTS OffTO'], 
                        row['%PTS PITP'], row['2FGM %AST'], row['2FGM %UAST'], row['3FGM %AST'], 
                        row['3FGM %UAST'], row['FGM %AST'], row['FGM %UAST']
                    ])
            for index,row in team_df.iterrows():
            # Step 1: Find the minimum games_since for the team, if any
            
                team = row['Team']
            
            # Retrieve the current values from the table
                cur.execute(
                    sql.SQL("SELECT games_played, PTS, REB, AST, PF, STL, TOV, BLK, FGA, FGM, threeA, threeM, FTA, FTM FROM team_avg WHERE team = %s"),
                    [team]
                )
                
                result = cur.fetchone()
                
                if result:
                    games_played, current_pts, current_reb, current_ast, current_pf, current_stl, current_tov, current_bs, current_fga, current_fgm, current_threea, current_threem, current_fta, current_ftm = result

                    # Calculate new averages
                    games_played += 1
                    updated_row = [
                        (current_pts * (games_played - 1) + row['PTS']) / games_played,
                        (current_reb * (games_played - 1) + row['REB']) / games_played,
                        (current_ast * (games_played - 1) + row['AST']) / games_played,
                        (current_pf * (games_played - 1) + row['PF']) / games_played,
                        (current_stl * (games_played - 1) + row['STL']) / games_played,
                        (current_tov * (games_played - 1) + row['TOV']) / games_played,
                        (current_bs * (games_played - 1) + row['BLK']) / games_played,
                        (current_fga * (games_played - 1) + row['FGA']) / games_played,
                        (current_fgm * (games_played - 1) + row['FGM']) / games_played,
                        (current_threea * (games_played - 1) + row['3PA']) / games_played,
                        (current_threem * (games_played - 1) + row['3PM']) / games_played,
                        (current_fta * (games_played - 1) + row['FTA']) / games_played,
                        (current_ftm * (games_played - 1) + row['FTM']) / games_played
                    ]

                    # Update the table with the new averages
                    update_query = sql.SQL("""
                        UPDATE team_avg
                        SET games_played = %s, PTS = %s, REB = %s, AST = %s, PF = %s, STL = %s, TOV = %s, BLK = %s,
                            FGA = %s, FGM = %s, threeA = %s, threeM = %s, FTA = %s, FTM = %s
                        WHERE team = %s
                    """)
                    
                    cur.execute(update_query, [games_played] + updated_row + [team])




                cur.execute(
                sql.SQL("SELECT games_played, PTS, REB, AST, PF, STL, TOV, BLK, FGA, FGM, threeA, threeM, FTA, FTM FROM team_allowed_avg WHERE team = %s"),
                [row['opp']]
            )
            
                result = cur.fetchone()
                
                if result:
                    games_played, current_pts, current_reb, current_ast, current_pf, current_stl, current_tov, current_bs, current_fga, current_fgm, current_threea, current_threem, current_fta, current_ftm = result

                    # Calculate new averages
                    games_played += 1
                    updated_row = [
                        (current_pts * (games_played - 1) + row['PTS']) / games_played,
                        (current_reb * (games_played - 1) + row['REB']) / games_played,
                        (current_ast * (games_played - 1) + row['AST']) / games_played,
                        (current_pf * (games_played - 1) + row['PF']) / games_played,
                        (current_stl * (games_played - 1) + row['STL']) / games_played,
                        (current_tov * (games_played - 1) + row['TOV']) / games_played,
                        (current_bs * (games_played - 1) + row['BLK']) / games_played,
                        (current_fga * (games_played - 1) + row['FGA']) / games_played,
                        (current_fgm * (games_played - 1) + row['FGM']) / games_played,
                        (current_threea * (games_played - 1) + row['3PA']) / games_played,
                        (current_threem * (games_played - 1) + row['3PM']) / games_played,
                        (current_fta * (games_played - 1) + row['FTA']) / games_played,
                        (current_ftm * (games_played - 1) + row['FTM']) / games_played
                    ]

                    # Update the table with the new averages
                    update_query = sql.SQL("""
                        UPDATE team_avg
                        SET games_played = %s, PTS = %s, REB = %s, AST = %s, PF = %s, STL = %s, TOV = %s, BLK = %s,
                            FGA = %s, FGM = %s, threeA = %s, threeM = %s, FTA = %s, FTM = %s
                        WHERE team = %s
                    """)
                    
                    cur.execute(update_query, [games_played] + updated_row + [row['opp']])


                cur.execute(
                    sql.SQL("SELECT MIN(games_since) FROM team_for_lag WHERE team = %s"),
                    [row['Team']]
                )
                min_games_since = cur.fetchone()[0] -1

                if min_games_since is not None:
                    # Step 2: Delete a specific record if needed (adjust logic as per requirements)
                    cur.execute(
                        sql.SQL("DELETE FROM team_for_lag WHERE team = %s AND games_since = %s"),
                        [row['Team'], min_games_since + 5]
                    )

                # Step 3: Insert the new row into the table
                insert_query = sql.SQL("""
                    INSERT INTO team_for_lag (
                            team, games_since, PTS, REB, AST, PF, STL, TOV, BLK, FGA, FGM, threeA, 
                            threeM, FTA, FTM
                        ) VALUES (
                            %s, %s, %s, 
                            %s, %s, %s, 
                            %s, %s, %s, 
                            %s, %s, %s, 
                            %s, %s, %s
                        )
                        ON CONFLICT (team, games_since) 
                        DO NOTHING
                """)
                
                cur.execute(insert_query, (
                    row['Team'], min_games_since, row['PTS'], 
                    row['REB'], row['AST'], row['PF'], 
                    row['STL'], row['TOV'], row['BLK'], 
                    row['FGA'], row['FGM'], row['3PA'], 
                    row['3PM'], row['FTA'], row['FTM']
                ))
                cur.execute(
                sql.SQL("SELECT MIN(games_since) FROM team_allowed_lag WHERE team = %s"),
                [row['opp']]
            )
                min_games_since = cur.fetchone()[0] -1 

                if min_games_since is not None:
                    # Step 2: Delete a specific record if needed (adjust logic as per requirements)
                    cur.execute(
                        sql.SQL("DELETE FROM team_allowed_lag WHERE team = %s AND games_since = %s"),
                        [row['opp'], min_games_since + 5]
                    )
                conn.commit()

                # Step 3: Insert the new row into the table
                insert_query = sql.SQL("""
                    INSERT INTO team_allowed_lag (
                            team, games_since, PTS, REB, AST, PF, STL, TOV, BLK, FGA, FGM, threeA, 
                            threeM, FTA, FTM
                        ) VALUES (
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                            %s, %s, %s
                        )
                        ON CONFLICT (team, games_since) 
                        DO NOTHING
                """)
                
                cur.execute(insert_query, (
                    row['opp'], min_games_since, row['PTS'], row['REB'], row['AST'], row['PF'], 
                    row['STL'], row['TOV'], row['BLK'], row['FGA'], row['FGM'], row['3PA'], 
                    row['3PM'], row['FTA'], row['FTM']
                ))
                cur.execute(
                sql.SQL("SELECT MIN(games_since) FROM matchup WHERE team = %s AND opp = %s"),
                [row['Team'], row['opp']]
                )
                min_games_since = cur.fetchone()[0] -1 

                if min_games_since is not None:
                    # Step 2: Delete a specific record if needed (adjust logic as per requirements)
                    cur.execute(
                        sql.SQL("DELETE FROM matchup WHERE team = %s AND opp = %s AND games_since = %s"),
                        [row['Team'], row['opp'], min_games_since + 3]
                    )
                # Step 3: Insert the new row into the table
                insert_query = sql.SQL("""
                    INSERT INTO matchup (
                            team, opp, games_since, FGA, FGM, ThreeA, ThreeM, 
                            FTA, FTM, PTS, REB, AST, TOV
                        ) VALUES (
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                        )
                        ON CONFLICT (team, opp, games_since) 
                        DO NOTHING
                """)
                
                cur.execute(insert_query, (
                    row['Team'], row['opp'], min_games_since, row['FGA'], row['FGM'], row['3PA'], 
                    row['3PM'], row['FTA'], row['FTM'], row['PTS'], row['REB'], row['AST'], row['TOV']
                ))
            conn.commit()

        if close:
            cur.close()
            conn.close()
    
    def get_odds(self):
        url = 'https://sportsbook.draftkings.com/leagues/basketball/wnba?category=player-points&subcategory=points'
        options = webdriver.ChromeOptions()
        options.add_argument('--headless') 
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        time.sleep(3)


        # Initialize an empty list to store dictionaries
        data_list = []

        # Assuming you already have the HTML response from the page
        response = driver.page_source
        soup = BeautifulSoup(response, 'html.parser')

        # Find the relevant tables
        tables = soup.find_all(class_='sportsbook-table')

        events = soup.find_all('div', class_='sportsbook-event-accordion__title-wrapper')

        # Initialize a dictionary to hold team matchups
        team_matchups = {}

        # Loop through each event to extract the team names
        for event in events:
            team_images = event.find_all('img', class_='sportsbook-event-accordion__title-logo')
            
            if len(team_images) == 2:
                # Extract team names from the alt attributes
                team_1 = team_images[0]['alt'].replace('-logo', '').strip().split()[0].lower()
                team_2 = team_images[1]['alt'].replace('-logo', '').strip().split()[0].lower()

                if team_1 == 'la':
                    team_1 = 'las'
                if team_2 == 'la':
                    team_2 = 'las'
                if team_1 == 'ny':
                    team_1 = 'nyl'
                if team_2 == 'ny':
                    team_2 = 'nyl'

                # Add the matchup to the dictionary
                team_matchups[team_1] = [team_2,0]
                team_matchups[team_2] = [team_1,1]

        # Iterate through rows of the first table (excluding the header)
        for table in tables: 
            for row in table.find_all('tr')[1:]:
                tmp = row.text
                tmp = tmp.replace(u'\xa0', u' ')

                # Attempt to match with the first regex pattern
                lines = re.findall(r'(.+)New!.+O ([\d.]{3,6})([+−]\d{2,4}).+([\d.]{3,6})([+−]\d{2,4})', tmp)
                if not lines:  # If no match, try the second pattern
                    lines = re.findall(r'(.+)O ([\d.]{3,6})([+−]\d{2,4}).+([\d.]{3,6})([+−]\d{2,4})', tmp)

                if lines:  # Only process if there's a match
                    lines = lines[0] 
                    dct = {
                        'name': lines[0].strip(),
                        'line': float(lines[1]),
                        'over': lines[2],
                        'under': lines[4]
                    }
                    data_list.append(dct)

        # Convert the list of dictionaries to a DataFrame
        dk_df = pd.DataFrame(data_list)
        driver.quit()
        return dk_df,team_matchups
    
    def get_teams(self, text):
        data = json.loads(text)
        df = pd.json_normalize(data['data'])
        ids=  dict(re.findall(r'"id":"([^"]+)",.{15,30}"display_name":"([^"]+)"', text))
        t_ids=  dict(re.findall(r""""name":"([A-z'\-]+ [A-z'\-]+)","position":"[A-z]","team":"([A-Z]+)",""", text))
        df["player"]= df["relationships.new_player.data.id"].map(ids)
        df["team"]= df["player"].map(t_ids)
        df["opp"]= df["attributes.description"]
        df = df[df['attributes.odds_type']=='standard']
        df["attributes.stat_type"].unique()
        fixed_df = df[['player',"attributes.stat_type",'attributes.line_score','opp','team']]
        return fixed_df.dropna()
    def get_prize_picks(self,text):
    
        text= text.replace('\t', '')

        names = re.findall(r'display_name":"([^"]+)', text)
        new_names = []
        for name in names:
            if '+' not in name:
                new_names.append(name)
        data = json.loads(text)
        df = pd.json_normalize(data['data'])
        ids=  dict(re.findall(r'"id":"([^"]+)",.{15,30}"display_name":"([^"]+)"', text))
        df["relationships.new_player.data.id"]= df["relationships.new_player.data.id"].map(ids)
        df = df[df['attributes.odds_type']=='standard']
        fixed_df = df
        fixed_df = df[['relationships.new_player.data.id',"attributes.stat_type",'attributes.line_score','attributes.description']]
        fixed_df["attributes.stat_type"].unique()
        fixed_df = fixed_df[fixed_df['attributes.stat_type']=="Points"]
        return fixed_df
    
    def allinsert_stats(self,df,team_df,pos_df, close = False):
        conn = self.conn
        team_df.columns = [col.upper() for col in team_df.columns]
        with conn.cursor() as cur:

            for index, row in df.iterrows():

                player = row['PLAYER']


                # Retrieve the current values from the table
                cur.execute(
                    sql.SQL("""
                        SELECT fga, fgm, threepa, threepm, fta, ftm, pts, reb, oreb, dreb, ast, tov, pf, stl, blk, pace, pace_per_40, pie, 
                            percentagefga_twopt, percentagefga_threept, percentagepts_twopt, percentagepts_twopt_mr, 
                            percentagepts_threept, percentagepts_fbps, percentagepts_ft, percentagepts_offto, percentagepts_pitp, 
                            twofgm_percentageast, twofgm_percentageuast, threefgm_percentageast, threefgm_percentageuast, 
                            fgm_percentageast, fgm_percentageuast, usgpercentage, rebpercentage, games_played 
                        FROM stat_avg_season 
                        WHERE player = %s
                    """),
                    [player]
                )

                result = cur.fetchone()
                if result:
                    (current_fga, current_fgm, current_threepa, current_threepm, current_fta, current_ftm, current_pts, current_reb, 
                    current_oreb, current_dreb, current_ast, current_tov, current_pf, current_stl, current_blk, current_pace, 
                    current_pace_per_40, current_pie, current_percentagefga_twopt, current_percentagefga_threept, 
                    current_percentagepts_twopt, current_percentagepts_twopt_mr, current_percentagepts_threept, 
                    current_percentagepts_fbps, current_percentagepts_ft, current_percentagepts_offto, current_percentagepts_pitp, 
                    current_twofgm_percentageast, current_twofgm_percentageuast, current_threefgm_percentageast, 
                    current_threefgm_percentageuast, current_fgm_percentageast, current_fgm_percentageuast, current_usgpercentage, 
                    current_rebpercentage, games_played) = result

                    # Calculate new averages
                    games_played += 1
                    updated_row = [
                        (current_fga * (games_played - 1) + row['FGA']) / games_played,
                        (current_fgm * (games_played - 1) + row['FGM']) / games_played,
                        (current_threepa * (games_played - 1) + row['3PA']) / games_played,
                        (current_threepm * (games_played - 1) + row['3PM']) / games_played,
                        (current_fta * (games_played - 1) + row['FTA']) / games_played,
                        (current_ftm * (games_played - 1) + row['FTM']) / games_played,
                        (current_pts * (games_played - 1) + row['PTS']) / games_played,
                        (current_reb * (games_played - 1) + row['REB']) / games_played,
                        (current_oreb * (games_played - 1) + row['OREB']) / games_played,
                        (current_dreb * (games_played - 1) + row['DREB']) / games_played,
                        (current_ast * (games_played - 1) + row['AST']) / games_played,
                        (current_tov * (games_played - 1) + row['TOV']) / games_played,
                        (current_pf * (games_played - 1) + row['PF']) / games_played,
                        (current_stl * (games_played - 1) + row['STL']) / games_played,
                        (current_blk * (games_played - 1) + row['BLK']) / games_played,
                        (current_pace * (games_played - 1) + row['PACE']) / games_played,
                        (current_pace_per_40 * (games_played - 1) + row['PACE/40']) / games_played,
                        (current_pie * (games_played - 1) + row['PIE']) / games_played,
                        (current_percentagefga_twopt * (games_played - 1) + row['%FGA 2PT']) / games_played,
                        (current_percentagefga_threept * (games_played - 1) + row['%FGA 3PT']) / games_played,
                        (current_percentagepts_twopt * (games_played - 1) + row['%PTS 2PT']) / games_played,
                        (current_percentagepts_twopt_mr * (games_played - 1) + row['%PTS 2PT MR']) / games_played,
                        (current_percentagepts_threept * (games_played - 1) + row['%PTS 3PT']) / games_played,
                        (current_percentagepts_fbps * (games_played - 1) + row['%PTS FBPs']) / games_played,
                        (current_percentagepts_ft * (games_played - 1) + row['%PTS FT']) / games_played,
                        (current_percentagepts_offto * (games_played - 1) + row['%PTS OffTO']) / games_played,
                        (current_percentagepts_pitp * (games_played - 1) + row['%PTS PITP']) / games_played,
                        (current_twofgm_percentageast * (games_played - 1) + row['2FGM %AST']) / games_played,
                        (current_twofgm_percentageuast * (games_played - 1) + row['2FGM %UAST']) / games_played,
                        (current_threefgm_percentageast * (games_played - 1) + row['3FGM %AST']) / games_played,
                        (current_threefgm_percentageuast * (games_played - 1) + row['3FGM %UAST']) / games_played,
                        (current_fgm_percentageast * (games_played - 1) + row['FGM %AST']) / games_played,
                        (current_fgm_percentageuast * (games_played - 1) + row['FGM %UAST']) / games_played,
                        (current_usgpercentage * (games_played - 1) + row['USG%']) / games_played,
                        (current_rebpercentage * (games_played - 1) + row['REB%']) / games_played,
                        games_played
                    ]

                    # Update the table with the new averages
                    update_query = sql.SQL("""
                        UPDATE stat_avg_season
                        SET fga = %s, fgm = %s, threepa = %s, threepm = %s, fta = %s, ftm = %s, pts = %s, reb = %s, oreb = %s, dreb = %s, 
                            ast = %s, tov = %s, pf = %s, stl = %s, blk = %s, pace = %s, pace_per_40 = %s, pie = %s, percentagefga_twopt = %s, 
                            percentagefga_threept = %s, percentagepts_twopt = %s, percentagepts_twopt_mr = %s, percentagepts_threept = %s, 
                            percentagepts_fbps = %s, percentagepts_ft = %s, percentagepts_offto = %s, percentagepts_pitp = %s, 
                            twofgm_percentageast = %s, twofgm_percentageuast = %s, threefgm_percentageast = %s, threefgm_percentageuast = %s, 
                            fgm_percentageast = %s, fgm_percentageuast = %s, usgpercentage = %s, rebpercentage = %s, games_played = %s
                        WHERE player = %s
                    """)

                    cur.execute(update_query, updated_row + [player])
                    
                    player_name = row['PLAYER']
                    opp = row['opp']

                    # Step 2: Find the minimum games_since for the player, if any
                    cur.execute(
                        sql.SQL("SELECT MIN(games_since) FROM stat_lag WHERE player = %s"),
                        [player_name]
                    )
                    
                    min_games_since = cur.fetchone()[0]- 1


                    cur.execute(
                        sql.SQL("DELETE FROM stat_lag WHERE player = %s AND games_since = %s"),
                        [player_name, min_games_since+5]
                    )

                    # Step 4: Insert the new row into the table
                    insert_query = sql.SQL("""
        INSERT INTO stat_lag (
            player, games_since, fga, fgm, threepa, threepm, fta, ftm, pts, pf, reb, oreb, dreb, ast, tov, stl, blk, pace, pace_per_40, 
            pie, percentagefga_twopt, percentagefga_threept, percentagepts_twopt, percentagepts_twopt_mr, percentagepts_threept, 
            percentagepts_fbps, percentagepts_ft, percentagepts_offto, percentagepts_pitp, twofgm_percentageast, 
            twofgm_percentageuast, threefgm_percentageast, threefgm_percentageuast, fgm_percentageast, fgm_percentageuast, usgpercentage, 
                                           rebpercentage
        ) VALUES (%s, %s, %s, %s, %s, %s, 
                  %s, %s, %s, %s, %s, %s, 
                  %s, %s, %s, %s, %s, %s, 
                  %s, %s, %s, %s, %s, %s, 
                  %s, %s, %s, %s, %s, %s, 
                  %s, %s, %s, %s, %s, %s,%s)
    """)

                    cur.execute(insert_query, [
                        row['PLAYER'], min_games_since, row['FGA'], row['FGM'], row['3PA'], row['3PM'], 
                        row['FTA'], row['FTM'], row['PTS'], row['PF'], row['REB'], row['OREB'], 
                        row['DREB'], row['AST'], row['TOV'], row['STL'], row['BLK'], row['PACE'], 
                        row['PACE/40'], row['PIE'], row['%FGA 2PT'], row['%FGA 3PT'], row['%PTS 2PT'], row['%PTS 2PT MR'], 
                        row['%PTS 3PT'], row['%PTS FBPs'], row['%PTS FT'], row['%PTS OffTO'], row['%PTS PITP'], row['2FGM %AST'], 
                        row['2FGM %UAST'], row['3FGM %AST'], row['3FGM %UAST'], row['FGM %AST'], row['FGM %UAST'], row['USG%'], 
                        row['REB%']
                    ])

                    

                    #STAT_LAG_OPP
                    #select * from stat_lag_opp where player = 'Caitlin Clark' and opp = 'dal' and games_since = (SELECT MAX(games_since) FROM stat_lag_opp WHERE player = 'Caitlin Clark' and opp = 'dal');


                    # Step 2: Find the minimum games_since for the player, if any

                    cur.execute(
                        sql.SQL("DELETE FROM stat_lag_opp WHERE player = %s AND opp = %s"),
                        [player_name, opp]
                    )



                    # Step 4: Insert the new row into the table
                    insert_query = sql.SQL("""
                        INSERT INTO stat_lag_opp (
                            player, opp, fga, fgm, threepa, threepm, fta, ftm, pts, pf, reb, oreb, dreb, ast, tov, stl, blk, pace, pace_per_40, pie, percentagefga_twopt, percentagefga_threept, percentagepts_twopt, percentagepts_twopt_mr, percentagepts_threept, percentagepts_fbps, percentagepts_ft, percentagepts_offto, percentagepts_pitp, twofgm_percentageast, twofgm_percentageuast, threefgm_percentageast, threefgm_percentageuast, fgm_percentageast, fgm_percentageuast, usgpercentage, rebpercentage
                        ) VALUES (%s, %s, %s, %s, %s, %s, 
                                  %s, %s, %s, %s, %s, %s, 
                                  %s, %s, %s, %s, %s, %s, 
                                  %s, %s, %s, %s, %s, %s, 
                                  %s, %s, %s, %s, %s, %s, 
                                  %s, %s, %s, %s, %s, %s,%s)
                    """)

                    cur.execute(insert_query, [
                        row['PLAYER'], opp, row['FGA'], row['FGM'], row['3PA'], row['3PM'], 
                        row['FTA'], row['FTM'], row['PTS'], row['PF'], row['REB'], row['OREB'], 
                        row['DREB'], row['AST'], row['TOV'], row['STL'], row['BLK'], row['PACE'], 
                        row['PACE/40'], row['PIE'], row['%FGA 2PT'], row['%FGA 3PT'], row['%PTS 2PT'], row['%PTS 2PT MR'], 
                        row['%PTS 3PT'], row['%PTS FBPs'], row['%PTS FT'], row['%PTS OffTO'], row['%PTS PITP'], row['2FGM %AST'], 
                        row['2FGM %UAST'], row['3FGM %AST'], row['3FGM %UAST'], row['FGM %AST'], row['FGM %UAST'], row['USG%'], 
                        row['REB%']
                    ])
            for index,row in team_df.iterrows():
            # Step 1: Find the minimum games_since for the team, if any
            
                team = row['TEAM']
                opp = row['OPP']
            
            # Retrieve the current values from the table
                cur.execute(
                sql.SQL("""
                    SELECT games_played, pts, reb, oreb, dreb, ast, pf, stl, tov, blk, fga, fgm, threepa, threepm, fta, ftm,
                        offrtg, defrtg, netrtg, astpercentage, ast_per_to, ast_ratio, orebpercentage, drebpercentage, rebpercentage,
                        tovpercentage, efgpercentage, tspercentage, pace, pace_per_40, pie
                    FROM team_avg 
                    WHERE team = %s
                """),
                [team]
            )

                result = cur.fetchone()

                # If the team exists in the table, update the averages
                if result:
                    (
                        games_played, current_pts, current_reb, current_oreb, current_dreb, current_ast, current_pf, current_stl, 
                        current_tov, current_bs, current_fga, current_fgm, current_threepa, current_threepm, current_fta, current_ftm,
                        current_offrtg, current_defrtg, current_netrtg, current_astpercentage, current_ast_per_to, current_ast_ratio,
                        current_orebpercentage, current_drebpercentage, current_rebpercentage, current_tovpercentage, current_efgpercentage,
                        current_tspercentage, current_pace, current_pace_per_40, current_pie
                    ) = result

                    # Update games played and calculate new averages
                    games_played += 1
                    updated_row = [
                        (current_pts * (games_played - 1) + row['PTS']) / games_played,
                        (current_reb * (games_played - 1) + row['REB']) / games_played,
                        (current_oreb * (games_played - 1) + row['OREB']) / games_played,
                        (current_dreb * (games_played - 1) + row['DREB']) / games_played,
                        (current_ast * (games_played - 1) + row['AST']) / games_played,
                        (current_pf * (games_played - 1) + row['PF']) / games_played,
                        (current_stl * (games_played - 1) + row['STL']) / games_played,
                        (current_tov * (games_played - 1) + row['TOV']) / games_played,
                        (current_bs * (games_played - 1) + row['BLK']) / games_played,
                        (current_fga * (games_played - 1) + row['FGA']) / games_played,
                        (current_fgm * (games_played - 1) + row['FGM']) / games_played,
                        (current_threepa * (games_played - 1) + row['3PA']) / games_played,
                        (current_threepm * (games_played - 1) + row['3PM']) / games_played,
                        (current_fta * (games_played - 1) + row['FTA']) / games_played,
                        (current_ftm * (games_played - 1) + row['FTM']) / games_played,
                        # Update all other stats similarly
                        (current_offrtg * (games_played - 1) + row['OFFRTG']) / games_played,
                        (current_defrtg * (games_played - 1) + row['DEFRTG']) / games_played,
                        (current_netrtg * (games_played - 1) + row['NETRTG']) / games_played,
                        (current_astpercentage * (games_played - 1) + row['AST%']) / games_played,
                        (current_ast_per_to * (games_played - 1) + row['AST/TO']) / games_played,
                        (current_ast_ratio * (games_played - 1) + row['AST RATIO']) / games_played,
                        (current_orebpercentage * (games_played - 1) + row['OREB%']) / games_played,
                        (current_drebpercentage * (games_played - 1) + row['DREB%']) / games_played,
                        (current_rebpercentage * (games_played - 1) + row['REB%']) / games_played,
                        (current_tovpercentage * (games_played - 1) + row['TOV%']) / games_played,
                        (current_efgpercentage * (games_played - 1) + row['EFG%']) / games_played,
                        (current_tspercentage * (games_played - 1) + row['TS%']) / games_played,
                        (current_pace * (games_played - 1) + row['PACE']) / games_played,
                        (current_pace_per_40 * (games_played - 1) + row['PACE/40']) / games_played,
                        (current_pie * (games_played - 1) + row['PIE']) / games_played
                    ]

                    # Update the table with the new averages
                    update_query = sql.SQL("""
                        UPDATE team_avg
                        SET games_played = %s, pts = %s, reb = %s, oreb = %s, dreb = %s, ast = %s, pf = %s, stl = %s, tov = %s, blk = %s,
                            fga = %s, fgm = %s, threepa = %s, threepm = %s, fta = %s, ftm = %s,
                            offrtg = %s, defrtg = %s, netrtg = %s, astpercentage = %s, ast_per_to = %s, ast_ratio = %s, orebpercentage = %s, 
                            drebpercentage = %s, rebpercentage = %s, tovpercentage = %s, efgpercentage = %s, tspercentage = %s, 
                            pace = %s, pace_per_40 = %s, pie = %s
                        WHERE team = %s
                    """)

                    cur.execute(update_query, [games_played] + updated_row + [team])




                cur.execute(
                    sql.SQL("""
                        SELECT games_played, pts, reb, oreb, dreb, ast, pf, stl, tov, blk, fga, fgm, threepa, threepm, fta, ftm,
                            offrtg, defrtg, netrtg, astpercentage, ast_per_to, ast_ratio, orebpercentage, drebpercentage, rebpercentage,
                            tovpercentage, efgpercentage, tspercentage, pace, pace_per_40, pie
                        FROM team_allowed_avg 
                        WHERE team = %s
                    """),
                    [opp]
                )

                result = cur.fetchone()

                # If the team exists in the table, update the averages
                if result:
                    (
                        games_played, current_pts, current_reb, current_oreb, current_dreb, current_ast, current_pf, current_stl, 
                        current_tov, current_bs, current_fga, current_fgm, current_threepa, current_threepm, current_fta, current_ftm,
                        current_offrtg, current_defrtg, current_netrtg, current_astpercentage, current_ast_per_to, current_ast_ratio,
                        current_orebpercentage, current_drebpercentage, current_rebpercentage, current_tovpercentage, current_efgpercentage,
                        current_tspercentage, current_pace, current_pace_per_40, current_pie
                    ) = result

                    # Update games played and calculate new averages
                    games_played += 1
                    updated_row = [
                        (current_pts * (games_played - 1) + row['PTS']) / games_played,
                        (current_reb * (games_played - 1) + row['REB']) / games_played,
                        (current_oreb * (games_played - 1) + row['OREB']) / games_played,
                        (current_dreb * (games_played - 1) + row['DREB']) / games_played,
                        (current_ast * (games_played - 1) + row['AST']) / games_played,
                        (current_pf * (games_played - 1) + row['PF']) / games_played,
                        (current_stl * (games_played - 1) + row['STL']) / games_played,
                        (current_tov * (games_played - 1) + row['TOV']) / games_played,
                        (current_bs * (games_played - 1) + row['BLK']) / games_played,
                        (current_fga * (games_played - 1) + row['FGA']) / games_played,
                        (current_fgm * (games_played - 1) + row['FGM']) / games_played,
                        (current_threepa * (games_played - 1) + row['3PA']) / games_played,
                        (current_threepm * (games_played - 1) + row['3PM']) / games_played,
                        (current_fta * (games_played - 1) + row['FTA']) / games_played,
                        (current_ftm * (games_played - 1) + row['FTM']) / games_played,
                        # Update all other stats similarly
                        (current_offrtg * (games_played - 1) + row['OFFRTG']) / games_played,
                        (current_defrtg * (games_played - 1) + row['DEFRTG']) / games_played,
                        (current_netrtg * (games_played - 1) + row['NETRTG']) / games_played,
                        (current_astpercentage * (games_played - 1) + row['AST%']) / games_played,
                        (current_ast_per_to * (games_played - 1) + row['AST/TO']) / games_played,
                        (current_ast_ratio * (games_played - 1) + row['AST RATIO']) / games_played,
                        (current_orebpercentage * (games_played - 1) + row['OREB%']) / games_played,
                        (current_drebpercentage * (games_played - 1) + row['DREB%']) / games_played,
                        (current_rebpercentage * (games_played - 1) + row['REB%']) / games_played,
                        (current_tovpercentage * (games_played - 1) + row['TOV%']) / games_played,
                        (current_efgpercentage * (games_played - 1) + row['EFG%']) / games_played,
                        (current_tspercentage * (games_played - 1) + row['TS%']) / games_played,
                        (current_pace * (games_played - 1) + row['PACE']) / games_played,
                        (current_pace_per_40 * (games_played - 1) + row['PACE/40']) / games_played,
                        (current_pie * (games_played - 1) + row['PIE']) / games_played
                    ]

                    # Update the table with the new averages
                    update_query = sql.SQL("""
                        UPDATE team_allowed_avg
                        SET games_played = %s, pts = %s, reb = %s, oreb = %s, dreb = %s, ast = %s, pf = %s, stl = %s, tov = %s, blk = %s,
                            fga = %s, fgm = %s, threepa = %s, threepm = %s, fta = %s, ftm = %s,
                            offrtg = %s, defrtg = %s, netrtg = %s, astpercentage = %s, ast_per_to = %s, ast_ratio = %s, orebpercentage = %s, 
                            drebpercentage = %s, rebpercentage = %s, tovpercentage = %s, efgpercentage = %s, tspercentage = %s, 
                            pace = %s, pace_per_40 = %s, pie = %s
                        WHERE team = %s
                    """)

                    cur.execute(update_query, [games_played] + updated_row + [opp])
                


                cur.execute(
                    sql.SQL("SELECT MIN(games_since) FROM team_for_lag WHERE team = %s"),
                    [row['TEAM']]
                )
                min_games_since = cur.fetchone()[0] -1

                if min_games_since is not None:
                    # Step 2: Delete a specific record if needed (adjust logic as per requirements)
            
    # Step 2: Delete a specific record if needed (adjust logic as per requirements)
                    cur.execute(
                        sql.SQL("DELETE FROM team_for_lag WHERE team = %s AND games_since = %s"),
                        [row['TEAM'], min_games_since + 5]
                    )

                # Step 3: Insert the new row into the table
                insert_query = sql.SQL("""
                    INSERT INTO team_for_lag (
                        team, games_since, offrtg, defrtg, netrtg, astpercentage, 
                        ast_per_to, ast_ratio, orebpercentage, drebpercentage, rebpercentage, tovpercentage, 
                        efgpercentage,tspercentage, pace, pace_per_40, pie, pts, 
                        reb, oreb, dreb, ast, pf, stl, 
                        tov, blk, fga, fgm, threepa, threepm, 
                                       fta, ftm
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s, 
                        %s, %s, %s, %s, %s, %s, 
                        %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s, %s, %s, %s
                    )
                    ON CONFLICT (team, games_since)
                    DO NOTHING
                """)

                cur.execute(insert_query, (
                    row['TEAM'], min_games_since, row['OFFRTG'], row['DEFRTG'], row['NETRTG'], row['AST%'], 
                    row['AST/TO'], row['AST RATIO'], row['OREB%'], row['DREB%'], row['REB%'], row['TOV%'], 
                    row['EFG%'], row['TS%'], row['PACE'], row['PACE/40'], row['PIE'], row['PTS'], 
                    row['REB'], row['OREB'], row['DREB'], row['AST'], row['PF'], row['STL'], 
                    row['TOV'], row['BLK'], row['FGA'], row['FGM'], row['3PA'], row['3PM'], 
                    row['FTA'], row['FTM']
                ))

                cur.execute(
                sql.SQL("SELECT MIN(games_since) FROM team_allowed_lag WHERE team = %s"),
                [row['OPP']]
            )
                min_games_since = cur.fetchone()[0] -1 

                if min_games_since is not None:
                    # Step 2: Delete a specific record if needed (adjust logic as per requirements)
                    cur.execute(
                        sql.SQL("DELETE FROM team_allowed_lag WHERE team = %s AND games_since = %s"),
                        [row['OPP'], min_games_since + 5]
                    )
                conn.commit()

                # Step 3: Insert the new row into the table
                insert_query = sql.SQL("""
                    INSERT INTO team_allowed_lag (
                        team, games_since, offrtg, defrtg, netrtg, astpercentage, ast_per_to, ast_ratio,
                        orebpercentage, drebpercentage, rebpercentage, tovpercentage, efgpercentage,
                        tspercentage, pace, pace_per_40, pie, pts, reb, oreb, dreb, ast, pf, stl, tov,
                        blk, fga, fgm, threepa, threepm, fta, ftm
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                                       %s,%s
                    )
                    ON CONFLICT (team, games_since)
                    DO NOTHING
                """)


                cur.execute(insert_query, (
                    row['TEAM'], min_games_since, row['OFFRTG'], row['DEFRTG'], row['NETRTG'], row['AST%'], 
                    row['AST/TO'], row['AST RATIO'], row['OREB%'], row['DREB%'], 
                    row['REB%'], row['TOV%'], row['EFG%'], row['TS%'], 
                    row['PACE'], row['PACE/40'], row['PIE'], row['PTS'], row['REB'], row['OREB'], 
                    row['DREB'], row['AST'], row['PF'], row['STL'], row['TOV'], row['BLK'], row['FGA'], 
                    row['FGM'], row['3PA'], row['3PM'], row['FTA'], row['FTM']

                ))
                cur.execute(
                sql.SQL("SELECT MIN(games_since) FROM matchup WHERE team = %s AND opp = %s"),
                [row['TEAM'], row['OPP']]
                )
                min_games_since = cur.fetchone()[0] -1 

                if min_games_since is not None:
                    # Step 2: Delete a specific record if needed (adjust logic as per requirements)
                    cur.execute(
                        sql.SQL("DELETE FROM matchup WHERE team = %s AND opp = %s AND games_since = %s"),
                        [row['TEAM'], row['OPP'], min_games_since + 4]
                    )
                # Step 3: Insert the new row into the table
                insert_query = sql.SQL("""
                    INSERT INTO matchup (
                        team, opp, games_since, fga, fgm, threepa, threepm, fta, ftm, 
                        pts, reb, oreb, dreb, ast, tov, pf, stl, blk, pace_per_40, pace, pie
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                    )
                    ON CONFLICT (team, opp, games_since)
                    DO NOTHING
                """)

                cur.execute(insert_query, (
                    row['TEAM'], row['OPP'], min_games_since, row['FGA'], row['FGM'], row['3PA'], 
                    row['3PM'], row['FTA'], row['FTM'], row['PTS'], row['REB'], row['OREB'], 
                    row['DREB'], row['AST'], row['TOV'], row['PF'], row['STL'], row['BLK'], 
                    row['PACE/40'], row['PACE'], row['PIE']
                ))


            for index,row in pos_df.iterrows():
                team = row['Team']
                pos = row['pos']
                cur.execute(
                sql.SQL("""
                    SELECT games_played, pts, reb, oreb, dreb, fga, ast
                    FROM pos_allowed
                    WHERE team = %s AND pos = %s
                """),
                [team, pos]
            )

                result = cur.fetchone()

                # If the team and pos exist in the table, update the averages
                if result:
                    (
                        games_played, current_pts, current_reb, current_oreb, current_dreb, current_fga, current_ast
                    ) = result

                    # Update games played and calculate new averages
                    games_played += 1
                    updated_row = [
                        (current_pts * (games_played - 1) + row['PTS']) / games_played,
                        (current_reb * (games_played - 1) + row['REB']) / games_played,
                        (current_oreb * (games_played - 1) + row['OREB']) / games_played,
                        (current_dreb * (games_played - 1) + row['DREB']) / games_played,
                        (current_fga * (games_played - 1) + row['FGA']) / games_played,
                        (current_ast * (games_played - 1) + row['AST']) / games_played
                    ]
                    
                    # Prepare the update query
                    cur.execute(
                        sql.SQL("""
                            UPDATE pos_allowed
                            SET games_played = %s, pts = %s, reb = %s, oreb = %s, dreb = %s, fga = %s, ast = %s
                            WHERE team = %s AND pos = %s
                        """),   
                        [
                            games_played, updated_row[0], updated_row[1], updated_row[2],
                            updated_row[3], updated_row[4], updated_row[5], team, pos
                        ]
                    )
                    cur.execute(
                    sql.SQL("SELECT MIN(games_since) FROM pos_allowed_lag WHERE team = %s AND pos = %s"),
                    [row['Team'], row['pos']]
                )
                    min_games_since = cur.fetchone()[0] - 1

                    if min_games_since is not None:
                        # Step 2: Delete a specific record if needed (adjust logic as per requirements)
                        cur.execute(
                            sql.SQL("DELETE FROM pos_allowed_lag WHERE team = %s AND pos = %s AND games_since = %s"),
                            [row['Team'], row['pos'], min_games_since + 5]
                        )

                    # Step 3: Insert the new row into the table
                    insert_query = sql.SQL("""
                        INSERT INTO pos_allowed_lag (
                            team, games_since, pos, pts, reb, oreb, dreb, fga, ast
                        ) VALUES (
                            %s, %s, %s, %s, %s, %s, %s, %s, %s
                        )
                        ON CONFLICT (team, pos, games_since)
                        DO NOTHING
                    """)

                    cur.execute(insert_query, (
                        row['opp'], min_games_since, row['pos'], row['PTS'], row['REB'], row['OREB'], 
                        row['DREB'], row['FGA'], row['AST']
                    ))

            conn.commit()
        

        if close:
            cur.close()
            conn.close()
                






