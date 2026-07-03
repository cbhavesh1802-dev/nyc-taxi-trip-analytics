-- Trip volume and average fare by hour of day
-- Business question: when is demand highest, and does fare/tip behavior change by hour?

SELECT
    pickup_hour,
    COUNT(*)                              AS trip_count,
    ROUND(AVG(fare_amount), 2)            AS avg_fare,
    ROUND(AVG(tip_amount), 2)             AS avg_tip,
    ROUND(AVG(trip_distance), 2)          AS avg_distance
FROM trips
WHERE fare_amount > 0 AND trip_distance > 0
GROUP BY pickup_hour
ORDER BY pickup_hour;
