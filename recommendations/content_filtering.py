import pandas as pd
from datetime import datetime
import numpy as np
from scipy.stats import spearmanr
from sklearn.preprocessing import MultiLabelBinarizer
import networkx as nx
import community as community_louvain


games_data = {
    'title': ['Game A', 'Game B', 'Game C', 'Game D', 'Game E', 'Game F'],
    'genres': [
        ['Action', 'Adventure'], 
        ['Adventure', 'Puzzle'], 
        ['Action', 'RPG'], 
        ['Horror', 'Survival'], 
        ['Action', 'Adventure'], 
        ['Puzzle', 'Strategy']
    ],
    'platforms': [
        ['PC', 'Console'], 
        ['PC'], 
        ['Console', 'Mobile'], 
        ['PC', 'Mobile'], 
        ['Console'], 
        ['PC', 'Console', 'Mobile']
    ],
    'ratings': [4.5, 4.0, 5.0, 3.5, 4.8, 4.2],
    'release_date': [
        datetime(2020, 1, 1), 
        datetime(2020, 6, 1), 
        datetime(2021, 7, 15), 
        datetime(2021, 10, 30), 
        datetime(2022, 3, 22),
        datetime(2021, 12, 1)
    ]
}

games_df = pd.DataFrame(games_data)


mlb_genres = MultiLabelBinarizer()
genre_matrix = mlb_genres.fit_transform(games_df['genres'])


features_matrix = np.hstack([
    genre_matrix,
    games_df[['ratings']].values / games_df['ratings'].max(),
    (games_df['release_date'].dt.year.values[:, None] - games_df['release_date'].dt.year.min()) /
    (games_df['release_date'].dt.year.max() - games_df['release_date'].dt.year.min())
])


spearman_correlation_matrix = np.zeros((features_matrix.shape[0], features_matrix.shape[0]))


for i in range(features_matrix.shape[0]):
    for j in range(features_matrix.shape[0]):
        if i != j:
            correlation, p_value = spearmanr(features_matrix[i], features_matrix[j])
            # Remove all negative values and p values > 0.05
            if correlation > 0 and p_value < 0.05:
                spearman_correlation_matrix[i, j] = correlation
            else:
                spearman_correlation_matrix[i, j] = 0


print(spearman_correlation_matrix)

similarity_graph = nx.from_numpy_array(spearman_correlation_matrix)
partition = community_louvain.best_partition(similarity_graph)


communities = set(partition.values())
representative_games = {}
for community in communities:
    subgraph_nodes = [nodes for nodes in partition if partition[nodes] == community]
    subgraph = similarity_graph.subgraph(subgraph_nodes)
    pagerank = nx.pagerank(subgraph)
    most_representative = max(pagerank, key=pagerank.get)
    representative_games[community] = games_df.iloc[most_representative]['title']


def get_recommendations(game_title, user_platforms, top_n=5):
    game_index = games_df[games_df['title'] == game_title].index[0]
    game_community = partition[game_index]
    

    community_games_indices = [game for game, community in partition.items() if community == game_community]    


    available_games_indices = [
        index for index in community_games_indices 
        if any(platform in user_platforms for platform in games_df.iloc[index]['platforms'])
    ]

    scores = []
    for game in available_games_indices:
        if game != game_index:
            score = spearman_correlation_matrix[game_index, game]
            scores.append((game, score))
    

    scores.sort(key=lambda x: x[1], reverse=True)
    

    recommended_games_indices = [game[0] for game in scores[:top_n]]
    recommended_games = games_df.iloc[recommended_games_indices]
    
    return recommended_games['title'].tolist()


recommended_games = get_recommendations('Game A', 'PC')
print(recommended_games)