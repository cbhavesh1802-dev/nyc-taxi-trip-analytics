-- Average trip speed by hour of day (distance / duration)
-- Business question: when does traffic slow trips down the most?
-- Filters out clearly bad records (zero/negative duration, unrealistic speed)

WITH clean_trips AS (
    SELECT
        pickup_hour,
        trip_distance,
        trip_duration_min,
        (trip_distance / (trip_duration_min / 60.0)) AS speed_mph
    FROM trips
    WHERE trip_duration_min BETWEEN 1 AND 180
      AND trip_distance > 0
)
SELECT
    pickup_hour,
    COUNT(*)                       AS trip_count,
    ROUND(AVG(speed_mph), 2)       AS avg_speed_mph,
    ROUND(AVG(trip_duration_min), 2) AS avg_duration_min
FROM clean_trips
WHERE speed_mph BETWEEN 1 AND 60  -- excludes GPS/data errors outside plausible NYC taxi speed range
GROUP BY pickup_hour
ORDER BY pickup_hour;
