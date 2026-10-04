SELECT 
    s.sid AS station_id,
    s.s_name AS station_name,
    -- Rounded to 2 decimal places
    ROUND(AVG(m.pm_2_5), 2) AS avg_pm2_5_all_time,
    ROUND(AVG(m.vol_pm_2_5), 2) AS avg_vpm2_5_all_time,
    COUNT(*) AS total_readings
FROM 
    Measurement m
JOIN 
    Station s ON m.station_id = s.sid
GROUP BY 
    s.sid, s.s_name
ORDER BY 
    s.s_name;
