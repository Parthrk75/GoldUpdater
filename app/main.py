import io
import pandas as pd
import yfinance as yf
import requests
import base64
from datetime import datetime

# GitHub repository details
GITHUB_REPO = 'Parthrk75/gold-price-data'  # Replace with your GitHub repo
CSV_FILE_PATH = 'historical_gold_spot_prices.csv'  # Path in GitHub repo
GITHUB_TOKEN = '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'  # Replace with your GitHub token

def update_csv_data():
    gld = yf.Ticker("GLD")
    today = datetime.today().strftime('%Y-%m-%d')

    historical_data = gld.history(period="1d", start="2020-01-01", end=today)

    if historical_data.empty:
        print("No historical data available.")
        return None

    selected_data = historical_data[["Open", "High", "Low", "Close"]]

    scaling_factor = 10.77
    selected_data.loc[:, "Open (Spot Price USD)"] = selected_data["Open"] * scaling_factor
    selected_data.loc[:, "High (Spot Price USD)"] = selected_data["High"] * scaling_factor
    selected_data.loc[:, "Low (Spot Price USD)"] = selected_data["Low"] * scaling_factor
    selected_data.loc[:, "Close (Spot Price USD)"] = selected_data["Close"] * scaling_factor

    selected_data = selected_data.round({"Open (Spot Price USD)": 2, 
                                         "High (Spot Price USD)": 2,
                                         "Low (Spot Price USD)": 2,
                                         "Close (Spot Price USD)": 2})

    selected_data = selected_data.reset_index()
    selected_data["Date"] = selected_data["Date"].dt.strftime('%d-%m-%Y 00:00')

    selected_data = selected_data[["Date", "Open (Spot Price USD)", "High (Spot Price USD)", "Low (Spot Price USD)", "Close (Spot Price USD)"]]

    return selected_data

def get_github_file_content():
    url = f'https://api.github.com/repos/{GITHUB_REPO}/contents/{CSV_FILE_PATH}'
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    response = requests.get(url, headers=headers)

    if response.status_code == 404:
        print("File not found on GitHub, creating a new one.")
        return None

    file_content = response.json()
    file_sha = file_content.get('sha', None)
    file_data = base64.b64decode(file_content['content']).decode('utf-8')
    
    df = pd.read_csv(io.StringIO(file_data))
    return df, file_sha

def push_to_github(new_data):
    commit_message = f"Update gold price data: {datetime.today().strftime('%Y-%m-%d')}"

    existing_data_info = get_github_file_content()

    if existing_data_info is None:
        combined_data = new_data
        sha = None
    else:
        existing_data, sha = existing_data_info
        combined_data = pd.concat([existing_data, new_data]).drop_duplicates(subset=["Date"])

    csv_data = combined_data.to_csv(index=False)

    encoded_content = base64.b64encode(csv_data.encode('utf-8')).decode('utf-8')

    payload = {
        'message': commit_message,
        'content': encoded_content,
        'sha': sha if sha else '',
    }

    url = f'https://api.github.com/repos/{GITHUB_REPO}/contents/{CSV_FILE_PATH}'
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    response = requests.put(url, headers=headers, json=payload)

    if response.status_code in [200, 201]:
        print("File pushed to GitHub successfully.")
    else:
        print(f"Failed to push file to GitHub: {response.status_code}, {response.json()}")

def main():
    new_data = update_csv_data()
    if new_data is not None:
        push_to_github(new_data)

if __name__ == '__main__':
    main()
