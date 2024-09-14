import json
import os
import warnings
from tensorflow.keras.models import load_model
import pickle
import database

# Suppress specific warnings
warnings.filterwarnings("ignore", category=UserWarning, message="pandas only supports SQLAlchemy")

# Define the absolute path for the 'data' directory outside of the current folder
DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'public', 'data'))

# Ensure the 'public/data' directory exists
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

def generate_predictions():
    home_set = set(('MIN', 'ATL', 'DAL', 'IND', 'PHO'))
    models = []
    stat_dict = {'Offensive Rebounds': 0, 'Defensive Rebounds': 1, 'Points': 2, 'Pts+Rebs+Asts': 3, 'FG Attempted': 4,
                 'Rebounds': 5, 'Assists': 6}

    for model in ['oreb', 'dreb', 'pts', 'pra', 'fga', 'reb', 'ast']:
        loaded_model = load_model(f'nn_{model}_4.keras')
        with open(f'xgb_{model}.pkl', 'rb') as f:
            pipeline_loaded = pickle.load(f)
        models.append((loaded_model, pipeline_loaded))

    db = database.Database()
    with open('prizepick_lines.txt', 'r') as file:
        text = file.read()
        lines = db.get_teams(text)

    prediction_results = []
    for _, row in lines.iterrows():
        try:
            if row['attributes.stat_type'] not in stat_dict:
                continue
            player = row['player'].replace("'", '').lower().title()
            team = row['team']
            opp = row['opp']
            nn, xgb = models[stat_dict[row['attributes.stat_type']]]

            home = 1 if team in home_set else 0

            un_aligned = db.get_row(player, team, opp, home, ['pts', 'reb', 'ast', 'oreb', 'dreb', 'fga'], season=28, close=False)
            aligned = db.realign_df(un_aligned)

            prediction_nn = nn.predict(aligned)
            prediction_xgb = xgb.predict(aligned)
            prediction_val = .4 * prediction_nn + .6 * prediction_xgb

            Over_Under = 'under' if prediction_val < float(row['attributes.line_score']) else 'over'

            prediction = {
                'name': player,
                'team': team,
                'prediction': round(float(prediction_val[0]), 2),
                'line': float(row['attributes.line_score']),
                'stat': row['attributes.stat_type'],
                'odds': 'none',
                'book': 'pp',
                'OU': Over_Under
            }

            prediction_results.append(prediction)

        except Exception as e:
            print(e)

    # Save predictions to the JSON file in the 'data' directory
    try:
        predictions_path = os.path.join(DATA_DIR, 'predictions.json')
        with open(predictions_path, 'w') as json_file:
            json.dump(prediction_results, json_file, indent=2)
        print(f"Predictions saved to {predictions_path}")
    except Exception as e:
        print(f"Error saving predictions: {e}")

if __name__ == '__main__':
    generate_predictions()
