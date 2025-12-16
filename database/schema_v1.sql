DROP TABLE IF EXISTS activity_log CASCADE;
DROP TABLE IF EXISTS dashboard_stats CASCADE;
DROP TABLE IF EXISTS sightings CASCADE;
DROP TABLE IF EXISTS environmental_reports CASCADE;
DROP TABLE IF EXISTS species CASCADE;
DROP TABLE IF EXISTS locations CASCADE;
DROP TABLE IF EXISTS report_categories CASCADE;
DROP TABLE IF EXISTS report_severity CASCADE;
DROP TABLE IF EXISTS users CASCADE;

DROP TYPE IF EXISTS category_type CASCADE;
DROP TYPE IF EXISTS status_trend_type CASCADE;
DROP TYPE IF EXISTS location_type_enum CASCADE;
DROP TYPE IF EXISTS severity_type CASCADE;
DROP TYPE IF EXISTS verification_type CASCADE;
DROP TYPE IF EXISTS report_type_enum CASCADE;
DROP TYPE IF EXISTS report_status_type CASCADE;
DROP TYPE IF EXISTS user_role_type CASCADE;


-- CREATE ENUM TYPES

CREATE TYPE category_type AS ENUM ('land', 'water');
CREATE TYPE status_trend_type AS ENUM ('stable', 'increasing', 'decreasing', 'unknown');
CREATE TYPE location_type_enum AS ENUM ('city', 'municipality');
-- Keep severity enum aligned with the application model (4 levels, low->critical)
CREATE TYPE severity_type AS ENUM ('Low', 'Medium', 'High', 'Critical');
CREATE TYPE verification_type AS ENUM ('pending', 'verified', 'rejected');
-- Restrict report types to the categories used in the application model
CREATE TYPE report_type_enum AS ENUM ('pollution', 'deforestation', 'waste_dumping', 'wildlife_incident', 'other');
CREATE TYPE report_status_type AS ENUM ('pending', 'in_progress', 'completed', 'closed');
CREATE TYPE user_role_type AS ENUM ('admin', 'public');


-- Description: Stores information about wildlife species (land and water)
CREATE TABLE species (
    species_id SERIAL PRIMARY KEY,
    common_name VARCHAR(100) NOT NULL,
    scientific_name VARCHAR(150) NOT NULL,
    category category_type NOT NULL,
    species_type VARCHAR(50),
    conservation_status VARCHAR(50),
    status_trend status_trend_type,
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


-- TABLE 2: LOCATIONS

CREATE TABLE locations (
    location_id SERIAL PRIMARY KEY,
    city_name VARCHAR(100) NOT NULL,
    location_type location_type_enum NOT NULL,
    latitude DECIMAL(10,7) NOT NULL,
    longitude DECIMAL(10,7) NOT NULL,
    severity_level severity_type NOT NULL,
    total_reports INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_locations_severity ON locations(severity_level);
CREATE INDEX idx_locations_coordinates ON locations(latitude, longitude);


-- Description: Wildlife observation records linking species to locations
CREATE TABLE sightings (
    sighting_id SERIAL PRIMARY KEY,
    species_id INT NOT NULL,
    location_id INT NOT NULL,
    sighting_date DATE NOT NULL DEFAULT CURRENT_DATE,
    number_observed INT DEFAULT 1,
    observer_name VARCHAR(100),
    observer_contact VARCHAR(100),
    verification_status verification_type DEFAULT 'pending',
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_sightings_species FOREIGN KEY (species_id) REFERENCES species(species_id) ON DELETE CASCADE,
    CONSTRAINT fk_sightings_location FOREIGN KEY (location_id) REFERENCES locations(location_id) ON DELETE CASCADE
);

CREATE INDEX idx_sightings_date ON sightings(sighting_date);
CREATE INDEX idx_sightings_species ON sightings(species_id);
CREATE INDEX idx_sightings_location ON sightings(location_id);


-- TABLE 4: REPORT_CATEGORIES
CREATE TABLE report_categories (
    category_id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- TABLE 5: REPORT_SEVERITY

CREATE TABLE report_severity (
    severity_id SERIAL PRIMARY KEY,
    level VARCHAR(50) UNIQUE NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- TABLE 6: ENVIRONMENTAL_REPORTS
CREATE TABLE environmental_reports (
    report_id SERIAL PRIMARY KEY,
    location_id INT NOT NULL,
    report_type report_type_enum NOT NULL,
    severity severity_type NOT NULL,
    status report_status_type DEFAULT 'pending',
    title VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    reporter_name VARCHAR(100),
    reporter_contact VARCHAR(100),
    report_date DATE NOT NULL,
    resolution_date DATE,
    photo_url VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_reports_location FOREIGN KEY (location_id) REFERENCES locations(location_id) ON DELETE CASCADE
);

CREATE INDEX idx_reports_type ON environmental_reports(report_type);
CREATE INDEX idx_reports_status ON environmental_reports(status);
CREATE INDEX idx_reports_severity ON environmental_reports(severity);

-- TABLE 7: USERS
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    full_name VARCHAR(100),
    user_role user_role_type DEFAULT 'public',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);

CREATE INDEX idx_users_role ON users(user_role);

-- TABLE 8: ACTIVITY_LOG
CREATE TABLE activity_log (
    log_id SERIAL PRIMARY KEY,
    user_id INT,
    action_type VARCHAR(50) NOT NULL,
    description TEXT,
    ip_address VARCHAR(45),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_activity_user FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE SET NULL
);

CREATE INDEX idx_activity_user ON activity_log(user_id);
CREATE INDEX idx_activity_date ON activity_log(created_at);

-- TABLE 9: DASHBOARD_STATS
CREATE TABLE dashboard_stats (
    stat_id SERIAL PRIMARY KEY,
    stat_date DATE UNIQUE NOT NULL,
    total_reports INT DEFAULT 0,
    pending_reports INT DEFAULT 0,
    completed_reports INT DEFAULT 0,
    critical_reports INT DEFAULT 0,
    total_sightings INT DEFAULT 0,
    verified_sightings INT DEFAULT 0,
    land_species_count INT DEFAULT 0,
    water_species_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_stats_date ON dashboard_stats(stat_date);

-- FUNCTION: Auto-update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- TRIGGERS: Auto-update updated_at on UPDATE
CREATE TRIGGER update_species_updated_at 
    BEFORE UPDATE ON species
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_locations_updated_at 
    BEFORE UPDATE ON locations
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_environmental_reports_updated_at 
    BEFORE UPDATE ON environmental_reports
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();


