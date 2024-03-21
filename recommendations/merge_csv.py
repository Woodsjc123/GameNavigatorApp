import pandas as pd

columns = [
    'userID', 'Title', 'hours',
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


def clean_title(title):
    title = str(title).lower()
    for char in [":", ";", "'", "."]:
        title = title.replace(char, "")
    return title

df_users = pd.read_csv('C:\\Users\\John\\Desktop\\Notebooks\\clean.csv')  
df_games = pd.read_csv('C:\\Users\\Woods\\University\\FYP\\games-features.csv') 


df_users['Title'] = df_users['Title'].apply(clean_title)
df_games['QueryName'] = df_games['QueryName'].apply(clean_title)
df_games['ResponseName'] = df_games['ResponseName'].apply(clean_title)


df_merged_primary = pd.merge(df_users, df_games, left_on='Title', right_on='QueryName', how='left')


no_match = df_merged_primary['QueryName'].isnull()


df_secondary = pd.merge(df_users[no_match], df_games, left_on='Title', right_on='ResponseName', how='left')


df_final = pd.concat([df_merged_primary.dropna(subset=['QueryName']), df_secondary])


df_final = df_final.loc[:,~df_final.columns.duplicated()].copy()

df_final_selected = df_final[columns].copy()


df_final_selected = df_final_selected.drop_duplicates()


df_final_selected.to_csv('final_merged_data.csv', index=False)