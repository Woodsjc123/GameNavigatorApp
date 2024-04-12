import pandas as pd
import numpy as np
import networkx as nx
from scipy.stats import spearmanr
from concurrent.futures import ThreadPoolExecutor



games_df = pd.read_csv('.\\csv\\clean_games_features.csv')

# Convert true or false values to 0 or 1
boolean_columns = [col for col in games_df.columns if 'Category' in col or 'GenreIs' in col or 'IsFree' in col]
for col in boolean_columns:
    games_df[col] = games_df[col].astype(int)


games_df['hours'] = games_df['hours'] / games_df['hours'].max()
games_df['PriceFinal'] = games_df['PriceFinal'] / games_df['PriceFinal'].max()


features = [col for col in games_df.columns if col not in ['userID', 'Title']]
features_matrix = games_df[features].values



batch_size = 1000  


num_games = features_matrix.shape[0]
num_batches = int(np.ceil(num_games / batch_size))


def process_batch(batch_start, batch_end):
    corr_matrix = np.zeros((num_games, batch_end - batch_start))
    for i in range(num_games):
        for j in range(batch_start, batch_end):
            if i < j: 
                correlation, p_value = spearmanr(features_matrix[i], features_matrix[j])
                
                if p_value < 0.05 and correlation > 0.9:
                    corr_matrix[i, j - batch_start] = correlation
                else:
                    corr_matrix[i, j - batch_start] = 0  

    return corr_matrix



spearman_correlation_matrix = np.zeros((num_games, num_games))


for batch_num in range(num_batches):
    batch_start = batch_num * batch_size
    batch_end = min((batch_num + 1) * batch_size, num_games)
    
    with ThreadPoolExecutor(max_workers=4) as executor: 
        corr_matrix = list(executor.map(process_batch, [batch_start], [batch_end]))[0]


    spearman_correlation_matrix[:num_games, batch_start:batch_end] = corr_matrix


spearman_correlation_matrix[spearman_correlation_matrix < 0.9] = 0
i_upper = np.triu_indices(num_games, 1)
spearman_correlation_matrix[i_upper[1], i_upper[0]] = spearman_correlation_matrix[i_upper]


np.save('spearman_correlation_matrix.npy', spearman_correlation_matrix)