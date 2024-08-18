import requests
import pandas as pd
import csv

# Step 1: Data Retrieval
url = "https://download-data.deutschebahn.com/static/datasets/haltestellen/D_Bahnhof_2020_alle.CSV"
print(url)
def fetch_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print("Failed to fetch data")
        return None

# Step 2: Data Processing
def process_data(raw_data):
    # Assuming raw_data contains the CSV content fetched from the URL
    # Use pandas to read the CSV data into a DataFrame
    df = pd.read_csv(pd.compat.StringIO(raw_data), delimiter=';')  # Adjust delimiter if needed
    # Perform data cleaning, preprocessing, or transformations as needed
    # For example:
    # df_cleaned = df.dropna()  # Remove rows with missing values
    return df

# Step 3: Data Storage
def store_data(df):
    # Save processed data to a CSV file or a database
    at=df.to_csv('processed_data.csv', index=False)  # Save as CSV without index
    print(df)


"""# Putting it all together
def run_pipeline():
    # Fetch data
    raw_data = fetch_data(url)
    if raw_data:
        # Process data
        processed_data = process_data(raw_data)
        # Store data
        store_data(processed_data)
        print("Data pipeline executed successfully!")
    else:
        print("Pipeline execution failed.")

# Step 4: Automation (Run the pipeline)
run_pipeline()  # Execute the pipeline"""
