# This program calculates the cosine similarity of the clean csv file and saves it to a csv

import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.model_selection import train_test_split
import json


df = pd.read_csv('C:\\Users\\John\\Desktop\\Notebooks\\clean.csv', header=0, names=["User", "Game", "PlayTime"])


unique_users = df['User'].unique()
train_users, test_users = train_test_split(unique_users, test_size=0.2, random_state=21)


with open('train_users.json', 'w') as f:
    json.dump(train_users.tolist(), f)

with open('test_users.json', 'w') as f:
    json.dump(test_users.tolist(), f)


train_df = df[df['User'].isin(train_users)]
test_df = df[df['User'].isin(test_users)]


matrix = train_df.pivot_table(index='User', columns='Game', values='PlayTime', fill_value=0)



def rating(playtime):
    frequency = playtime / playtime.sum()
    return 4 * (1 - np.exp(-frequency.cumsum().shift(fill_value=0))) + 1




implicit_matrix = matrix.apply(rating, axis=1)


cosine_sim = cosine_similarity(implicit_matrix)
cosine_sim_df = pd.DataFrame(cosine_sim, index=implicit_matrix.index, columns=implicit_matrix.index)


cosine_sim_df.to_csv('cosine_similarity.csv')
