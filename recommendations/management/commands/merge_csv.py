import pandas as pd


def clean_title(title):
    title = str(title).lower().strip()

    for char in [":", "_", ";", "&", "'", ".", ",", "-", "(", ")", "/", " "]:
        title = title.replace(char, "")
    return title


df_users = pd.read_csv('F:\\TUD\\FYP\\recommendations\csv\clean.csv')  
df_games = pd.read_csv('F:\\TUD\\FYP\\recommendations\csv\games-features.csv') 


df_users['title'] = df_users['title'].apply(clean_title)
df_games['QueryName'] = df_games['QueryName'].apply(clean_title)
df_games['ResponseName'] = df_games['ResponseName'].apply(clean_title)


df_merged = pd.merge(df_users, df_games, left_on='title', right_on='QueryName', how='left')


no_match = df_merged['QueryName'].isnull()
df_secondary = pd.merge(df_users[no_match], df_games, left_on='title', right_on='ResponseName', how='left')


df_final = pd.concat([df_merged.dropna(subset=['QueryName']), df_secondary])


columns = [
    'userID', 'title', 'hours',
    'RequiredAge', 'IsFree',
    'CategorySinglePlayer', 'CategoryMultiplayer', 'CategoryCoop',
    'CategoryMMO', 'CategoryInAppPurchase', 'CategoryIncludeSrcSDK',
    'CategoryIncludeLevelEditor', 'CategoryVRSupport',
    'GenreIsNonGame', 'GenreIsIndie', 'GenreIsAction',
    'GenreIsAdventure', 'GenreIsCasual', 'GenreIsStrategy',
    'GenreIsRPG', 'GenreIsSimulation', 'GenreIsEarlyAccess',
    'GenreIsFreeToPlay', 'GenreIsSports', 'GenreIsRacing',
    'GenreIsMassivelyMultiplayer', 'PriceInitial', 'PriceFinal'
]


df_final = df_final.loc[:, ~df_final.columns.duplicated()].copy()
df_final_selected = df_final[columns].copy()


df_final_selected = df_final_selected.drop_duplicates(subset=['userID', 'title'])


df_final_selected = df_final_selected.dropna()


df_final_selected.to_csv('final_merged_data.csv', index=False)