-- SQL QUERIES

-- 1. GET ALL SPECIES WITH SPECIFIC COLUMNS
SELECT species_id, common_name, scientific_name, category, species_type, 
       conservation_status, photo_url 
FROM species 
ORDER BY common_name;

-- 2. GET ALL LAND ANIMALS
SELECT common_name, scientific_name, species_type, conservation_status, habitat_info, diet_info
FROM species 
WHERE category = 'land' 
ORDER BY species_type;

-- 3. GET ALL WATER ANIMALS
SELECT common_name, scientific_name, species_type, conservation_status, habitat_info, diet_info
FROM species 
WHERE category = 'water' 
ORDER BY species_type;

-- 4. GET SPECIES BY CONSERVATION STATUS (Endangered species)
SELECT common_name, scientific_name, conservation_status, status_trend
FROM species
WHERE conservation_status IN ('Endangered', 'Critically Endangered', 'Vulnerable')
ORDER BY conservation_status;

-- 5. GET SPECIES WITH DECREASING POPULATION
SELECT common_name, scientific_name, status_trend, total_sightings_estimate
FROM species
WHERE status_trend = 'decreasing';

-- 6. JOIN: GET ALL SIGHTINGS WITH SPECIES AND LOCATION DETAILS
SELECT 
    s.sighting_id,
    sp.common_name,
    sp.scientific_name,
    l.city_name,
    s.sighting_date,
    s.number_observed,
    s.observer_name,
    s.verification_status
FROM sightings s
INNER JOIN species sp ON s.species_id = sp.species_id
INNER JOIN locations l ON s.location_id = l.location_id
ORDER BY s.sighting_date DESC;

-- 7. JOIN: GET ALL ENVIRONMENTAL REPORTS WITH LOCATION DETAILS
SELECT 
    er.report_id,
    er.title,
    er.report_type,
    er.severity,
    er.status,
    l.city_name,
    er.report_date,
    er.reporter_name
FROM environmental_reports er
INNER JOIN locations l ON er.location_id = l.location_id
ORDER BY er.report_date DESC;

-- 8. GET LOCATIONS WITH MOST SIGHTINGS (using LEFT JOIN)
SELECT 
    l.city_name,
    l.location_type,
    l.severity_level,
    COUNT(s.sighting_id) AS total_sightings,
    COUNT(DISTINCT s.species_id) AS unique_species
FROM locations l
LEFT JOIN sightings s ON l.location_id = s.location_id
GROUP BY l.location_id, l.city_name, l.location_type, l.severity_level
ORDER BY total_sightings DESC;

-- 9. GET LOCATIONS WITH MOST CRITICAL/HIGH SEVERITY REPORTS
SELECT 
    l.city_name,
    l.severity_level,
    COUNT(CASE WHEN er.severity = 'Critical' THEN 1 END) AS critical_reports,
    COUNT(CASE WHEN er.severity = 'High' THEN 1 END) AS high_reports,
    COUNT(er.report_id) AS total_reports
FROM locations l
LEFT JOIN environmental_reports er ON l.location_id = er.location_id
GROUP BY l.location_id, l.city_name, l.severity_level
ORDER BY critical_reports DESC, high_reports DESC;

-- 10. GET REPORT STATISTICS BY TYPE
SELECT 
    report_type,
    severity,
    COUNT(*) AS count,
    COUNT(CASE WHEN status = 'completed' THEN 1 END) AS completed,
    COUNT(CASE WHEN status = 'pending' THEN 1 END) AS pending,
    COUNT(CASE WHEN status = 'in_progress' THEN 1 END) AS in_progress
FROM environmental_reports
GROUP BY report_type, severity
ORDER BY report_type, severity;

-- 11. GET SIGHTING VERIFICATION STATISTICS
SELECT 
    sp.category,
    COUNT(*) AS total_sightings,
    COUNT(CASE WHEN s.verification_status = 'verified' THEN 1 END) AS verified,
    COUNT(CASE WHEN s.verification_status = 'pending' THEN 1 END) AS pending,
    COUNT(CASE WHEN s.verification_status = 'rejected' THEN 1 END) AS rejected,
    ROUND(100.0 * COUNT(CASE WHEN s.verification_status = 'verified' THEN 1 END) / COUNT(*), 2) AS verification_rate
FROM sightings s
INNER JOIN species sp ON s.species_id = sp.species_id
GROUP BY sp.category;

-- 12. GET TOP 5 MOST SIGHTED SPECIES (with location and sighting count)
SELECT 
    sp.common_name,
    sp.scientific_name,
    COUNT(s.sighting_id) AS sighting_count,
    COUNT(DISTINCT s.location_id) AS locations
