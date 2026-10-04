SELECT 
    m.datetime,
    s.s_name AS station_name,
    m.nitrogen_oxides AS max_nox
FROM 
    Measurement m
JOIN 
    Station s ON m.station_id = s.sid
WHERE 
    YEAR(m.datetime) = 2022
ORDER BY 
    m.nitrogen_oxides DESC
LIMIT 1;