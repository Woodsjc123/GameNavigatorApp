from django.contrib.auth.models import User
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.model_selection import train_test_split


# Collaborative based on play count
df = pd.read_csv('C:\\Users\\John\\Desktop\\Notebooks\\clean.csv', header=0, names=["User", "Game", "PlayTime"])

unique_users = df['User'].unique()
train_users, test_users = train_test_split(unique_users, test_size=0.2, random_state=27)

train_df = df[df['User'].isin(train_users)]
test_df = df[df['User'].isin(test_users)]


matrix = train_df.pivot_table(index='User', columns='Game', values='PlayTime', fill_value=0)
matrix_std = matrix.apply(lambda x: (x - np.mean(x)) / (np.max(x) - np.min(x)), axis=1)
cosine_sim = cosine_similarity(matrix_std)
cosine_sim_df = pd.DataFrame(cosine_sim, index=matrix_std.index, columns=matrix_std.index)


def generate_recommendations(user_id, top_n=5):
    if user_id not in cosine_sim_df.index:
        print(f"User {user_id} not found.")
        return []

    similar_users = cosine_sim_df[user_id].sort_values(ascending=False)[1:top_n+1]
    
    
    recommended_games = pd.Series(dtype=np.float64)
    for similar_user in similar_users.index:
        similar_user_games = matrix.loc[similar_user]
        recommended_games = recommended_games.add(similar_user_games, fill_value=0)


    played_games = matrix.loc[user_id]
    recommended_games = recommended_games[~recommended_games.index.isin(played_games[played_games > 0].index)]


    recommended_games = recommended_games.sort_values(ascending=False)[:top_n]
    
    return list(recommended_games.index)


# user_id = '' 
# recommended_games = generate_recommendations(user_id)
# print(f"Recommended games for user: {recommended_games}")