FROM sightings s
INNER JOIN species sp ON s.species_id = sp.species_id
GROUP BY sp.species_id, sp.common_name, sp.scientific_name
ORDER BY sighting_count DESC
LIMIT 5;

-- 13. GET ALL CITIES AND MUNICIPALITIES WITH REPORT COUNT AND SEVERITY DISTRIBUTION
SELECT 
    l.city_name,
    l.location_type,
    l.severity_level,
    l.total_reports,
    COUNT(CASE WHEN er.severity = 'Critical' THEN 1 END) AS critical_count,
    COUNT(CASE WHEN er.severity = 'High' THEN 1 END) AS high_count,
    COUNT(CASE WHEN er.severity = 'Medium' THEN 1 END) AS medium_count,
    COUNT(CASE WHEN er.severity = 'Low' THEN 1 END) AS low_count
FROM locations l
LEFT JOIN environmental_reports er ON l.location_id = er.location_id
GROUP BY l.location_id, l.city_name, l.location_type, l.severity_level, l.total_reports
ORDER BY l.total_reports DESC;

-- 14. GET SPECIES BY CATEGORY WITH HABITAT AND DIET INFO
SELECT 
    common_name,
    scientific_name,
    species_type,
    category,
    conservation_status,
    habitat_info,
    diet_info,
    photo_url
FROM species
WHERE category = 'land'
ORDER BY species_type, common_name;

-- 15. GET RECENT SIGHTINGS (Last 30 days) - PostgreSQL syntax
SELECT 
    s.sighting_id,
    sp.common_name,
    l.city_name,
    s.sighting_date,
    s.number_observed,
    s.verification_status
FROM sightings s
INNER JOIN species sp ON s.species_id = sp.species_id
INNER JOIN locations l ON s.location_id = l.location_id
WHERE s.sighting_date >= CURRENT_DATE - INTERVAL '30 days'
ORDER BY s.sighting_date DESC;

-- 16. GET DASHBOARD STATISTICS (Summary)
SELECT 
    COUNT(DISTINCT sp.species_id) AS total_species,
    COUNT(DISTINCT CASE WHEN sp.category = 'land' THEN sp.species_id END) AS land_species,
    COUNT(DISTINCT CASE WHEN sp.category = 'water' THEN sp.species_id END) AS water_species,
    COUNT(DISTINCT s.sighting_id) AS total_sightings,
    COUNT(DISTINCT l.location_id) AS locations_with_sightings,
    COUNT(DISTINCT er.report_id) AS total_environmental_reports,
    COUNT(CASE WHEN er.severity = 'Critical' THEN 1 END) AS critical_reports
FROM species sp
LEFT JOIN sightings s ON sp.species_id = s.species_id
LEFT JOIN locations l ON s.location_id = l.location_id
LEFT JOIN environmental_reports er ON l.location_id = er.location_id;

-- 17. FIND SPECIES WITHOUT SIGHTINGS (Not yet recorded)
SELECT 
    sp.species_id,
    sp.common_name,
    sp.scientific_name,
    sp.category,
    sp.conservation_status
FROM species sp
LEFT JOIN sightings s ON sp.species_id = s.species_id
WHERE s.sighting_id IS NULL;

-- 18. GET COMPLETE SIGHTING DETAILS WITH ALL RELATED INFO
SELECT 
    s.sighting_id,
    sp.common_name,
    sp.scientific_name,
    sp.category,
    sp.species_type,
    sp.photo_url,
    l.city_name,
    l.location_type,
    l.latitude,
    l.longitude,
    s.sighting_date,
    s.number_observed,
    s.observer_name,
    s.observer_contact,
    s.verification_status,
    s.notes,
    s.created_at
FROM sightings s
INNER JOIN species sp ON s.species_id = sp.species_id
INNER JOIN locations l ON s.location_id = l.location_id
ORDER BY s.created_at DESC;

-- 19. GET USER ACTIVITY LOG WITH USER DETAILS
SELECT 
    al.log_id,
    u.username,
    u.full_name,
    al.action_type,
    al.description,
    al.ip_address,
    al.created_at
FROM activity_log al
LEFT JOIN users u ON al.user_id = u.user_id
ORDER BY al.created_at DESC;

-- 20. COUNT SPECIES BY TYPE AND CATEGORY
SELECT 
    category,
    species_type,
    COUNT(*) AS species_count,
    STRING_AGG(common_name, ', ') AS species_list
FROM species
GROUP BY category, species_type
ORDER BY category, species_type;