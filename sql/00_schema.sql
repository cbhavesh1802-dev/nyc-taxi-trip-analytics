-- ============================================================
-- NYC Yellow Taxi Trip Analytics
-- Source: NYC TLC Yellow Taxi Trip Data (2016 Q1: Jan, Feb, Mar + 2015 Jan)
-- ============================================================
-- Note: this batch of files predates the LocationID/zone system --
-- pickup/dropoff are recorded as raw lat/lon coordinates, not zone IDs.
-- taxi_zone_lookup.csv (LocationID-based) is from a later TLC schema
-- version and does NOT join directly to this data. Geospatial analysis
-- is out of scope here; this project focuses on temporal and fare patterns.
-- ============================================================

CREATE TABLE IF NOT EXISTS trips (
    vendor_id         INTEGER,
    pickup_datetime   TEXT,
    dropoff_datetime  TEXT,
    passenger_count   INTEGER,
    trip_distance     REAL,
    ratecode_id       INTEGER,
    payment_type      INTEGER,
    fare_amount       REAL,
    extra             REAL,
    mta_tax           REAL,
    tip_amount        REAL,
    tolls_amount      REAL,
    improvement_surcharge REAL,
    total_amount      REAL,
    trip_duration_min REAL,
    pickup_hour       INTEGER,
    pickup_dow        INTEGER,
    pickup_month      TEXT
);
