from __future__ import absolute_import
from sqlalchemy import create_engine
import pandas as pd

# Read data
data_url = 'https://download-data.deutschebahn.com/static/datasets/haltestellen/D_Bahnhof_2020_alle.CSV'

df = pd.read_csv(data_url, sep=';', decimal=',')
print(df)
# First, drop the "Status" column
df = df.drop(['Status'], axis=1)

# Drop rows with invalid values
valid_verkehr = ["FV", "RV", "nur DPN"]
df = df[df['Verkehr'].isin(valid_verkehr)]

df = df[(df['Laenge'] >= -90) & (df['Laenge'] <= 90) & (df['Breite'] >= -90) & (df['Breite'] <= 90)]

df = df[df['IFOPT'].str.contains(r'^[A-Za-z]{2}:\d*:\d*(?::\d*)?$', na=False)]

df = df.dropna()
print(df)
# Convert "Betreiber_Nr" column to integer
df["Betreiber_Nr"] = df["Betreiber_Nr"].astype(int)

# Create the engine without printing execution details
engine = create_engine("sqlite:///trainstops.sqlite", echo=False)
df.to_sql('trainstops', engine, if_exists='replace', index=False)
