import requests
import time
import csv
from datetime import datetime
import os

def get_prices(crypto_ids, currency="usd", retries=3):
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        'ids': ",".join(crypto_ids),
        'vs_currencies': currency
    }

    for attempt in range(retries):
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status() # Check for HTTP errors
            data = response.json()
            print("[INFO] API Response:", data)
            return data
        except requests.exceptions.HTTPError as e:
            if response.status_code == 429: #rage limit reached
                print(f"[!] Rate limit hit, retrying in {attempt + 1}0 seconds...")
                time.sleep((attempt + 1) * 10) # wait longer with each retry
            else:
                print(f"[!] Error fetching prices: {e}")
                return{}

def track_prices(crypto_ids, currency="usd", interval=10, duration=60):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    writers = {}
    files = {}

    # Open a separate CSV file for each coin
    for coin in crypto_ids:
        filename = os.path.join(script_dir, f"{coin}_{currency}_log.csv")
        file = open(filename, mode="w", newline="", encoding="utf-8")
        writer = csv.writer(file)
        writer.writerow(["Timestamp", f"{coin}_{currency}"])  # Header
        writers[coin] = writer
        files[coin] = file

    start_time = time.time()
    while time.time() - start_time < duration:
        data = get_prices(crypto_ids, currency)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # ✅ Full timestamp

        for coin in crypto_ids:
            price = data.get(coin, {}).get(currency)
            if price is not None:
                print(f"[{timestamp}] {coin.capitalize()}: {price} {currency.upper()}")
                writers[coin].writerow([timestamp, price])
            else:
                print(f"[{timestamp}] Failed to get price for {coin}")

        print("-" * 50)
        time.sleep(interval)

    # Close all files
    for file in files.values():
        file.close()

# 🔁 Start the tracker
crypto_list = ["bitcoin", "ethereum", "dogecoin"]
track_prices(crypto_list, currency="usd", interval=30, duration=300)