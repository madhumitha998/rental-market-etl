import os
import pandas as pd
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas
from dotenv import load_dotenv

# 1. Load our secret keys
load_dotenv()

def teleport_data():
    # 2. Connect to the Cloud Warehouse
    print("☁️  Connecting to Snowflake...")
    conn = snowflake.connector.connect(
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        warehouse="COMPUTE_WH",
        database="RENTAL_DB",
        schema="RAW"
    )

    try:
        # 3. Read our local CSV
        df = pd.read_csv("data/raw_rentals.csv")

        # Standardize column names to match Snowflake (UPPERCASE)
        df.columns = [x.upper() for x in df.columns] 

        # Replace any empty/NaN values with None so Snowflake handles them as NULL
        df = df.where(pd.notnull(df), None)

        print(f"📄 Found {len(df)} rows. Sending to Snowflake...")

        # 4. Push the data to the RAW table we built in Snowflake
        print("🚀 Teleporting data to the cloud...")
        success, nchunks, nrows, _ = write_pandas(
            conn, 
            df, 
            table_name='TROY_RENTALS',
            database='RENTAL_DB',
            schema='RAW'
        )

        if success:
            print(f"✅ Mission Accomplished! {nrows} rows are now in Snowflake.")
        
    finally:
        conn.close()

if __name__ == "__main__":
    teleport_data()