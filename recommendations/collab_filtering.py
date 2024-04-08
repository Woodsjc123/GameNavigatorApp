# This program uses collaborative filtering on the clean.csv file to generate an array of video game recommendations
import pandas as pd
import numpy as np
import json


cosine_df = pd.read_csv('.\\csv\\cosine_similarity.csv', index_col=0)


with open('.\\json\\train_users.json', 'r') as f:
    train_users = json.load(f)

with open('.\\json\\test_users.json', 'r') as f:
    test_users = json.load(f)



df = pd.read_csv('C:\\Users\\John\\Desktop\\Notebooks\\clean.csv', header=0, names=["User", "Game", "PlayTime"])
train_df = df[df['User'].isin(train_users)]
matrix = train_df.pivot_table(index='User', columns='Game', values='PlayTime', fill_value=0)



def generate_recommendations(user_id, top_n=5):

    if user_id in train_users:
        
        user_id = int(user_id)

        similar_users = cosine_df.loc[user_id].sort_values(ascending=False)[1:top_n+1]
        
        recommended_games = pd.Series(dtype=np.float64)

        for similar_user in similar_users.index:
            similar_user_games = matrix.loc[int(similar_user)]
            recommended_games = recommended_games.add(similar_user_games, fill_value=0)

        # Exclude the games that the user is listed as having played
        played_games = matrix.loc[user_id]
        recommended_games = recommended_games[~recommended_games.index.isin(played_games[played_games > 0].index)]

        # Sort games
        recommended_games = recommended_games.sort_values(ascending=False)[:top_n]
        
        return list(recommended_games.index)
    
    elif user_id not in cosine_df.index:
        print(f"User {user_id} not found.")
        return
    
    else:
        print(f"User {user_id} is not in the training set.")


# Test
user_id = 199841615  
user_recommendations = generate_recommendations(user_id)
print(user_recommendations)
