SELECT 
    s.s_name AS station_name,
    -- Rounded to 2 decimal places
    ROUND(AVG(m.pm_2_5), 2) AS avg_pm2_5,         
    ROUND(AVG(m.vol_pm_2_5), 2) AS avg_vpm2_5,    
    COUNT(*) AS reading_count               
FROM 
    Measurement m
JOIN 
    Station s ON m.station_id = s.sid
WHERE 
    YEAR(m.datetime) = 2022
    AND TIME(m.datetime) BETWEEN '07:30:00' AND '08:30:00'  -- close to the 08:00 hours
GROUP BY 
    s.s_name
ORDER BY 
    s.s_name;