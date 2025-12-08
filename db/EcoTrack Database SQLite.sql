DROP TABLE IF EXISTS activity_log;
DROP TABLE IF EXISTS dashboard_stats;
DROP TABLE IF EXISTS sightings;
DROP TABLE IF EXISTS environmental_reports;
DROP TABLE IF EXISTS species;
DROP TABLE IF EXISTS locations;
DROP TABLE IF EXISTS report_categories;
DROP TABLE IF EXISTS report_severity;
DROP TABLE IF EXISTS users;

-- TABLE 1: SPECIES
CREATE TABLE species (
    species_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    common_name VARCHAR(100) NOT NULL,
    scientific_name VARCHAR(150) NOT NULL,
    category VARCHAR(5) NOT NULL CHECK (category IN ('land', 'water')),
    species_type VARCHAR(50),
    conservation_status VARCHAR(50),
    status_trend VARCHAR(10) CHECK (status_trend IN ('stable', 'increasing', 'decreasing', 'unknown')),
    total_sightings_estimate VARCHAR(50),
    description TEXT,
    habitat_info TEXT,
    diet_info TEXT,
    photo_url VARCHAR(255),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_species_category ON species(category);
CREATE INDEX idx_species_type ON species(species_type);
CREATE INDEX idx_conservation_status ON species(conservation_status);

-- TABLE 2: LOCATIONS
CREATE TABLE locations (
    location_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    city_name VARCHAR(100) NOT NULL,
    location_type VARCHAR(12) NOT NULL CHECK (location_type IN ('city', 'municipality')),
    latitude NUMERIC(10, 7) NOT NULL,
    longitude NUMERIC(10, 7) NOT NULL,
    severity_level VARCHAR(8) NOT NULL CHECK (severity_level IN ('Critical', 'High', 'Medium', 'Low')),
    total_reports INTEGER DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_locations_severity ON locations(severity_level);
CREATE INDEX idx_locations_coordinates ON locations(latitude, longitude);

-- TABLE 3: SIGHTINGS
CREATE TABLE sightings (
    sighting_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    species_id INTEGER NOT NULL,
    location_id INTEGER NOT NULL,
    sighting_date DATE NOT NULL,
    number_observed INTEGER DEFAULT 1,
    observer_name VARCHAR(100),
    observer_contact VARCHAR(100),
    verification_status VARCHAR(8) DEFAULT 'pending' CHECK (verification_status IN ('pending', 'verified', 'rejected')),
    notes TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (species_id) REFERENCES species(species_id) ON DELETE CASCADE,
    FOREIGN KEY (location_id) REFERENCES locations(location_id) ON DELETE CASCADE
);

CREATE INDEX idx_sightings_date ON sightings(sighting_date);
CREATE INDEX idx_sightings_species ON sightings(species_id);
CREATE INDEX idx_sightings_location ON sightings(location_id);

-- TABLE 4: REPORT_CATEGORIES
CREATE TABLE report_categories (
    category_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- TABLE 5: REPORT_SEVERITY
CREATE TABLE report_severity (
    severity_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    level VARCHAR(50) NOT NULL UNIQUE,
    description TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- TABLE 6: ENVIRONMENTAL_REPORTS
CREATE TABLE environmental_reports (
    report_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    location_id INTEGER NOT NULL,
    report_type VARCHAR(17) NOT NULL CHECK (report_type IN ('pollution', 'deforestation', 'waste_dumping', 'wildlife_incident', 'other')),
    severity VARCHAR(8) NOT NULL CHECK (severity IN ('Critical', 'High', 'Medium', 'Low')),
    status VARCHAR(11) DEFAULT 'pending' CHECK (status IN ('pending', 'in_progress', 'completed', 'closed')),
    title VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    reporter_name VARCHAR(100),
    reporter_contact VARCHAR(100),
    report_date DATE NOT NULL,
    resolution_date DATE,
    photo_url VARCHAR(255),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (location_id) REFERENCES locations(location_id) ON DELETE CASCADE
);

CREATE INDEX idx_reports_type ON environmental_reports(report_type);
CREATE INDEX idx_reports_status ON environmental_reports(status);
CREATE INDEX idx_reports_severity ON environmental_reports(severity);

-- TABLE 7: USERS
CREATE TABLE users (
    user_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    full_name VARCHAR(100),
    user_role VARCHAR(6) DEFAULT 'public' CHECK (user_role IN ('admin', 'public')),
    is_active BOOLEAN DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_login DATETIME
);

CREATE INDEX idx_users_role ON users(user_role);

-- TABLE 8: ACTIVITY_LOG
CREATE TABLE activity_log (
    log_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    action_type VARCHAR(50) NOT NULL,
    description TEXT,
    ip_address VARCHAR(45),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE SET NULL
);

CREATE INDEX idx_activity_user ON activity_log(user_id);
CREATE INDEX idx_activity_date ON activity_log(created_at);

-- TABLE 9: DASHBOARD_STATS
CREATE TABLE dashboard_stats (
    stat_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    stat_date DATE NOT NULL UNIQUE,
    total_reports INTEGER DEFAULT 0,
    pending_reports INTEGER DEFAULT 0,
    completed_reports INTEGER DEFAULT 0,
    critical_reports INTEGER DEFAULT 0,
    total_sightings INTEGER DEFAULT 0,
    verified_sightings INTEGER DEFAULT 0,
    land_species_count INTEGER DEFAULT 0,
    water_species_count INTEGER DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_stats_date ON dashboard_stats(stat_date);

-- TRIGGER: Auto-update updated_at timestamp on species
CREATE TRIGGER update_species_updated_at 
    AFTER UPDATE ON species
    FOR EACH ROW
BEGIN
    UPDATE species SET updated_at = CURRENT_TIMESTAMP WHERE species_id = OLD.species_id;
END;

-- TRIGGER: Auto-update updated_at timestamp on locations
CREATE TRIGGER update_locations_updated_at 
    AFTER UPDATE ON locations
    FOR EACH ROW
BEGIN
    UPDATE locations SET updated_at = CURRENT_TIMESTAMP WHERE location_id = OLD.location_id;
END;

-- TRIGGER: Auto-update updated_at timestamp on environmental_reports
CREATE TRIGGER update_environmental_reports_updated_at 
    AFTER UPDATE ON environmental_reports
    FOR EACH ROW
BEGIN
    UPDATE environmental_reports SET updated_at = CURRENT_TIMESTAMP WHERE report_id = OLD.report_id;
END;


-- INSERT DATA: SPECIES (20 records - 12 land, 8 water)

-- Land Species - Birds (4)
INSERT INTO species (common_name, scientific_name, category, species_type, conservation_status, status_trend, total_sightings_estimate, description, habitat_info, diet_info, photo_url) VALUES
('Philippine Duck', 'Anas luzonica', 'land', 'bird', 'Least Concern', 'stable', '15,000-30,000', 'Sporting brown plumage and a distinctive blue-grey bill, this species charms with its subtle beauty and surprises with its adaptability.', 'Freshwater lakes, marshes, rice paddies, and wetlands throughout the Philippines. Prefers shallow waters with vegetation.', 'Seeds, aquatic plants, small invertebrates, and grain. Dabbles and tips-up to feed on submerged vegetation.', '/static/img/Animals/duck.jpg'),
('White-breasted Waterhen', 'Amaurornis phoenicurus', 'land', 'bird', 'Least Concern', 'stable', '10,000-100,000', 'Adult White-breasted waterhens have mainly dark grey upperparts and flanks, and a white face, neck, and breast. The lower belly and undertail are cinnamon or white colored.', 'Wetlands, marshes, ricefields, and water margins. Often found in areas with dense vegetation and reeds.', 'Aquatic invertebrates, small fish, seeds, and plant material. Forages by picking from water surface or ground.', '/static/img/Animals/white breasted waterhen.webp'),
('Garden Sunbird', 'Cinnyris jugularis', 'land', 'bird', 'Least Concern', 'stable', '15,000-25,000', 'A beautifully colored passerine bird from Southeast Asia. It has a long downward-curved bill which it uses to take nectar and capture insects.', 'Gardens, scrubland, forest edges, and cultivated areas with flowering plants. Found in lowlands and hills up to 2000m.', 'Primarily nectar from flowering plants, also small insects and spiders caught while feeding on flowers.', '/static/img/Animals/olive backed sunbird.webp'),
('Collared Kingfisher', 'Todiramphus chloris', 'land', 'bird', 'Least Concern', 'stable', 'Unknown', 'It hunts insects, crabs and small fish by perching and quickly diving its prey. This species is widespread and easily spotted due to its loud calls.', 'Open habitats near water including mangroves, coastal areas, ricefields, and forest edges. Often seen perched prominently.', 'Small fish, crustaceans, and large insects. Hunts by perching and diving quickly to catch prey in water.', '/static/img/Animals/xollared kingfisher.webp');

-- Land Species - Mammals (5)
INSERT INTO species (common_name, scientific_name, category, species_type, conservation_status, status_trend, total_sightings_estimate, description, habitat_info, diet_info, photo_url) VALUES
('Greater Musky Fruit Bat', 'Ptenochirus jagori', 'land', 'mammal', 'Least Concern', 'stable', 'Not specified yet', 'A captivating creature of the night, found gracefully navigating the tropical forests of Southeast Asia. These fascinating bats play a vital role in their ecosystems.', 'Tropical forests, secondary forests, and forest gardens. Roosts in caves, tree hollows, and human structures.', 'Fruits and nectar from various tree species. Plays important role in seed dispersal and pollination.', '/static/img/Animals/bat.png'),
('Luzon Giant Cloud Rat', 'Phloeomys pallidus', 'land', 'mammal', 'Concerned', 'stable', 'Unknown', 'This rodent has a relatively long pelage, which also covers the tail. The color is highly variable, but it is usually pale brown-grey or white with some dark brown or black patches.', 'Cloud forests and mossy montane forests of northern Luzon at high elevations (1500-2500m). Nocturnal and arboreal.', 'Leaves, bark, and vegetation found in forest canopy. Primarily herbivorous, adapted for arboreal life.', '/static/img/Animals/luzon giant cloud rat.webp'),
('Lion', 'Panthera leo', 'land', 'mammal', 'Vulnerable', 'decreasing', '23,000-39,000', 'The lion is a big wild cat with short, tawny-colored fur and white underparts. The long tail ends with a black tuft.', 'Savannas, grasslands, and open woodlands in Africa and small population in Gir Forest, India. Social cats living in prides.', 'Large herbivores including zebras, antelope, and buffalo. Apex predators hunted cooperatively in groups.', '/static/img/Animals/lion.webp'),
('Philippine Warty Pig', 'Sus philippensis', 'land', 'mammal', 'Vulnerable', 'decreasing', 'Unknown', 'A wild pig species with a distinctive "mane" and warty face. Important for nutrient cycling in forests.', 'Tropical forests and forest edges throughout the Philippines. Nocturnal and solitary, uses forest for shelter and food.', 'Roots, tubers, insects, small animals, and fallen fruit. Forages on forest floor and helps maintain soil health.', '/static/img/Animals/philippine warty pig.jpg'),
('Philippine Long-Tailed Macaque', 'Macaca fascicularis philippensis', 'land', 'mammal', 'Least Concern', 'decreasing', 'Unknown', 'Lives in group and eat fruits, leaves, and small animals, making it very adaptable. However, its population is decreasing due to habitat loss and trapping.', 'Tropical forests, mangroves, and agricultural areas throughout Philippines. Highly adaptable to different habitats. Social species living in troops.', 'Fruits, leaves, seeds, insects, and small vertebrates. Opportunistic feeders adaptable to various food sources.', '/static/img/Animals/philippine long-tailed macaque.jpg');

-- Land Species - Reptiles (3)
INSERT INTO species (common_name, scientific_name, category, species_type, conservation_status, status_trend, total_sightings_estimate, description, habitat_info, diet_info, photo_url) VALUES
('Tokay Gecko', 'Gekko gecko', 'land', 'reptile', 'Least Concern', 'stable', 'Unknown', 'The skin of Tokay geckos is soft to the touch and is generally gray with red speckles. However, Tokay geckos can change the color of their skin to blend into the environment.', 'Tropical forests, caves, human structures, and rocky areas. Nocturnal, often heard by distinctive loud calls at night.', 'Insects, spiders, small vertebrates, and other small animals. Active hunters that wait for prey on surfaces.', '/static/img/Animals/tokay gecko.webp'),
('Reticulated Python', 'Malayopython reticulatus', 'land', 'reptile', 'Least Concern', 'stable', 'Unknown', 'Is a non-venomous snake native to South and Southeast Asia. It is the world''s longest snake and is among the three heaviest snakes.', 'Tropical rainforests, swamps, and cultivated areas throughout Southeast Asia. Semi-aquatic, often found near water.', 'Mammals and large birds. Constrictor that swallows prey whole. Can consume large animals.', '/static/img/Animals/reticulated python.webp'),
('Common House Gecko', 'Hemidactylus frenatus', 'land', 'reptile', 'Least Concern', 'stable', 'Unknown', 'A small lizard native to Southeast Asia. They are named so because they are often seen climbing walls of houses and other buildings in search of insects.', 'Human settlements, houses, buildings, and trees. Commensal species highly adapted to living with humans.', 'Small insects, spiders, and invertebrates. Nocturnal hunters attracted to artificial lights around buildings.', '/static/img/Animals/common house gecko.webp');

-- Water Species - Sea Turtles (3)
INSERT INTO species (common_name, scientific_name, category, species_type, conservation_status, status_trend, total_sightings_estimate, description, habitat_info, diet_info, photo_url) VALUES
('Olive Ridley Turtle', 'Lepidochelys olivacea', 'water', 'reptile', 'Vulnerable', 'unknown', 'Unknown', 'A small to medium sea turtle known for its olive colored shell. They are famous for nesting events called "arribadas". They feed on jellyfish, small fish, crustaceans.', 'Tropical and subtropical oceans worldwide. Highly migratory, travels long distances between feeding and nesting grounds.', 'Jellyfish, small fish, crustaceans, and marine plants. Also consumes floating debris which can be fatal.', '/static/img/Animals/olive ridley turtle.jpg'),
('Green Turtle', 'Chelonia mydas', 'water', 'reptile', 'Endangered', 'unknown', 'Unknown', 'Large herbivorous sea turtle often found near coral reefs and seagrass beds. Adults eat sea grass, helping maintain healthy marine ecosystems.', 'Tropical and subtropical oceans, coastal reefs, and seagrass beds. Females return to natal beaches to nest.', 'Juveniles are omnivorous eating jellyfish and invertebrates. Adults are herbivorous, feeding on seagrass and algae.', '/static/img/Animals/green turtle.jpg'),
('Hawksbill Turtle', 'Eretmochelys imbricata', 'water', 'reptile', 'Critically Endangered', 'unknown', 'Unknown', 'Critically endangered turtle known for its beautifully patterned shell. They help control sponge populations on coral reefs.', 'Tropical coral reefs and rocky areas throughout world oceans. Highly migratory and solitary species.', 'Primarily sponges living on coral reefs. Also eats tunicates, corals, and other invertebrates. Helps maintain reef health.', '/static/img/Animals/hawksbill turtle.jpg');

-- Water Species - Fish/Sharks (3)
INSERT INTO species (common_name, scientific_name, category, species_type, conservation_status, status_trend, total_sightings_estimate, description, habitat_info, diet_info, photo_url) VALUES
('Whale Shark', 'Rhincodon typus', 'water', 'fish', 'Endangered', 'decreasing', 'Unknown', 'The world''s largest fish. A gentle filter feeder eating plankton and small fish. Important to ocean plankton balance.', 'Tropical and subtropical oceans between 21-30°C. Migratory, seasonally moves to areas with plankton blooms.', 'Filter feeder eating plankton, fish eggs, and small fish. Processes large volumes of water daily.', '/static/img/Animals/whale shark.jpg'),
('Blacktip Reef Shark', 'Carcharhinus melanopterus', 'water', 'fish', 'Near Threatened', 'unknown', 'Unknown', 'A small reef shark with black-tipped fins. Lives in shallow water and coral reefs. Plays a role in keeping fish populations balanced.', 'Shallow coastal waters, coral reefs, and lagoons in Indo-Pacific region. Found at depths less than 60m.', 'Small fish, rays, and crustaceans. Important predator maintaining balance in reef ecosystems.', '/static/img/Animals/blacktip reef shark.jpg'),
('Manta Rays', 'Mobula alfredi, Mobula birostris', 'water', 'fish', 'Vulnerable', 'unknown', 'Unknown', 'Large, gentle rays called "sea butterflies". Filter feeding on plankton. Highly intelligent and long lived.', 'Tropical and subtropical oceans. Highly migratory, seasonally congregates in areas with plankton abundance.', 'Filter feeders eating plankton and small fish. Can consume up to 1% of body weight daily in plankton.', '/static/img/Animals/manta rays.jpeg');

-- Water Species - Marine Mammals (2)
INSERT INTO species (common_name, scientific_name, category, species_type, conservation_status, status_trend, total_sightings_estimate, description, habitat_info, diet_info, photo_url) VALUES
('Spinner Dolphin', 'Stenella longirostris', 'water', 'mammal', 'Vulnerable', 'unknown', 'Unknown', 'Small, active dolphins known for spinning jumps. Feed on small fish and squid. Important part of marine food chain.', 'Tropical and subtropical oceans worldwide. Often found in groups, daylight hours in deeper offshore waters.', 'Small fish and squid caught during night feeding dives. Uses echolocation to hunt in deep waters.', '/static/img/Animals/spinner dolphin.jpeg'),
('Dwarf Sperm Whale', 'Kogia sima', 'water', 'mammal', 'Data Deficient', 'unknown', 'Unknown', 'A small, shy whale species rarely seen alive. Known for releasing a cloud of ink-like fluid to escape predators.', 'Deep offshore waters of tropical and subtropical oceans. Elusive and rarely observed in wild.', 'Deep-sea squid and fish. Dives to depths of 300-900m to hunt in deep water.', '/static/img/Animals/dwarf sperm whale.jpg');

-- INSERT DATA: LOCATIONS (34 records - 5 cities, 29 municipalities)

-- Cities (5)
INSERT INTO locations (city_name, location_type, latitude, longitude, severity_level, total_reports) VALUES
('Batangas City', 'city', 13.7565, 121.0583, 'Critical', 0),
('Calaca', 'city', 13.9167, 120.8167, 'Low', 0),
('Lipa City', 'city', 13.9411, 121.1622, 'High', 0),
('Santo Tomas', 'city', 14.1078, 121.1414, 'Medium', 0),
('Tanauan City', 'city', 14.0858, 121.1500, 'Critical', 0);

-- Municipalities (29)
INSERT INTO locations (city_name, location_type, latitude, longitude, severity_level, total_reports) VALUES
('Agoncillo', 'municipality', 13.9333, 120.9333, 'Low', 0),
('Alitagtag', 'municipality', 13.8667, 121.0000, 'Low', 0),
('Balayan', 'municipality', 13.9333, 120.7333, 'Medium', 0),
('Balete', 'municipality', 14.0167, 121.0833, 'Low', 0),
('Bauan', 'municipality', 13.7833, 121.0000, 'High', 0),
('Calatagan', 'municipality', 13.8333, 120.6333, 'Low', 0),
('Cuenca', 'municipality', 13.9000, 121.0500, 'Medium', 0),
('Ibaan', 'municipality', 13.8167, 121.1333, 'Low', 0),
('Laurel', 'municipality', 14.0500, 120.9167, 'Medium', 0),
('Lemery', 'municipality', 13.8833, 120.9000, 'Medium', 0),
('Lian', 'municipality', 14.0333, 120.6500, 'Low', 0),
('Lobo', 'municipality', 13.6333, 121.2167, 'High', 0),
('Mabini', 'municipality', 13.7667, 120.9333, 'Critical', 0),
('Malvar', 'municipality', 14.0500, 121.1667, 'Low', 0),
('Mataasnakahoy', 'municipality', 14.0000, 121.1167, 'Medium', 0),
('Nasugbu', 'municipality', 14.0667, 120.6333, 'High', 0),
('Padre Garcia', 'municipality', 13.8833, 121.2167, 'Low', 0),
('Rosario', 'municipality', 13.8500, 121.2167, 'Medium', 0),
('San Jose', 'municipality', 13.8667, 121.1000, 'Low', 0),
('San Juan', 'municipality', 13.8167, 121.4000, 'Critical', 0),
('San Luis', 'municipality', 13.8500, 120.9500, 'Medium', 0),
('San Nicolas', 'municipality', 13.9333, 120.9500, 'High', 0),
('San Pascual', 'municipality', 13.8000, 120.9833, 'Medium', 0),
('Santa Teresita', 'municipality', 13.8500, 120.9833, 'Low', 0),
('Taal', 'municipality', 13.8667, 120.9167, 'High', 0),
('Talisay', 'municipality', 14.1000, 121.0167, 'Low', 0),
('Taysan', 'municipality', 13.7833, 121.1833, 'Medium', 0),
('Tingloy', 'municipality', 13.7333, 120.8667, 'Low', 0),
('Tuy', 'municipality', 14.0167, 120.7333, 'Low', 0);

-- INSERT DATA: REPORT_CATEGORIES (5 records)
INSERT INTO report_categories (name, description) VALUES
('Pollution', 'Air, water, soil, or noise pollution'),
('Deforestation', 'Illegal or unauthorized forest clearing'),
('Waste Dumping', 'Illegal waste disposal'),
('Wildlife Incident', 'Wildlife injury, trafficking, or habitat issues'),
('Other', 'Other environmental concerns');

-- INSERT DATA: REPORT_SEVERITY (4 records)
INSERT INTO report_severity (level, description) VALUES
('Low', 'Minor environmental impact, non-urgent'),
('Medium', 'Moderate impact, should be addressed soon'),
('High', 'Significant impact, requires prompt action'),
('Critical', 'Severe impact, immediate action required');

-- INSERT DATA: USERS (2 records)
INSERT INTO users (username, password, full_name, user_role, is_active) VALUES
('admin', 'admin123', 'Administrator', 'admin', 1),
('user1', 'user123', 'Public User', 'public', 1);

-- INSERT DATA: ENVIRONMENTAL_REPORTS (10 records)
INSERT INTO environmental_reports (location_id, report_type, severity, status, title, description, reporter_name, reporter_contact, report_date) VALUES
(1, 'pollution', 'Critical', 'pending', 'Illegal Waste Dumping at Batangas City Port', 'Large amounts of industrial waste found dumped near the port area. Immediate cleanup required.', 'Juan Dela Cruz', 'juan@email.com', '2025-12-01'),
(25, 'deforestation', 'High', 'in_progress', 'Deforestation in Taal Watershed', 'Unauthorized tree cutting observed in the protected watershed area.', 'Maria Santos', 'maria@email.com', '2025-12-07'),
(16, 'pollution', 'High', 'pending', 'Plastic Pollution at Nasugbu Beach', 'Excessive plastic waste accumulating along the shoreline, affecting marine life.', 'Pedro Reyes', '09123456789', '2025-12-07'),
(8, 'wildlife_incident', 'Critical', 'in_progress', 'Wildlife Trafficking Suspected', 'Reports of illegal bird trading in the local market area.', 'Ana Garcia', 'ana.garcia@email.com', '2025-12-03'),
(12, 'pollution', 'High', 'pending', 'Water Pollution in Tanauan River', 'Factory discharge causing water discoloration and fish kill.', 'Carlos Manuel', '09187654321', '2025-11-26'),
(1, 'waste_dumping', 'Medium', 'completed', 'Illegal Garbage Dump Near School', 'Garbage pile found near elementary school causing health concerns.', 'Rosa Mendez', 'rosa@email.com', '2025-11-20'),
(3, 'pollution', 'High', 'pending', 'Air Pollution from Factory', 'Heavy smoke emission from manufacturing plant affecting nearby residents.', 'Antonio Cruz', '09198765432', '2025-12-05'),
(20, 'wildlife_incident', 'Medium', 'pending', 'Injured Sea Turtle Found', 'Sea turtle found with fishing net entanglement on the beach.', 'Elena Flores', 'elena@email.com', '2025-12-06'),
(13, 'deforestation', 'Critical', 'in_progress', 'Mangrove Area Being Cleared', 'Illegal clearing of protected mangrove forest for fish pond development.', 'Roberto Santos', '09176543210', '2025-12-02'),
(10, 'other', 'Low', 'completed', 'Noise Pollution from Construction', 'Extended construction hours causing disturbance to wildlife in nearby area.', 'Carmen Reyes', 'carmen@email.com', '2025-11-15');

-- INSERT DATA: SIGHTINGS (20 records)
INSERT INTO sightings (species_id, location_id, sighting_date, number_observed, observer_name, observer_contact, verification_status, notes) VALUES
(1, 6, '2025-12-01', 12, 'Maria Santos', 'maria@email.com', 'verified', 'Group of Philippine Ducks spotted near rice paddies'),
(2, 10, '2025-12-02', 5, 'Juan Reyes', '09123456789', 'verified', 'White-breasted Waterhens foraging in wetland area'),
(3, 3, '2025-12-03', 8, 'Ana Cruz', 'ana@email.com', 'pending', 'Garden Sunbirds feeding on flowering plants'),
(4, 11, '2025-12-04', 2, 'Pedro Garcia', '09187654321', 'verified', 'Collared Kingfisher pair observed near mangroves'),
(5, 7, '2025-12-05', 15, 'Rosa Mendez', 'rosa@email.com', 'pending', 'Fruit bats colony in cave entrance'),
(6, 9, '2025-12-01', 1, 'Carlos Manuel', '09198765432', 'verified', 'Rare sighting of Luzon Giant Cloud Rat in mountain forest'),
(7, 1, '2025-12-02', 3, 'Elena Flores', 'elena@email.com', 'rejected', 'Reported lion sighting - likely misidentification'),
(10, 4, '2025-12-03', 4, 'Roberto Santos', '09176543210', 'verified', 'Tokay Geckos on building walls at night'),
(11, 8, '2025-12-04', 1, 'Carmen Reyes', 'carmen@email.com', 'pending', 'Reticulated Python spotted crossing road'),
(12, 2, '2025-12-05', 20, 'Antonio Lopez', '09165432109', 'verified', 'Common House Geckos abundant around street lights'),
(13, 16, '2025-12-01', 2, 'Lisa Chen', 'lisa@email.com', 'verified', 'Olive Ridley Turtles nesting on beach'),
(14, 20, '2025-12-02', 1, 'Mark Johnson', '09154321098', 'pending', 'Green Turtle spotted in seagrass area'),
(15, 13, '2025-12-03', 1, 'Sarah Lee', 'sarah@email.com', 'verified', 'Hawksbill Turtle near coral reef'),
(16, 11, '2025-12-04', 3, 'David Kim', '09143210987', 'verified', 'Whale Sharks feeding in open water'),
(17, 10, '2025-12-05', 6, 'Emily Wang', 'emily@email.com', 'pending', 'Blacktip Reef Sharks in shallow lagoon'),
(18, 16, '2025-12-01', 2, 'Michael Brown', '09132109876', 'verified', 'Manta Rays filter feeding near surface'),
(19, 1, '2025-12-02', 25, 'Jennifer Davis', 'jennifer@email.com', 'verified', 'Pod of Spinner Dolphins spotted offshore'),
(20, 20, '2025-12-03', 1, 'Chris Wilson', '09121098765', 'pending', 'Possible Dwarf Sperm Whale sighting - needs verification'),
(1, 15, '2025-12-06', 8, 'Patricia Martin', 'patricia@email.com', 'pending', 'Philippine Ducks in irrigation canal'),
(3, 14, '2025-12-07', 6, 'James Taylor', '09119876543', 'verified', 'Garden Sunbirds in residential garden');

-- INSERT DATA: ACTIVITY_LOG (sample records)
INSERT INTO activity_log (user_id, action_type, description, ip_address) VALUES
(1, 'User Login', 'Admin logged in successfully', '192.168.1.1'),
(1, 'Create Report', 'Created environmental report #1', '192.168.1.1'),
(2, 'User Login', 'User logged in', '192.168.1.2'),
(2, 'Add Sighting', 'Added new species sighting', '192.168.1.2'),
(1, 'Update Report', 'Updated report #1 status', '192.168.1.1'),
(1, 'Delete User', 'Deleted inactive user account', '192.168.1.1');

-- INSERT DATA: DASHBOARD_STATS
INSERT INTO dashboard_stats (stat_date, total_reports, pending_reports, completed_reports, critical_reports, total_sightings, verified_sightings, land_species_count, water_species_count) VALUES
('2025-12-07', 10, 5, 2, 3, 20, 12, 12, 8);

-- SQL QUERIES (SQLite Syntax)

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

-- 15. GET RECENT SIGHTINGS (Last 30 days) - SQLite syntax
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
    GROUP_CONCAT(common_name, ', ') AS species_list
FROM species
GROUP BY category, species_type
ORDER BY category, species_type;