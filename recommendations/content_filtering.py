import pandas as pd
import numpy as np
from scipy.stats import spearmanr
import networkx as nx
import community as community_louvain


games_df = pd.read_csv('merged_data.csv')

games_df.head()

boolean_columns = [col for col in games_df.columns if 'Category' in col or 'GenreIs' in col or 'IsFree' in col]
for col in boolean_columns:
    games_df[col] = games_df[col].astype(int)


games_df['hours'] = games_df['hours'] / games_df['hours'].max()
games_df['PriceFinal'] = games_df['PriceFinal'] / games_df['PriceFinal'].max()


features = [col for col in games_df.columns if col not in ['userID', 'Title']]
features_matrix = games_df[features].values


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


def get_recommendations(game_title, top_n=5):

    game_index = games_df[games_df['title'] == game_title].index[0]
    game_community = partition[game_index]
    

    community_games_indices = [game for game, community in partition.items() if community == game_community]    


    # available_games_indices = [
    #     index for index in community_games_indices 
    #     if any(platform in user_platforms for platform in games_df.iloc[index]['platforms'])
    # ]

    scores = []
    for game in community_games_indices:
        if game != game_index:
            score = spearman_correlation_matrix[game_index, game]
            scores.append((game, score))
    

    scores.sort(key=lambda x: x[1], reverse=True)
    

    recommended_games_indices = [game[0] for game in scores[:top_n]]
    recommended_games = games_df.iloc[recommended_games_indices]
    
    return recommended_games['title'].tolist()


recommended_games = get_recommendations('the elder scrolls v skyrim')
print(recommended_games)