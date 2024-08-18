import yfinance as yf
import os
class data_generating:
    
    def fetch_stock_data(self,symbol, start_date, end_date):
        # Fetching data using yfinance
        stock_data = yf.download(symbol, start=start_date, end=end_date)
        return stock_data

    def save_data_to_csv(self,data, directory, filename):
        if not os.path.exists(directory):
            os.makedirs(directory)
        filepath = os.path.join(directory, filename)
        data.to_csv(filepath)
        print(f"Data saved successfully to {filepath}")

    def main(self,company_symbol):
        start_date = '2023-01-01'  # Start date for historical data
        end_date = '2023-12-31'    # End date for historical data
        directory = 'Directory'  # Directory to save the CSV file
        filename = f"{company_symbol}_stock_data.csv"  # Filename for the CSV file

        # Fetching historical stock data for the specified company
        company_data = self.fetch_stock_data(company_symbol, start_date, end_date)

        # Saving data to CSV file in the specified directory
        self.save_data_to_csv(company_data, directory, filename)




dg=data_generating()
company_symbol = 'ACBM'  # Replace 'TSLA' with the desired company symbol
dg.main(company_symbol)
#