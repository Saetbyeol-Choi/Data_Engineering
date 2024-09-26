import pandas as pd

df = pd.read_csv('C:/Users/sbyeo/MSDS/Data_Engineering/etl_project_2/data/cleaned_spotify_data.csv')
print(df.head())  # Display the first few rows
print(df[['streams', 'in_spotify_playlists']].max())

