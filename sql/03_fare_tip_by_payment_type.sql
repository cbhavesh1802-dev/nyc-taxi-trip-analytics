-- Fare and tip behavior by payment type
-- Payment type: 1=Credit card, 2=Cash, 3=No charge, 4=Dispute
-- Business question: does tipping behavior differ meaningfully by payment method?
-- Note: cash tips are not captured in this data, so pct_tip for cash will be ~0 by definition.

SELECT
    CASE payment_type
        WHEN 1 THEN 'Credit Card' WHEN 2 THEN 'Cash'
        WHEN 3 THEN 'No Charge' WHEN 4 THEN 'Dispute'
        ELSE 'Other'
    END                                            AS payment_type,
    COUNT(*)                                       AS trip_count,
    ROUND(AVG(fare_amount), 2)                     AS avg_fare,
    ROUND(AVG(tip_amount), 2)                      AS avg_tip,
    ROUND(100.0 * AVG(tip_amount) / NULLIF(AVG(fare_amount), 0), 2) AS avg_tip_pct
FROM trips
WHERE fare_amount > 0
GROUP BY payment_type
ORDER BY trip_count DESC;
