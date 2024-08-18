import sqlite3
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Ridge, Lasso
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor , VotingRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import joblib
import os
from data import data_generating

class Stock:
   
    def __init__(self):
        # Initialize the instance variable to None
        self.voting_system_model = None
        self.dataset = None 

    def data_loader(self):
        # Connect to the SQLite database
        conn = sqlite3.connect('Directory/data.db')  

        # Query to retrieve data from the database (replace 'table_name' with your table name)
        query = "SELECT * FROM stock" 

        # Load data into a DataFrame
        df = pd.read_sql_query(query, conn)

        # Close the connection
        conn.close()

        # Display the DataFrame
        return df 
    
    def data_loader_csv(self,value):
        data_generating_instance=data_generating()
        data_generating_instance.main(value)
        self.dataset = f"{value}_stock_data"   # Assuming this holds the dataset name
        file_path = f"Directory/{self.dataset}.csv"  # Constructing the file path

        df = pd.read_csv(file_path)

        return df

    def preprocessing(self,value):
        # Load data using data_loader method
        data = self.data_loader_csv(value)
        
        # Check for duplicates and drop them
        data.drop_duplicates(inplace=True)

        # Remove rows with null values
        data.dropna(inplace=True)
        
        # Drop 'id' column
        # data.drop(columns=["id"], inplace=True)
        df2 = data[['Date', 'Open', 'Close']]

          
        # Convert 'date' column to datetime and extract features
        df2['Date'] = pd.to_datetime(df2['Date'])
        df2['year'] = df2['Date'].dt.year
        df2['month'] = df2['Date'].dt.month
        df2['day'] = df2['Date'].dt.day
        
        # Drop the original 'date' column
        df2.drop(columns=['Date'], inplace=True)

     
        print('Data = ',df2)
        return df2
    
    def model_training(self,value):
        # Get preprocessed data
        data = self.preprocessing(value)

        # Splitting data into features (X) and target (y)
        target_column = 'Close'  # Replace with your target column name
        X = data.drop(columns=[target_column])
        y = data[target_column]
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # List of base models
        base_models = [
            ('Support Vector Machine (SVM)', SVR()),
            ('Decision Tree', DecisionTreeRegressor()),
            ('Random Forest', RandomForestRegressor()),
            ('Gradient Boosting', GradientBoostingRegressor()),
            ('Ridge', Ridge()),  # Added Ridge regression
            ('Lasso', Lasso())   # Added Lasso regression
          
        ]

        # Store predictions and MSE for base models
        predictions_base_models = {}
        mse_base_models = {}

        for name, model in base_models:
            model.fit(X_train, y_train)  # Train the model
            predictions = model.predict(X_test)  # Make predictions
            predictions_base_models[name] = predictions  # Store predictions for visualization
            mse_base_models[name] = mean_squared_error(y_test, predictions)  # Calculate MSE

        # Initialize base models and create a Voting Regressor
        base_estimators = [(name, model) for name, model in base_models]
        voting_model = VotingRegressor(estimators=base_estimators)

        # Train the Voting Regressor
        voting_model.fit(X_train, y_train)
        print('X_test (First Row):')
        # print(X_test.iloc[0])
        # Evaluate the Voting Regressor
        prediction_meta_model = voting_model.predict(X_test)
        mse_meta_model = mean_squared_error(y_test, prediction_meta_model)

        # save model
        # Directory to save models
        models_dir = 'models'

        # Create the directory if it doesn't exist
        if not os.path.exists(models_dir):
            os.makedirs(models_dir)

       
        file_path = f"{self.dataset}.pkl"  # Constructing the file path


        # Path to save the trained model
        voting_model_path = os.path.join(models_dir, file_path)
        joblib.dump(voting_model, voting_model_path)


        self.voting_system_model=voting_model

        return y_test, predictions_base_models, prediction_meta_model, mse_base_models, mse_meta_model 

    
 
    def visualize_predictions(self, y_test, predictions_base_models, prediction_meta_model, mse_base_models, mse_meta_model):
        plt.figure(figsize=(10, 6))

        # Plotting actual vs predicted for each base model
        for name, preds in predictions_base_models.items():
            plt.scatter(y_test, preds, label=f'{name} Predictions')

        # Plotting actual vs predicted for meta-model
        plt.scatter(y_test, prediction_meta_model, label='Voting Regressor (Meta-model) Predictions', color='black', marker='x')

        plt.xlabel('Actual')
        plt.ylabel('Predicted')
        plt.title('Actual vs Predicted Values')
        plt.legend()
        plt.grid(True)
        plt.show()

        # Display MSE for each model
        print("Mean Squared Error for Base Models:")
        for name, mse in mse_base_models.items():
            print(f"{name}: {mse}")

        print(f"Mean Squared Error for Voting Regressor (Meta-model): {mse_meta_model}")

    def voting_model(self,value):
        predict=self.voting_system_model.predict(value)

        return predict

def main():
    # Instantiate the Stock class
    stock_instance = Stock()
   
    # Call the model_training method for meta-model
    meta_model_mse = stock_instance.model_training()
    print(f"Mean Squared Error for Voting Regressor (Meta-model): {meta_model_mse}")
    
    df = pd.DataFrame([obj])


    data = {
        'Open': [3.03],
        'year': [2024.00],
        'month': [10.00],
        'day': [7.00]
    }

    X_train = pd.DataFrame(data)

    # Print the resulting DataFrame
 
    predicted_value=stock_instance.voting_model(X_train)
      
    

instance=Stock()
instance.model_training('SLP')
