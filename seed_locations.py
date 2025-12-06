"""Seed example locations into the database.

Run: python seed_locations.py
"""
from app import app
from model import Location
from database import db

SAMPLE_LOCATIONS = [
    {'city_name': 'Batangas City', 'latitude': 13.7562, 'location_type': 'city', 'longitude': 121.0573, 'severity_level': 'Critical'},
    {'city_name': 'Calaca', 'latitude': 13.9303, 'location_type': 'city', 'longitude': 120.8128, 'severity_level': 'Low'},
    {'city_name': 'Lipa City', 'latitude': 13.9483, 'location_type': 'city', 'longitude': 121.1683, 'severity_level': 'High'},
    {'city_name': 'Santo Tomas', 'latitude': 14.08, 'location_type': 'city', 'longitude': 121.14, 'severity_level': 'Medium'},
    {'city_name': 'Tanauan City', 'latitude': 14.0844, 'location_type': 'city', 'longitude': 121.1492, 'severity_level': 'Critical'},

    {'city_name': 'Agoncillo', 'latitude': 13.9342, 'location_type': 'municipality', 'longitude': 120.9283, 'severity_level': 'Low'},
    {'city_name': 'Alitagtag', 'latitude': 13.8653, 'location_type': 'municipality', 'longitude': 121.0047, 'severity_level': 'Low'},
    {'city_name': 'Balayan', 'latitude': 13.9442, 'location_type': 'municipality', 'longitude': 120.7336, 'severity_level': 'Medium'},
    {'city_name': 'Balete', 'latitude': 14.0167, 'location_type': 'municipality', 'longitude': 121.0833, 'severity_level': 'Low'},
    {'city_name': 'Bauan', 'latitude': 13.7925, 'location_type': 'municipality', 'longitude': 121.0078, 'severity_level': 'High'},
    {'city_name': 'Calatagan', 'latitude': 13.8322, 'location_type': 'municipality', 'longitude': 120.6275, 'severity_level': 'Low'},
    {'city_name': 'Cuenca', 'latitude': 13.9167, 'location_type': 'municipality', 'longitude': 121.05, 'severity_level': 'Medium'},
    {'city_name': 'Ibaan', 'latitude': 13.8211, 'location_type': 'municipality', 'longitude': 121.1444, 'severity_level': 'Low'},
    {'city_name': 'Laurel', 'latitude': 14.05, 'location_type': 'municipality', 'longitude': 120.9333, 'severity_level': 'Medium'},
    {'city_name': 'Lemery', 'latitude': 13.9011, 'location_type': 'municipality', 'longitude': 120.8928, 'severity_level': 'Medium'},
    {'city_name': 'Lian', 'latitude': 13.9875, 'location_type': 'municipality', 'longitude': 120.6558, 'severity_level': 'Low'},
    {'city_name': 'Lobo', 'latitude': 13.6267, 'location_type': 'municipality', 'longitude': 121.2142, 'severity_level': 'High'},
    {'city_name': 'Mabini', 'latitude': 13.7639, 'location_type': 'municipality', 'longitude': 120.9417, 'severity_level': 'Critical'},
    {'city_name': 'Malvar', 'latitude': 14.0322, 'location_type': 'municipality', 'longitude': 121.155, 'severity_level': 'Low'},
    {'city_name': 'Mataasnakahoy', 'latitude': 14.0203, 'location_type': 'municipality', 'longitude': 121.1111, 'severity_level': 'Medium'},
    {'city_name': 'Nasugbu', 'latitude': 14.0722, 'location_type': 'municipality', 'longitude': 120.6358, 'severity_level': 'High'},
    {'city_name': 'Padre Garcia', 'latitude': 13.8967, 'location_type': 'municipality', 'longitude': 121.2339, 'severity_level': 'Low'},
    {'city_name': 'Rosario', 'latitude': 13.8589, 'location_type': 'municipality', 'longitude': 121.2339, 'severity_level': 'Medium'},
    {'city_name': 'San Jose', 'latitude': 13.8825, 'location_type': 'municipality', 'longitude': 121.1067, 'severity_level': 'Low'},
    {'city_name': 'San Juan', 'latitude': 13.8167, 'location_type': 'municipality', 'longitude': 121.3833, 'severity_level': 'Critical'},
    {'city_name': 'San Luis', 'latitude': 13.8561, 'location_type': 'municipality', 'longitude': 120.9389, 'severity_level': 'Medium'},
    {'city_name': 'San Nicolas', 'latitude': 13.9458, 'location_type': 'municipality', 'longitude': 120.9633, 'severity_level': 'High'},
    {'city_name': 'San Pascual', 'latitude': 13.8058, 'location_type': 'municipality', 'longitude': 120.9828, 'severity_level': 'Medium'},
    {'city_name': 'Santa Teresita', 'latitude': 13.85, 'location_type': 'municipality', 'longitude': 120.9833, 'severity_level': 'Low'},
    {'city_name': 'Taal', 'latitude': 13.8767, 'location_type': 'municipality', 'longitude': 120.9233, 'severity_level': 'High'},
    {'city_name': 'Talisay', 'latitude': 14.095, 'location_type': 'municipality', 'longitude': 121.0142, 'severity_level': 'Low'},
    {'city_name': 'Taysan', 'latitude': 13.7667, 'location_type': 'municipality', 'longitude': 121.1714, 'severity_level': 'Medium'},
    {'city_name': 'Tingloy', 'latitude': 13.7333, 'location_type': 'municipality', 'longitude': 120.8667, 'severity_level': 'Low'},
    {'city_name': 'Tuy', 'latitude': 14.0167, 'location_type': 'municipality', 'longitude': 120.75, 'severity_level': 'Low'},
]


def seed():
    with app.app_context():
        inserted = 0
        updated = 0

        for loc in SAMPLE_LOCATIONS:
            existing = Location.query.filter_by(city_name=loc['city_name']).first()
            if existing:
                # update fields if they've changed
                changed = False
                if existing.location_type != loc['location_type']:
                    existing.location_type = loc['location_type']; changed = True
                if existing.latitude != loc['latitude']:
                    existing.latitude = loc['latitude']; changed = True
                if existing.longitude != loc['longitude']:
                    existing.longitude = loc['longitude']; changed = True
                if existing.severity_level != loc['severity_level']:
                    existing.severity_level = loc['severity_level']; changed = True

                if changed:
                    updated += 1
            else:
                l = Location(
                    city_name=loc['city_name'],
                    location_type=loc['location_type'],
                    latitude=loc['latitude'],
                    longitude=loc['longitude'],
                    severity_level=loc['severity_level'],
                    total_reports=0,
                )
                db.session.add(l)
                inserted += 1

        if inserted or updated:
            db.session.commit()

        print(f"Seed complete. Inserted: {inserted}, Updated: {updated}.")


if __name__ == '__main__':
    seed()
