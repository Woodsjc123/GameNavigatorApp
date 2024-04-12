# This program calculates communities within the spearman corrleation coeffecient and saves them along with
# the community pagerank scores

import pandas as pd
import numpy as np
import networkx as nx
import json
import community


spearman_correlation_matrix = np.load('filtered_spearman_correlation_matrix.npy')


games_df = pd.read_csv('.\\csv\\final_merged_data.csv')


similarity_graph = nx.from_numpy_array(spearman_correlation_matrix)

# Find communities
partition = community.best_partition(similarity_graph, resolution=1.8)


community_pagerank_scores = {}
representative_games = {}

for community_id in set(partition.values()):
    
    community_nodes = [nodes for nodes in partition.keys() if partition[nodes] == community_id]

    subgraph = similarity_graph.subgraph(community_nodes)

    pagerank_scores = nx.pagerank(subgraph)

    community_pagerank_scores[community_id] = pagerank_scores

    sorted_games = sorted(pagerank_scores, key=pagerank_scores.get, reverse=True)


    top_games = sorted_games[:min(10, len(sorted_games))]
    print(f"Community {community_id}:")

    for rank, game_index in enumerate(top_games, start=1):
        game_title = games_df.iloc[game_index]['Title']
        print(f"{rank}: {game_title}")
    print("\n")



with open('F:\\TUD\\FYP\\recommendations\\json\\community_partition_100.json', 'w') as file:
    json.dump(partition, file)

with open('F:\\TUD\\FYP\\recommendations\\json\\community_pagerank_scores_100.json', 'w') as file:
    json.dump(community_pagerank_scores, file)


