import os
import requests
import pandas as pd
from dotenv import load_dotenv

# 1. Load your secret key from the .env file
load_dotenv()
API_KEY = os.getenv("RENTCAST_API_KEY")

def fetch_rentals(zip_code):
    print(f"🚀 Starting the engine for Zip: {zip_code}...")
    
    url = f"https://api.rentcast.io/v1/listings/rental/long-term?zipCode={zip_code}&limit=50"
    headers = {"accept": "application/json", "X-Api-Key": API_KEY}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data)
        
        # Save locally so we don't waste API calls!
        os.makedirs('data', exist_ok=True)
        df.to_csv("data/raw_rentals.csv", index=False)
        
        print(f"✅ Success! Found {len(df)} homes and saved them to data/raw_rentals.csv")
    else:
        print(f"❌ Error: {response.status_code}")

if __name__ == "__main__":
    fetch_rentals("48084") # This is Troy, MI!