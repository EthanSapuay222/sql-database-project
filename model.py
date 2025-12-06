from database import db  # Import db from database.py
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash



# SPECIES MODEL

class Species(db.Model):
    __tablename__ = 'species'
    
    species_id = db.Column(db.Integer, primary_key=True)
    common_name = db.Column(db.String(100), nullable=False)
    scientific_name = db.Column(db.String(150), nullable=False)
    category = db.Column(db.Enum('land', 'water'), nullable=False)
    species_type = db.Column(db.String(50))  # bird, mammal, reptile, fish
    conservation_status = db.Column(db.String(50))
    status_trend = db.Column(db.Enum('stable', 'increasing', 'decreasing', 'unknown'))
    total_sightings_estimate = db.Column(db.String(50))
    description = db.Column(db.Text)
    habitat_info = db.Column(db.Text)
    diet_info = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    sightings = db.relationship('Sighting', backref='species', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'species_id': self.species_id,
            'common_name': self.common_name,
            'scientific_name': self.scientific_name,
            'category': self.category,
            'species_type': self.species_type,
            'conservation_status': self.conservation_status,
            'status_trend': self.status_trend,
            'total_sightings_estimate': self.total_sightings_estimate,
            'description': self.description,
            'habitat_info': self.habitat_info,
            'diet_info': self.diet_info
        }
    
    def __repr__(self):
        return f'<Species {self.common_name}>'


# LOCATION MODEL

class Location(db.Model):
    __tablename__ = 'locations'
    
    location_id = db.Column(db.Integer, primary_key=True)
    city_name = db.Column(db.String(100), nullable=False)
    location_type = db.Column(db.Enum('city', 'municipality'), nullable=False)
    latitude = db.Column(db.Numeric(10, 7), nullable=False)
    longitude = db.Column(db.Numeric(10, 7), nullable=False)
    severity_level = db.Column(db.Enum('Critical', 'High', 'Medium', 'Low'), nullable=False)
    total_reports = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    sightings = db.relationship('Sighting', backref='location', lazy=True)
    reports = db.relationship('EnvironmentalReport', backref='location', lazy=True)
    
    def to_dict(self):
        return {
            'location_id': self.location_id,
            'city_name': self.city_name,
            'location_type': self.location_type,
            'latitude': float(self.latitude),
            'longitude': float(self.longitude),
            'severity_level': self.severity_level,
            'total_reports': self.total_reports
        }
    
    def __repr__(self):
        return f'<Location {self.city_name}>'



# SIGHTING MODEL

class Sighting(db.Model):
    __tablename__ = 'sightings'
    
    sighting_id = db.Column(db.Integer, primary_key=True)
    species_id = db.Column(db.Integer, db.ForeignKey('species.species_id'), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('locations.location_id'), nullable=False)
    sighting_date = db.Column(db.Date, nullable=False)
    sighting_time = db.Column(db.Time)
    number_observed = db.Column(db.Integer, default=1)
    observer_name = db.Column(db.String(100))
    observer_contact = db.Column(db.String(100))
    verification_status = db.Column(db.Enum('pending', 'verified', 'rejected'), default='pending')
    notes = db.Column(db.Text)
    photo_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'sighting_id': self.sighting_id,
            'species': self.species.to_dict() if self.species else None,
            'location': self.location.to_dict() if self.location else None,
            'sighting_date': self.sighting_date.isoformat(),
            'sighting_time': self.sighting_time.isoformat() if self.sighting_time else None,
            'number_observed': self.number_observed,
            'observer_name': self.observer_name,
            'observer_contact': self.observer_contact,
            'verification_status': self.verification_status,
            'notes': self.notes,
            'photo_url': self.photo_url,
            'created_at': self.created_at.isoformat()
        }
    
    def __repr__(self):
        return f'<Sighting {self.sighting_id} - {self.species.common_name if self.species else "Unknown"}>'



# ENVIRONMENTAL REPORT MODEL

class EnvironmentalReport(db.Model):
    __tablename__ = 'environmental_reports'
    
    report_id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.Integer, db.ForeignKey('locations.location_id'), nullable=False)
    report_type = db.Column(db.Enum('pollution', 'habitat_loss', 'illegal_activity', 'wildlife_incident', 'other'), nullable=False)
    severity = db.Column(db.Enum('Critical', 'High', 'Medium', 'Low'), nullable=False)
    status = db.Column(db.Enum('pending', 'in_progress', 'completed', 'closed'), default='pending')
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    reporter_name = db.Column(db.String(100))
    reporter_contact = db.Column(db.String(100))
    report_date = db.Column(db.Date, nullable=False)
    resolution_date = db.Column(db.Date)
    photo_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'report_id': self.report_id,
            'location': self.location.to_dict() if self.location else None,
            'report_type': self.report_type,
            'severity': self.severity,
            'status': self.status,
            'title': self.title,
            'description': self.description,
            'reporter_name': self.reporter_name,
            'reporter_contact': self.reporter_contact,
            'report_date': self.report_date.isoformat(),
            'resolution_date': self.resolution_date.isoformat() if self.resolution_date else None,
            'photo_url': self.photo_url,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def __repr__(self):
        return f'<Report {self.report_id} - {self.title}>'

# USER MODEL

class User(db.Model):
    __tablename__ = 'users'
    
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(100))
    user_role = db.Column(db.Enum('admin', 'moderator', 'observer', 'public'), default='public')
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    def set_password(self, password):
        """Hash and set user password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if provided password matches hash"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'user_id': self.user_id,
            'username': self.username,
            'email': self.email,
            'full_name': self.full_name,
            'user_role': self.user_role,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'last_login': self.last_login.isoformat() if self.last_login else None
        }
    
    def __repr__(self):
        return f'<User {self.username}>'



# ACTIVITY LOG MODEL

class ActivityLog(db.Model):
    __tablename__ = 'activity_log'
    
    log_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='SET NULL'))
    action_type = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    ip_address = db.Column(db.String(45))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship
    user = db.relationship('User', backref='activity_logs')
    
    def to_dict(self):
        return {
            'log_id': self.log_id,
            'user_id': self.user_id,
            'action_type': self.action_type,
            'description': self.description,
            'ip_address': self.ip_address,
            'created_at': self.created_at.isoformat()
        }
    
    def __repr__(self):
        return f'<ActivityLog {self.log_id} - {self.action_type}>'



# DASHBOARD STATISTICS MODEL

class DashboardStats(db.Model):
    __tablename__ = 'dashboard_stats'
    
    stat_id = db.Column(db.Integer, primary_key=True)
    stat_date = db.Column(db.Date, unique=True, nullable=False)
    total_reports = db.Column(db.Integer, default=0)
    pending_reports = db.Column(db.Integer, default=0)
    completed_reports = db.Column(db.Integer, default=0)
    critical_reports = db.Column(db.Integer, default=0)
    total_sightings = db.Column(db.Integer, default=0)
    verified_sightings = db.Column(db.Integer, default=0)
    land_species_count = db.Column(db.Integer, default=0)
    water_species_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'stat_id': self.stat_id,
            'stat_date': self.stat_date.isoformat(),
            'total_reports': self.total_reports,
            'pending_reports': self.pending_reports,
            'completed_reports': self.completed_reports,
            'critical_reports': self.critical_reports,
            'total_sightings': self.total_sightings,
            'verified_sightings': self.verified_sightings,
            'land_species_count': self.land_species_count,
            'water_species_count': self.water_species_count,
            'created_at': self.created_at.isoformat()
        }
    
    def __repr__(self):
        return f'<DashboardStats {self.stat_date}>'