import pandas as pd
import requests
from urllib.parse import quote
import time

df = pd.read_csv('C:/Users/John/Desktop/Notebooks/clean.csv')

unique_games = df['title'].unique()

game_details = []

def fetch_game_details(title, api_key):
    url = f"https://api.rawg.io/api/games?key={api_key}&search={quote(title)}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['results']:
            game_info = data['results'][0]
            platforms = [platform['platform']['name'] for platform in game_info['platforms']]
            tags = [tag['name'] for tag in game_info['tags'] if tag['language'] == 'eng']
            return {
                'title': title,
                'platforms': ', '.join(platforms),
                'tags': ', '.join(tags)
            }
    return None

api_key = '4915b9306c824a47a1b6765e400fb02c'

for game in unique_games:
    details = fetch_game_details(game, api_key)
    if details:
        game_details.append(details)
        print("Added details for: " + game)
    time.sleep(2)

details_df = pd.DataFrame(game_details)


details_df.to_csv('C:/Users/John/Desktop/Notebooks/game_details_tags.csv', index=False)
