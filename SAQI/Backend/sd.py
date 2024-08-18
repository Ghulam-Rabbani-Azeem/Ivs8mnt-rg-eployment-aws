import pandas as pd
import os
import sqlite3
from sklearn.tree import DecisionTreeClassifier
import joblib

class sd:
    def __init__(self):
        # Initialize the instance variable to None
        self.dataset_statistics = [] 

    def database(self):
        # Connect to the SQLite database. It will create the database file if it does not exist.
        conn = sqlite3.connect('Directory/data.db')

        # Create a cursor object using the cursor method of the connection object
        cursor = conn.cursor()

        # SQL command to create a table
        create_table_sql = '''CREATE TABLE IF NOT EXISTS standardDeviation (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT,
                                height REAL,
                                sd REAL
                            );'''

        # Execute the SQL command
        cursor.execute(create_table_sql)

        # Commit the changes
        conn.commit()

        # Close the connection
        conn.close()

    def download(self):
       
        # Define a directory containing your CSV files
          
        csv_directory = 'Directory/'

        # Loop through each CSV file in the directory
        for filename in os.listdir(csv_directory):
            if filename.endswith('.csv'):
                # Read the CSV file into a DataFrame
                df = pd.read_csv(os.path.join(csv_directory, filename))
                
                # Convert 'Close' and 'Open' to numeric, coercing errors to NaN
                df['Close'] = pd.to_numeric(df['Close'], errors='coerce')
                df['Open'] = pd.to_numeric(df['Open'], errors='coerce')
                # # Calculate average price change
                average_change = df["Close"] - df["Open"] 
                
                dataset_info = {
                "name": filename,  # Assuming filename represents the dataset name
                "average_change": average_change.mean(),
                "standard_deviation": average_change.std(),
                "high_value": df['High'].max()
            }

            self.dataset_statistics.append(dataset_info)     

        
       
        # Now, you have lists of average_changes, standard_deviations, and high_values for each company
        # You can analyze and categorize companies based on these values.


        return self.dataset_statistics  
    

    def Decision(self):

        filtered_data = [data for data in self.dataset_statistics if not pd.isnull(data['standard_deviation'])]

        # Extracting features and target labels
        X = [[data['standard_deviation']] for data in filtered_data]
        y = [data['name'] for data in filtered_data]

        # Create a decision tree classifier
        clf = DecisionTreeClassifier()

        # Train the classifier on the features and target labels
        clf.fit(X, y)

        # Now,classifier to predict based on a standard deviation value
        print(f"Predicted names for standard deviation: {predicted_names}")
        # Save the trained decision tree model to a file
        model_filename = 'models/decision_tree_model.pkl'
        joblib.dump(clf, model_filename)

        
    def Load_Decision_TREE(self,value):
        # Load the saved decision tree model
        self.download()
        model_filename = 'models/decision_tree_model.pkl'
        loaded_model = joblib.load(model_filename)


        # filtered_data = [data for data in self.dataset_statistics if 
        #                     not pd.isnull(data['standard_deviation']) and 
        #                     data['standard_deviation'] <= value]

        filtered_data = [data for data in self.dataset_statistics if 
        value/2 <= data.get('standard_deviation', float('nan')) <= value]

        # Extracting features for prediction
        X = [[data['standard_deviation']] for data in filtered_data]

        # print(filtered_data)

        # Use the loaded model to make predictions based on the filtered data
        predicted_names = loaded_model.predict(X)

        
        # print(f"Predicted names for stocks with standard deviation <= 2: {predicted_names}")

        return predicted_names


   

# Create an instance of the 'sd' class
sd_instance = sd()

# Call the method using the instance
sd_instance.Load_Decision_TREE(10)
