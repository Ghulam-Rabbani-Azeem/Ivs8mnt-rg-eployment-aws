import urllib.request
import pandas as pd
import zipfile
import sqlite3  # Add this line to import sqlite3
import os



# Download and unzip data
zip_url = "https://www.mowesta.com/data/measure/mowesta-dataset-20221107.zip"
zip_file_name = "mowesta-dataset.zip"
extracted_dir = "mowesta-dataset"
urllib.request.urlretrieve(zip_url, zip_file_name)
if os.path.exists(zip_file_name):
    if not os.path.exists(extracted_dir):
        os.makedirs(extracted_dir)
    with zipfile.ZipFile(zip_file_name, 'r') as zip_ref:
        zip_ref.extractall(extracted_dir)
    csv_file_path = os.path.join(extracted_dir, "data.csv")
print("Downloaded and unziped data...")
    
# Reshaping Data
ex4_df = pd.read_csv(csv_file_path, sep=";", decimal=",", index_col=False,usecols=["Geraet", "Hersteller", "Model", "Monat", "Temperatur in °C (DWD)","Batterietemperatur in °C", "Geraet aktiv"])
ex4_df.rename(columns={"Temperatur in °C (DWD)":"Temperatur","Batterietemperatur in °C":"Batterietemperatur"}, inplace=True)
ex4_df=ex4_df.loc[:, :'Geraet aktiv']
print("Reshaped data...")

# Data Transformation
temp_cols = ['Temperatur', 'Batterietemperatur']
ex4_df[temp_cols] = (ex4_df[temp_cols] * 9/5) + 32
print("Data transformed.")

# Data Validation
ex4_df['Hersteller'] = ex4_df['Hersteller'].astype(str)
ex4_df['Model'] = ex4_df['Model'].astype(str)
ex4_df = ex4_df[ex4_df['Geraet'] > 0]
ex4_df = ex4_df[ex4_df['Hersteller'].str.strip() != ""]
ex4_df = ex4_df[ex4_df['Model'].str.strip() != ""]
ex4_df = ex4_df[ex4_df['Monat'].between(1, 12)]
ex4_df = ex4_df[pd.to_numeric(ex4_df['Temperatur'], errors='coerce').notna()]
ex4_df = ex4_df[pd.to_numeric(ex4_df['Batterietemperatur'], errors='coerce').notna()]
ex4_df = ex4_df[ex4_df['Geraet aktiv'].isin(['Ja', 'Nein'])]
print("Data validated.")

# Convert to Database
db_connection = sqlite3.connect("temperatures_db.sqlite")
ex4_df.to_sql('temperatures', db_connection, if_exists='replace', index=False)
db_connection.commit()
db_connection.close()
print("Database created.")
