-- 1. SPECIES TABLE
CREATE TABLE species (
    species_id INTEGER PRIMARY KEY AUTOINCREMENT,
    common_name VARCHAR(100) NOT NULL,
    scientific_name VARCHAR(150) NOT NULL,
    category TEXT CHECK(category IN ('land', 'water')) NOT NULL,
    species_type VARCHAR(50),  -- bird, mammal, reptile, fish, amphibian
    conservation_status VARCHAR(50),
    status_trend TEXT CHECK(status_trend IN ('stable', 'increasing', 'decreasing', 'unknown')),
    total_sightings_estimate VARCHAR(50),
    description TEXT,
    habitat_info TEXT,
    diet_info TEXT,
    photo_url VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_species_category ON species(category);
CREATE INDEX idx_species_type ON species(species_type);
CREATE INDEX idx_conservation_status ON species(conservation_status);

-- 2. LOCATIONS TABLE
CREATE TABLE locations (
    location_id INTEGER PRIMARY KEY AUTOINCREMENT,
    city_name VARCHAR(100) NOT NULL,
    location_type TEXT CHECK(location_type IN ('city', 'municipality')) NOT NULL,
    latitude DECIMAL(10, 7) NOT NULL,
    longitude DECIMAL(10, 7) NOT NULL,
    severity_level TEXT CHECK(severity_level IN ('Critical', 'High', 'Medium', 'Low')) NOT NULL,
    total_reports INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_locations_severity ON locations(severity_level);
CREATE INDEX idx_locations_coordinates ON locations(latitude, longitude);

-- 3. SIGHTINGS TABLE
CREATE TABLE sightings (
    sighting_id INTEGER PRIMARY KEY AUTOINCREMENT,
    species_id INTEGER NOT NULL,
    location_id INTEGER NOT NULL,
    sighting_date DATE NOT NULL,
    number_observed INTEGER DEFAULT 1,
    observer_name VARCHAR(100),
    observer_contact VARCHAR(100),
    verification_status TEXT CHECK(verification_status IN ('pending', 'verified', 'rejected')) DEFAULT 'pending',
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (species_id) REFERENCES species(species_id) ON DELETE CASCADE,
    FOREIGN KEY (location_id) REFERENCES locations(location_id) ON DELETE CASCADE
);
CREATE INDEX idx_sightings_date ON sightings(sighting_date);
CREATE INDEX idx_sightings_species ON sightings(species_id);
CREATE INDEX idx_sightings_location ON sightings(location_id);

-- 4. REPORT CATEGORIES TABLE
CREATE TABLE report_categories (
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 5. REPORT SEVERITY TABLE
CREATE TABLE report_severity (
    severity_id INTEGER PRIMARY KEY AUTOINCREMENT,
    level VARCHAR(50) UNIQUE NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 6. ENVIRONMENTAL REPORTS TABLE
CREATE TABLE environmental_reports (
    report_id INTEGER PRIMARY KEY AUTOINCREMENT,
    location_id INTEGER NOT NULL,
    report_type TEXT CHECK(report_type IN ('pollution', 'deforestation', 'waste_dumping', 'wildlife_incident', 'other')) NOT NULL,
    severity TEXT CHECK(severity IN ('Critical', 'High', 'Medium', 'Low')) NOT NULL,
    status TEXT CHECK(status IN ('pending', 'in_progress', 'completed', 'closed')) DEFAULT 'pending',
    title VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    reporter_name VARCHAR(100),
    reporter_contact VARCHAR(100),
    report_date DATE NOT NULL,
    resolution_date DATE,
    photo_url VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (location_id) REFERENCES locations(location_id) ON DELETE CASCADE
);
CREATE INDEX idx_reports_type ON environmental_reports(report_type);
CREATE INDEX idx_reports_status ON environmental_reports(status);
CREATE INDEX idx_reports_severity ON environmental_reports(severity);

-- 7. USERS TABLE
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100),
    user_role TEXT CHECK(user_role IN ('admin', 'moderator', 'observer', 'public')) DEFAULT 'public',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(user_role);

-- 8. ACTIVITY LOG TABLE
CREATE TABLE activity_log (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    action_type VARCHAR(50) NOT NULL,
    description TEXT,
    ip_address VARCHAR(45),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE SET NULL
);
CREATE INDEX idx_activity_user ON activity_log(user_id);
CREATE INDEX idx_activity_date ON activity_log(created_at);

-- 9. DASHBOARD STATS TABLE
CREATE TABLE dashboard_stats (
    stat_id INTEGER PRIMARY KEY AUTOINCREMENT,
    stat_date DATE UNIQUE NOT NULL,
    total_reports INTEGER DEFAULT 0,
    pending_reports INTEGER DEFAULT 0,
    completed_reports INTEGER DEFAULT 0,
    critical_reports INTEGER DEFAULT 0,
    total_sightings INTEGER DEFAULT 0,
    verified_sightings INTEGER DEFAULT 0,
    land_species_count INTEGER DEFAULT 0,
    water_species_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_stats_date ON dashboard_stats(stat_date);


-- SAMPLE DATA - SPECIES (20 total: 12 land, 8 water)


-- LAND SPECIES (12)
-- Birds
INSERT INTO species (common_name, scientific_name, category, species_type, conservation_status, status_trend, total_sightings_estimate, description, habitat_info, diet_info, photo_url) VALUES
('Philippine Duck', 'Anas luzonica', 'land', 'bird', 'Least Concern', 'stable', '15,000-30,000', 'Sporting brown plumage and a distinctive blue-grey bill, this species charms with its subtle beauty and surprises with its adaptability.', 'Freshwater lakes, marshes, rice paddies, and wetlands throughout the Philippines. Prefers shallow waters with vegetation.', 'Seeds, aquatic plants, small invertebrates, and grain. Dabbles and tips-up to feed on submerged vegetation.', '/static/img/Animals/duck.jpg'),
('White-breasted Waterhen', 'Amaurornis phoenicurus', 'land', 'bird', 'Least Concern', 'stable', '10,000-100,000', 'Adult White-breasted waterhens have mainly dark grey upperparts and flanks, and a white face, neck, and breast. The lower belly and undertail are cinnamon or white colored.', 'Wetlands, marshes, ricefields, and water margins. Often found in areas with dense vegetation and reeds.', 'Aquatic invertebrates, small fish, seeds, and plant material. Forages by picking from water surface or ground.', '/static/img/Animals/white breasted waterhen.webp'),
('Garden Sunbird', 'Cinnyris jugularis', 'land', 'bird', 'Least Concern', 'stable', '15,000-25,000', 'A beautifully colored passerine bird from Southeast Asia. It has a long downward-curved bill which it uses to take nectar and capture insects.', 'Gardens, scrubland, forest edges, and cultivated areas with flowering plants. Found in lowlands and hills up to 2000m.', 'Primarily nectar from flowering plants, also small insects and spiders caught while feeding on flowers.', '/static/img/Animals/olive backed sunbird.webp'),
('Collared Kingfisher', 'Todiramphus chloris', 'land', 'bird', 'Least Concern', 'stable', 'Unknown', 'It hunts insects, crabs and small fish by perching and quickly diving its prey. This species is widespread and easily spotted due to its loud calls.', 'Open habitats near water including mangroves, coastal areas, ricefields, and forest edges. Often seen perched prominently.', 'Small fish, crustaceans, and large insects. Hunts by perching and diving quickly to catch prey in water.', '/static/img/Animals/xollared kingfisher.webp');

-- Mammals
INSERT INTO species (common_name, scientific_name, category, species_type, conservation_status, status_trend, total_sightings_estimate, description, habitat_info, diet_info, photo_url) VALUES
('Greater Musky Fruit Bat', 'Ptenochirus jagori', 'land', 'mammal', 'Least Concern', 'stable', 'Not specified yet', 'A captivating creature of the night, found gracefully navigating the tropical forests of Southeast Asia. These fascinating bats play a vital role in their ecosystems.', 'Tropical forests, secondary forests, and forest gardens. Roosts in caves, tree hollows, and human structures.', 'Fruits and nectar from various tree species. Plays important role in seed dispersal and pollination.', '/static/img/Animals/bat.png'),
('Luzon Giant Cloud Rat', 'Phloeomys pallidus', 'land', 'mammal', 'Concerned', 'stable', 'Unknown', 'This rodent has a relatively long pelage, which also covers the tail. The color is highly variable, but it is usually pale brown-grey or white with some dark brown or black patches.', 'Cloud forests and mossy montane forests of northern Luzon at high elevations (1500-2500m). Nocturnal and arboreal.', 'Leaves, bark, and vegetation found in forest canopy. Primarily herbivorous, adapted for arboreal life.', '/static/img/Animals/luzon giant cloud rat.webp'),
('Lion', 'Panthera leo', 'land', 'mammal', 'Vulnerable', 'decreasing', '23,000-39,000', 'The lion is a big wild cat with short, tawny-colored fur and white underparts. The long tail ends with a black tuft.', 'Savannas, grasslands, and open woodlands in Africa and small population in Gir Forest, India. Social cats living in prides.', 'Large herbivores including zebras, antelope, and buffalo. Apex predators hunted cooperatively in groups.', '/static/img/Animals/lion.webp'),
('Philippine Warty Pig', 'Sus philippensis', 'land', 'mammal', 'Vulnerable', 'decreasing', 'Unknown', 'A wild pig species with a distinctive "mane" and warty face. Important for nutrient cycling in forests.', 'Tropical forests and forest edges throughout the Philippines. Nocturnal and solitary, uses forest for shelter and food.', 'Roots, tubers, insects, small animals, and fallen fruit. Forages on forest floor and helps maintain soil health.', '/static/img/Animals/philippine warty pig.jpg'),
('Philippine Long-Tailed Macaque', 'Macaca fascicularis philippensis', 'land', 'mammal', 'Least Concern', 'decreasing', 'Unknown', 'Lives in group and eat fruits, leaves, and small animals, making it very adaptable. However, its population is decreasing due to habitat loss and trapping.', 'Tropical forests, mangroves, and agricultural areas throughout Philippines. Highly adaptable to different habitats. Social species living in troops.', 'Fruits, leaves, seeds, insects, and small vertebrates. Opportunistic feeders adaptable to various food sources.', '/static/img/Animals/philippine long-tailed macaque.jpg');

-- Reptiles
INSERT INTO species (common_name, scientific_name, category, species_type, conservation_status, status_trend, total_sightings_estimate, description, habitat_info, diet_info, photo_url) VALUES
('Tokay Gecko', 'Gekko gecko', 'land', 'reptile', 'Least Concern', 'stable', 'Unknown', 'The skin of Tokay geckos is soft to the touch and is generally gray with red speckles. However, Tokay geckos can change the color of their skin to blend into the environment.', 'Tropical forests, caves, human structures, and rocky areas. Nocturnal, often heard by distinctive loud calls at night.', 'Insects, spiders, small vertebrates, and other small animals. Active hunters that wait for prey on surfaces.', '/static/img/Animals/tokay gecko.webp'),
('Reticulated Python', 'Malayopython reticulatus', 'land', 'reptile', 'Least Concern', 'stable', 'Unknown', 'Is a non-venomous snake native to South and Southeast Asia. It is the world''s longest snake and is among the three heaviest snakes.', 'Tropical rainforests, swamps, and cultivated areas throughout Southeast Asia. Semi-aquatic, often found near water.', 'Mammals and large birds. Constrictor that swallows prey whole. Can consume large animals.', '/static/img/Animals/reticulated python.webp'),
('Common House Gecko', 'Hemidactylus frenatus', 'land', 'reptile', 'Least Concern', 'stable', 'Unknown', 'A small lizard native to Southeast Asia. They are named so because they are often seen climbing walls of houses and other buildings in search of insects.', 'Human settlements, houses, buildings, and trees. Commensal species highly adapted to living with humans.', 'Small insects, spiders, and invertebrates. Nocturnal hunters attracted to artificial lights around buildings.', '/static/img/Animals/common house gecko.webp');

-- WATER SPECIES (8)
-- Sea Turtles
INSERT INTO species (common_name, scientific_name, category, species_type, conservation_status, status_trend, total_sightings_estimate, description, habitat_info, diet_info, photo_url) VALUES
('Olive Ridley Turtle', 'Lepidochelys olivacea', 'water', 'reptile', 'Vulnerable', 'unknown', 'Unknown', 'A small to medium sea turtle known for its olive colored shell. They are famous for nesting events called "arribadas". They feed on jellyfish, small fish, crustaceans.', 'Tropical and subtropical oceans worldwide. Highly migratory, travels long distances between feeding and nesting grounds.', 'Jellyfish, small fish, crustaceans, and marine plants. Also consumes floating debris which can be fatal.', '/static/img/Animals/olive ridley turtle.jpg'),
('Green Turtle', 'Chelonia mydas', 'water', 'reptile', 'Endangered', 'unknown', 'Unknown', 'Large herbivorous sea turtle often found near coral reefs and seagrass beds. Adults eat sea grass, helping maintain healthy marine ecosystems.', 'Tropical and subtropical oceans, coastal reefs, and seagrass beds. Females return to natal beaches to nest.', 'Juveniles are omnivorous eating jellyfish and invertebrates. Adults are herbivorous, feeding on seagrass and algae.', '/static/img/Animals/green turtle.jpg'),
('Hawksbill Turtle', 'Eretmochelys imbricata', 'water', 'reptile', 'Critically Endangered', 'unknown', 'Unknown', 'Critically endangered turtle known for its beautifully patterned shell. They help control sponge populations on coral reefs.', 'Tropical coral reefs and rocky areas throughout world oceans. Highly migratory and solitary species.', 'Primarily sponges living on coral reefs. Also eats tunicates, corals, and other invertebrates. Helps maintain reef health.', '/static/img/Animals/hawksbill turtle.jpg');

-- Fish/Sharks
INSERT INTO species (common_name, scientific_name, category, species_type, conservation_status, status_trend, total_sightings_estimate, description, habitat_info, diet_info, photo_url) VALUES
('Whale Shark', 'Rhincodon typus', 'water', 'fish', 'Endangered', 'decreasing', 'Unknown', 'The world''s largest fish. A gentle filter feeder eating plankton and small fish. Important to ocean plankton balance.', 'Tropical and subtropical oceans between 21-30°C. Migratory, seasonally moves to areas with plankton blooms.', 'Filter feeder eating plankton, fish eggs, and small fish. Processes large volumes of water daily.', '/static/img/Animals/whale shark.jpg'),
('Blacktip Reef Shark', 'Carcharhinus melanopterus', 'water', 'fish', 'Near Threatened', 'unknown', 'Unknown', 'A small reef shark with black-tipped fins. Lives in shallow water and coral reefs. Plays a role in keeping fish populations balanced.', 'Shallow coastal waters, coral reefs, and lagoons in Indo-Pacific region. Found at depths less than 60m.', 'Small fish, rays, and crustaceans. Important predator maintaining balance in reef ecosystems.', '/static/img/Animals/blacktip reef shark.jpg'),
('Manta Rays', 'Mobula alfredi, Mobula birostris', 'water', 'fish', 'Vulnerable', 'unknown', 'Unknown', 'Large, gentle rays called "sea butterflies". Filter feeding on plankton. Highly intelligent and long lived.', 'Tropical and subtropical oceans. Highly migratory, seasonally congregates in areas with plankton abundance.', 'Filter feeders eating plankton and small fish. Can consume up to 1% of body weight daily in plankton.', '/static/img/Animals/manta rays.jpeg');

-- Marine Mammals
INSERT INTO species (common_name, scientific_name, category, species_type, conservation_status, status_trend, total_sightings_estimate, description, habitat_info, diet_info, photo_url) VALUES
('Spinner Dolphin', 'Stenella longirostris', 'water', 'mammal', 'Vulnerable', 'unknown', 'Unknown', 'Small, active dolphins known for spinning jumps. Feed on small fish and squid. Important part of marine food chain.', 'Tropical and subtropical oceans worldwide. Often found in groups, daylight hours in deeper offshore waters.', 'Small fish and squid caught during night feeding dives. Uses echolocation to hunt in deep waters.', '/static/img/Animals/spinner dolphin.jpeg'),
('Dwarf Sperm Whale', 'Kogia sima', 'water', 'mammal', 'Data Deficient', 'unknown', 'Unknown', 'A small, shy whale species rarely seen alive. Known for releasing a cloud of ink-like fluid to escape predators.', 'Deep offshore waters of tropical and subtropical oceans. Elusive and rarely observed in wild.', 'Deep-sea squid and fish. Dives to depths of 300-900m to hunt in deep water.', '/static/img/Animals/dwarf sperm whale.jpg');

-- SAMPLE DATA - LOCATIONS (34 total: 5 cities + 29 municipalities)
-- Cities
INSERT INTO locations (city_name, location_type, latitude, longitude, severity_level, total_reports) VALUES
('Batangas City', 'city', 13.7562, 121.0573, 'Critical', 4),
('Calaca', 'city', 13.9303, 120.8128, 'Low', 40),
('Lipa City', 'city', 13.9483, 121.1683, 'High', 7),
('Santo Tomas', 'city', 14.0800, 121.1400, 'Medium', 15),
('Tanauan City', 'city', 14.0844, 121.1492, 'Critical', 5);

-- Municipalities
INSERT INTO locations (city_name, location_type, latitude, longitude, severity_level, total_reports) VALUES
('Agoncillo', 'municipality', 13.9342, 120.9283, 'Low', 45),
('Alitagtag', 'municipality', 13.8653, 121.0047, 'Low', 38),
('Balayan', 'municipality', 13.9442, 120.7336, 'Medium', 18),
('Balete', 'municipality', 14.0167, 121.0833, 'Low', 35),
('Bauan', 'municipality', 13.7925, 121.0078, 'High', 8),
('Calatagan', 'municipality', 13.8322, 120.6275, 'Low', 50),
('Cuenca', 'municipality', 13.9167, 121.0500, 'Medium', 12),
('Ibaan', 'municipality', 13.8211, 121.1444, 'Low', 25),
('Laurel', 'municipality', 14.0500, 120.9333, 'Medium', 16),
('Lemery', 'municipality', 13.9011, 120.8928, 'Medium', 10),
('Lian', 'municipality', 13.9875, 120.6558, 'Low', 42),
('Lobo', 'municipality', 13.6267, 121.2142, 'High', 6),
('Mabini', 'municipality', 13.7639, 120.9417, 'Critical', 2),
('Malvar', 'municipality', 14.0322, 121.1550, 'Low', 30),
('Mataasnakahoy', 'municipality', 14.0203, 121.1111, 'Medium', 14),
('Nasugbu', 'municipality', 14.0722, 120.6358, 'High', 9),
('Padre Garcia', 'municipality', 13.8967, 121.2339, 'Low', 28),
('Rosario', 'municipality', 13.8589, 121.2339, 'Medium', 20),
('San Jose', 'municipality', 13.8825, 121.1067, 'Low', 32),
('San Juan', 'municipality', 13.8167, 121.3833, 'Critical', 3),
('San Luis', 'municipality', 13.8561, 120.9389, 'Medium', 11),
('San Nicolas', 'municipality', 13.9458, 120.9633, 'High', 7),
('San Pascual', 'municipality', 13.8058, 120.9828, 'Medium', 13),
('Santa Teresita', 'municipality', 13.8500, 120.9833, 'Low', 33),
('Taal', 'municipality', 13.8767, 120.9233, 'High', 8),
('Talisay', 'municipality', 14.0950, 121.0142, 'Low', 29),
('Taysan', 'municipality', 13.7667, 121.1714, 'Medium', 17),
('Tingloy', 'municipality', 13.7333, 120.8667, 'Low', 36),
('Tuy', 'municipality', 14.0167, 120.7500, 'Low', 31);


-- SAMPLE DATA - CATEGORIES AND SEVERITY
INSERT INTO report_categories (name, description) VALUES
('Pollution', 'Air, water, soil, or noise pollution'),
('Deforestation', 'Illegal or unauthorized forest clearing'),
('Waste Dumping', 'Illegal waste disposal'),
('Wildlife Incident', 'Wildlife injury, trafficking, or habitat issues'),
('Other', 'Other environmental concerns');

INSERT INTO report_severity (level, description) VALUES
('Low', 'Minor environmental impact, non-urgent'),
('Medium', 'Moderate impact, should be addressed soon'),
('High', 'Significant impact, requires prompt action'),
('Critical', 'Severe impact, immediate action required');

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

-- 4. GET SPECIES BY CONSERVATION STATUS (e.g., Endangered)
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
    city_name,
    location_type,
    severity_level,
    total_reports,
    (SELECT COUNT(*) FROM environmental_reports WHERE location_id = locations.location_id AND severity = 'Critical') AS critical_count,
    (SELECT COUNT(*) FROM environmental_reports WHERE location_id = locations.location_id AND severity = 'High') AS high_count,
    (SELECT COUNT(*) FROM environmental_reports WHERE location_id = locations.location_id AND severity = 'Medium') AS medium_count,
    (SELECT COUNT(*) FROM environmental_reports WHERE location_id = locations.location_id AND severity = 'Low') AS low_count
FROM locations
ORDER BY total_reports DESC;

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

-- 15. GET RECENT SIGHTINGS (Last 30 days)
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
WHERE s.sighting_date >= DATE('now', '-30 days')
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
