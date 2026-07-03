-- Trip distance distribution by band
-- Business question: what does the typical trip look like -- mostly short hops or longer rides?

SELECT
    CASE
        WHEN trip_distance < 1   THEN '01: <1 mi'
        WHEN trip_distance < 2   THEN '02: 1-2 mi'
        WHEN trip_distance < 5   THEN '03: 2-5 mi'
        WHEN trip_distance < 10  THEN '04: 5-10 mi'
        ELSE                          '05: 10mi+'
    END                                    AS distance_band,
    COUNT(*)                              AS trip_count,
    ROUND(AVG(fare_amount), 2)            AS avg_fare,
    ROUND(AVG(tip_amount), 2)             AS avg_tip
FROM trips
WHERE trip_distance > 0 AND fare_amount > 0
GROUP BY distance_band
ORDER BY distance_band;
