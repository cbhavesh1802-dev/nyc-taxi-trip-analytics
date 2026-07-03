import sqlite3
import pandas as pd
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
DB_PATH = os.path.join(PROJECT_ROOT, "data", "taxi_analytics.db")
SQL_DIR = SCRIPT_DIR
OUT_DIR = os.path.join(PROJECT_ROOT, "outputs")
os.makedirs(OUT_DIR, exist_ok=True)

conn = sqlite3.connect(DB_PATH)

queries = {
    "trip_volume_by_hour.csv": "01_trip_volume_by_hour.sql",
    "trip_volume_by_dow.csv": "02_trip_volume_by_dow.sql",
    "fare_tip_by_payment_type.csv": "03_fare_tip_by_payment_type.sql",
    "speed_by_hour.csv": "04_speed_by_hour.sql",
    "distance_distribution.csv": "05_distance_distribution.sql",
}

for out_name, sql_file in queries.items():
    with open(os.path.join(SQL_DIR, sql_file)) as f:
        query = f.read()
    df = pd.read_sql_query(query, conn)
    out_path = os.path.join(OUT_DIR, out_name)
    df.to_csv(out_path, index=False)
    print(f"{out_name}: {len(df)} rows -> {out_path}")

conn.close()
