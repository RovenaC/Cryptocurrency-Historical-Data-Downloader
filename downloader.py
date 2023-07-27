import requests
import pandas as pd
from datetime import datetime, timedelta

class CryptocurrencyHistoricalDataDownloader:
    def __init__(self, api_base_url):
        self.api_base_url = api_base_url

    def download_historical_data(self, cryptocurrency, start_date, end_date):
        # Format the start and end dates
        start_date = self.format_date(start_date)
        end_date = self.format_date(end_date)

        # Make API call to get historical data
        url = f"{self.api_base_url}/coins/{cryptocurrency}/market_chart/range"
        params = {
            'vs_currency': 'usd',  # Replace with your preferred currency
            'from': start_date,
            'to': end_date
        }
        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame(data['prices'], columns=['timestamp', 'price'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df.set_index('timestamp', inplace=True)
            return df
        else:
            print("Error downloading data:", response.text)
            return None

    def format_date(self, date_str):
        # Format date string to match CoinGecko API format
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        return int(date_obj.timestamp() * 1000)

# Example usage:

# Define CoinGecko API base URL
api_base_url = "https://api.coingecko.com/api/v3"

# Create an instance of CryptocurrencyHistoricalDataDownloader
downloader = CryptocurrencyHistoricalDataDownloader(api_base_url)

# Download historical data for Bitcoin (BTC) from 2023-01-01 to 2023-07-01
start_date = "2023-01-01"
end_date = "2023-07-01"
btc_historical_data = downloader.download_historical_data("bitcoin", start_date, end_date)

# Save the data to a CSV file
if btc_historical_data is not None:
    btc_historical_data.to_csv("bitcoin_historical_data.csv")
    print("Historical data downloaded and saved successfully.")
