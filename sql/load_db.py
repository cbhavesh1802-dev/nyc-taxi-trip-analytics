"""
Loads one or more NYC Yellow Taxi trip CSVs into SQLite, in chunks --
never holds a full file in memory, so this scales cleanly from a small
file up to the full multi-gigabyte monthly extracts.

By default it looks for CSVs matching data/yellow_tripdata_*.csv.
To load files from elsewhere (e.g. ~/Documents, if you do not want to
copy multi-GB files into this repo folder), set the SOURCE_DIR
environment variable:

    TAXI_DATA_DIR=~/Documents python3 sql/load_db.py

Derived columns (trip_duration_min, pickup_hour, pickup_dow, pickup_month)
are computed once at load time so downstream SQL queries do not need to
re-parse datetimes on every run.
"""

import sqlite3
import pandas as pd
import os
import glob
import sys
import time

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
DEFAULT_DATA_DIR = os.path.join(PROJECT_ROOT, "data")
DB_PATH = os.path.join(DEFAULT_DATA_DIR, "taxi_analytics.db")

SOURCE_DIR = os.path.expanduser(os.environ.get("TAXI_DATA_DIR", DEFAULT_DATA_DIR))
CHUNK_SIZE = 200_000

COLUMN_MAP = {
    "vendorid": "vendor_id",
    "tpep_pickup_datetime": "pickup_datetime",
    "tpep_dropoff_datetime": "dropoff_datetime",
    "passenger_count": "passenger_count",
    "trip_distance": "trip_distance",
    "ratecodeid": "ratecode_id",
    "payment_type": "payment_type",
    "fare_amount": "fare_amount",
    "extra": "extra",
    "mta_tax": "mta_tax",
    "tip_amount": "tip_amount",
    "tolls_amount": "tolls_amount",
    "improvement_surcharge": "improvement_surcharge",
    "total_amount": "total_amount",
}

TARGET_COLUMNS = [
    "vendor_id", "pickup_datetime", "dropoff_datetime", "passenger_count",
    "trip_distance", "ratecode_id", "payment_type", "fare_amount", "extra",
    "mta_tax", "tip_amount", "tolls_amount", "improvement_surcharge", "total_amount",
]


def process_chunk(chunk):
    chunk = chunk.rename(columns={c: COLUMN_MAP[c.lower()] for c in chunk.columns if c.lower() in COLUMN_MAP})
    chunk = chunk.reindex(columns=TARGET_COLUMNS)

    chunk["pickup_datetime"] = pd.to_datetime(chunk["pickup_datetime"], errors="coerce")
    chunk["dropoff_datetime"] = pd.to_datetime(chunk["dropoff_datetime"], errors="coerce")

    chunk["trip_duration_min"] = (
        (chunk["dropoff_datetime"] - chunk["pickup_datetime"]).dt.total_seconds() / 60
    )
    chunk["pickup_hour"] = chunk["pickup_datetime"].dt.hour
    chunk["pickup_dow"] = chunk["pickup_datetime"].dt.dayofweek
    chunk["pickup_month"] = chunk["pickup_datetime"].dt.strftime("%Y-%m")

    chunk["pickup_datetime"] = chunk["pickup_datetime"].astype(str)
    chunk["dropoff_datetime"] = chunk["dropoff_datetime"].astype(str)

    return chunk


def main():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    files = sorted(glob.glob(os.path.join(SOURCE_DIR, "yellow_tripdata_*.csv")))

    if not files:
        print(f"No matching CSV files found in {SOURCE_DIR}")
        print("Set TAXI_DATA_DIR to the folder containing your yellow_tripdata_*.csv files.")
        sys.exit(1)

    print(f"Found {len(files)} file(s) to load from {SOURCE_DIR}:")
    for f in files:
        print(f"  - {f}")

    conn = sqlite3.connect(DB_PATH)
    total_rows = 0
    start_time = time.time()

    for fpath in files:
        print(f"\nLoading {os.path.basename(fpath)} ...")
        file_rows = 0
        for chunk in pd.read_csv(fpath, chunksize=CHUNK_SIZE, low_memory=False):
            processed = process_chunk(chunk)
            processed.to_sql("trips", conn, index=False, if_exists="append")
            file_rows += len(processed)
            total_rows += len(processed)
            print(f"  ... {file_rows:,} rows loaded from this file "
                  f"({total_rows:,} total, {time.time() - start_time:.0f}s elapsed)", end="\r")
        print()

    print("\nBuilding indexes ...")
    conn.execute("CREATE INDEX idx_pickup_hour ON trips(pickup_hour);")
    conn.execute("CREATE INDEX idx_pickup_dow ON trips(pickup_dow);")
    conn.execute("CREATE INDEX idx_payment_type ON trips(payment_type);")
    conn.execute("CREATE INDEX idx_pickup_month ON trips(pickup_month);")
    conn.commit()
    conn.close()

    elapsed = time.time() - start_time
    print(f"\nDone. Loaded {total_rows:,} total rows into {DB_PATH} in {elapsed:.0f}s.")


if __name__ == "__main__":
    main()
