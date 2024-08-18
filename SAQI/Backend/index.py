from implementation import Stock
import pandas as pd
import numpy as np
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request
import json
import joblib
from sd import sd

app = FastAPI()
# Configure CORS
origins = [
    "http://localhost:3000",
    "http://localhost:3000/ratio",
    "http://127.0.0.1:3000/rato",
    "http://127.0.0.1:3000/",
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.post("/add")
async def add_stock(request: Request):
     
    data = await request.json()
    stock_instance=Stock()
    stock_instance.model_training(data['data'])
    print(data['data'])


    return '' # Returning the received data as is



@app.post("/ratio")
async def read_data1(request: Request):
    request_data = await request.json()
    
    sd_instance = sd()
    value = request_data['data']
    input_data = np.array([[value]])
    
    Stocks=sd_instance.Load_Decision_TREE(value)
    print('---------->',Stocks)
    # Assuming you have a NumPy ndarray
    file_names_array = np.array(Stocks)

    # Convert the ndarray to a Python list using tolist()
    file_names_list = file_names_array.tolist()

    # Convert the list to JSON format
    file_names_json = json.dumps(file_names_list)
    data_list = [
        {
         'Open': [3.03],
            'year': [2024.00],
            'month': [1.00],
            'day': [7.00]
        },
      {
         'Open': [3.03],
            'year': [2024.00],
            'month': [2.00],
            'day': [7.00]
        },
        {
         'Open': [3.03],
            'year': [2024.00],
            'month': [3.00],
            'day': [7.00]
        },
        {
         'Open': [3.03],
            'year': [2024.00],
            'month': [4.00],
            'day': [7.00]
        },
        {
         'Open': [3.03],
            'year': [2024.00],
            'month': [5.00],
            'day': [7.00]
        },
        {
         'Open': [3.03],
            'year': [2024.00],
            'month': [6.00],
            'day': [7.00]
        },
        {
         'Open': [3.03],
            'year': [2024.00],
            'month': [7.00],
            'day': [7.00]
        },
         {
         'Open': [3.03],
            'year': [2024.00],
            'month': [8.00],
            'day': [7.00]
        },
        {
         'Open': [3.03],
            'year': [2024.00],
            'month': [9.00],
            'day': [7.00]
        },
         {
         'Open': [3.03],
            'year': [2024.00],
            'month': [10.00],
            'day': [7.00]
        },
         {
         'Open': [3.03],
            'year': [2024.00],
            'month': [11.00],
            'day': [7.00]
        },
        {
         'Open': [3.03],
            'year': [2024.00],
            'month': [12.00],
            'day': [7.00]
        },
    ]


    full_data = []

    for model_name in file_names_list:
        model_name = model_name.split('.')[0]
        model_filename = f'models/{model_name}.pkl'
        loaded_model = joblib.load(model_filename)

      

        prediction = []  # Initialize prediction list for each model
        
        for data_dict in data_list:
            X_train = pd.DataFrame(data_dict)
            predicted_values = loaded_model.predict(X_train)
            prediction.append(predicted_values)
            print(f"Predicted values for model '{model_name}': {predicted_values}")

        stock_info = {
            'name': model_name,
            'prediction': prediction
        }
        full_data.append(stock_info)

    # Convert the list of dictionaries into a DataFrame
    full_data_df = pd.DataFrame(full_data)
   

    full_data_df = full_data_df.to_json(orient='records')
    print(full_data_df)     
        
    
    return full_data_df




@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}
