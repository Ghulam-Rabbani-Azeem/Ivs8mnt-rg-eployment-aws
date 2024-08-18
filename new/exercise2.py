import pandas as pd
import sqlite3

# Fetch data from the URL
url = "https://download-data.deutschebahn.com/static/datasets/haltestellen/D_Bahnhof_2020_alle.CSV"

# Read CSV data into a DataFrame
df = pd.read_csv(url, sep=';', decimal=',')
print(df)

# Dropping the 'Status' column
df.drop(columns=['Status'], inplace=True) 
print(df)

# Filtering rows with valid values
   
# Drop rows with invalid values
# # Convert string columns 'Laenge' and 'Breite' to numeric (float)
df['Laenge'] = df['Laenge'].str.replace(',', '.').astype(float)
df['Breite'] = df['Breite'].str.replace(',', '.').astype(float)

# Filter rows based on valid coordinates and other conditions
valid_verkehr = ["FV", "RV", "nur DPN"]
valid_coordinates = (-90, 90)

df = df[
    (df['Verkehr'].isin(valid_verkehr)) &
    (df['Laenge'].between(*valid_coordinates)) &
    (df['Breite'].between(*valid_coordinates)) &
    (df['IFOPT'].str.contains(r'^[A-Za-z]{2}:\d*:\d*(?::\d*)?$', na=False))
]

df = df.dropna()
print(df)


# Connect to SQLite database
conn = sqlite3.connect('trainstops.sqlite')
cursor = conn.cursor()

# Create the "trainstops" table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS trainstops (
        EVA_NR BIGINT,
        DS100 TEXT,
        IFOPT TEXT,
        NAME TEXT,
        Verkehr TEXT,
        Laenge FLOAT,
        Breite FLOAT,
        Betreiber_Name TEXT,
        Betreiber_Nr INT
    )
''')

# Insert data into the "trainstops" table
df.to_sql('trainstops', con=conn, index=False, if_exists='replace')

# Commit changes and close connection
conn.commit()
conn.close()

print("Data successfully written to SQLite database 'trainstops.sqlite' in table 'trainstops'.")
