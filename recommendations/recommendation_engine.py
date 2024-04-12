import pandas as pd
import json

def get_playtime(user_id, df):
    playtime = df[df['userID'] == user_id]
    return dict(zip(playtime['title'], playtime['hours']))


def load_data():

    with open('F:\\TUD\\FYP\\recommendations\\json\\community_partition_100.json', 'r') as file:
        partition = json.load(file)

    with open('F:\\TUD\\FYP\\recommendations\\json\\community_pagerank_scores_100.json', 'r') as file:
        pagerank_scores = json.load(file)

    return partition, pagerank_scores


def get_recommendations(playtime, pagerank_scores, partition, games_df, top_n=5):
    user_index = [  # Match titles found in games_df and converting to lowercase
        games_df.index[games_df['title'].str.lower() == game_title.lower()].tolist()[0] for game_title in playtime.keys()
        if not games_df[games_df['title'].str.lower() == game_title.lower()].empty
    ]
    
    user_communities = set(partition[str(game_index)] for game_index in user_index if str(game_index) in partition)
    
    game_scores = {}
    for community in user_communities:
        for game_index, score in pagerank_scores[str(community)].items():
            game_index = int(game_index)

            if game_index not in user_index:    # If user has already played game, don't include it
                game_scores[game_index] = score
    

    recommended_games_indeces = sorted(game_scores, key=game_scores.get, reverse=True)[:top_n]


    recommended_games = [games_df.iloc[game_index]['title'] for game_index in recommended_games_indeces if game_index < len(games_df)]

    return recommended_games




# Testing the recommendations for test users
def main():
    games_df = pd.read_csv('.\\csv\\clean.csv')

    with open('.\\json\\test_users.json', 'r') as file:
        test_users = json.load(file)

    test_users = test_users[:10]

    partition, pagerank_scores = load_data()

    for user_id in test_users:
        playtime = get_playtime(user_id, games_df)
        
        recommendations = get_recommendations(playtime, pagerank_scores, partition, games_df, top_n=5)
        
        print(f"Recommendations for user {user_id}: {recommendations}")

if __name__ == "__main__":
    main()