-- Trip volume by day of week
-- Business question: which days see the most rides, weekday vs weekend patterns?

SELECT
    pickup_dow,
    CASE pickup_dow
        WHEN 0 THEN 'Monday' WHEN 1 THEN 'Tuesday' WHEN 2 THEN 'Wednesday'
        WHEN 3 THEN 'Thursday' WHEN 4 THEN 'Friday' WHEN 5 THEN 'Saturday'
        WHEN 6 THEN 'Sunday'
    END                                    AS day_name,
    COUNT(*)                              AS trip_count,
    ROUND(AVG(total_amount), 2)           AS avg_total_amount
FROM trips
WHERE fare_amount > 0
GROUP BY pickup_dow
ORDER BY pickup_dow;
