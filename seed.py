#!/usr/bin/env python
"""
Master Seed Script - Populates all reference data into the database
=================================================================

This script seeds the following tables:
  1. Locations (34 Batangas cities & municipalities)
  2. Report Categories (5 categories: Pollution, Deforestation, Waste Dumping, Wildlife Incident, Other)
  3. Report Severity Levels (4 levels: Low, Medium, High, Critical)

Usage: python seed.py

Tracking:
- v1.0 (Dec 6, 2025): Initial combined seed with locations, categories, severity
- Added locations: 34 Batangas locations with lat/long and severity levels
- Added categories: 5 environmental report types
- Added severity: 4-level severity scale
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app
from model import Location, ReportCategory, ReportSeverity
from database import db


# ============================================================================
# SECTION 1: LOCATIONS DATA
# ============================================================================
# 34 locations covering Batangas: 5 cities + 29 municipalities
# Fields: city_name, location_type (city/municipality), latitude, longitude, severity_level

SAMPLE_LOCATIONS = [
    # CITIES
    {'city_name': 'Batangas City', 'latitude': 13.7562, 'location_type': 'city', 'longitude': 121.0573, 'severity_level': 'Critical'},
    {'city_name': 'Calaca', 'latitude': 13.9303, 'location_type': 'city', 'longitude': 120.8128, 'severity_level': 'Low'},
    {'city_name': 'Lipa City', 'latitude': 13.9483, 'location_type': 'city', 'longitude': 121.1683, 'severity_level': 'High'},
    {'city_name': 'Santo Tomas', 'latitude': 14.08, 'location_type': 'city', 'longitude': 121.14, 'severity_level': 'Medium'},
    {'city_name': 'Tanauan City', 'latitude': 14.0844, 'location_type': 'city', 'longitude': 121.1492, 'severity_level': 'Critical'},

    # MUNICIPALITIES
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


# ============================================================================
# SECTION 2: REPORT CATEGORIES DATA
# ============================================================================
# 5 categories for environmental reports
# Used in submission form dropdown and dashboard filtering

SAMPLE_CATEGORIES = [
    {'name': 'Pollution', 'description': 'Air, water, soil, or noise pollution'},
    {'name': 'Deforestation', 'description': 'Illegal or unauthorized forest clearing'},
    {'name': 'Waste Dumping', 'description': 'Illegal waste disposal'},
    {'name': 'Wildlife Incident', 'description': 'Wildlife injury, trafficking, or habitat issues'},
    {'name': 'Other', 'description': 'Other environmental concerns'},
]


# ============================================================================
# SECTION 3: REPORT SEVERITY LEVELS DATA
# ============================================================================
# 4 severity levels for environmental reports
# Used in submission form dropdown and dashboard stats

SAMPLE_SEVERITY = [
    {'level': 'Low', 'description': 'Minor environmental impact, non-urgent'},
    {'level': 'Medium', 'description': 'Moderate impact, should be addressed soon'},
    {'level': 'High', 'description': 'Significant impact, requires prompt action'},
    {'level': 'Critical', 'description': 'Severe impact, immediate action required'},
]


# ============================================================================
# SEEDING FUNCTIONS
# ============================================================================

def seed_locations():
    """Seed locations table with upsert logic (insert or update)"""
    inserted = 0
    updated = 0

    for loc in SAMPLE_LOCATIONS:
        existing = Location.query.filter_by(city_name=loc['city_name']).first()
        if existing:
            # Update fields if they've changed
            changed = False
            if existing.location_type != loc['location_type']:
                existing.location_type = loc['location_type']
                changed = True
            if existing.latitude != loc['latitude']:
                existing.latitude = loc['latitude']
                changed = True
            if existing.longitude != loc['longitude']:
                existing.longitude = loc['longitude']
                changed = True
            if existing.severity_level != loc['severity_level']:
                existing.severity_level = loc['severity_level']
                changed = True

            if changed:
                updated += 1
        else:
            new_loc = Location(
                city_name=loc['city_name'],
                location_type=loc['location_type'],
                latitude=loc['latitude'],
                longitude=loc['longitude'],
                severity_level=loc['severity_level'],
                total_reports=0,
            )
            db.session.add(new_loc)
            inserted += 1

    if inserted or updated:
        db.session.commit()

    return inserted, updated


def seed_categories():
    """Seed report categories table with upsert logic"""
    inserted = 0
    updated = 0

    for cat_data in SAMPLE_CATEGORIES:
        existing = ReportCategory.query.filter_by(name=cat_data['name']).first()
        if existing:
            # Update description if changed
            if existing.description != cat_data.get('description'):
                existing.description = cat_data.get('description')
                updated += 1
        else:
            new_cat = ReportCategory(
                name=cat_data['name'],
                description=cat_data.get('description')
            )
            db.session.add(new_cat)
            inserted += 1

    if inserted or updated:
        db.session.commit()

    return inserted, updated


def seed_severity():
    """Seed report severity levels table with upsert logic"""
    inserted = 0
    updated = 0

    for sev_data in SAMPLE_SEVERITY:
        existing = ReportSeverity.query.filter_by(level=sev_data['level']).first()
        if existing:
            # Update description if changed
            if existing.description != sev_data.get('description'):
                existing.description = sev_data.get('description')
                updated += 1
        else:
            new_sev = ReportSeverity(
                level=sev_data['level'],
                description=sev_data.get('description')
            )
            db.session.add(new_sev)
            inserted += 1

    if inserted or updated:
        db.session.commit()

    return inserted, updated


def main():
    """Run all seeding operations"""
    with app.app_context():
        print("=" * 70)
        print("🌱 MASTER SEED - EcoTrack Database Initialization")
        print("=" * 70)

        # Seed Locations
        print("\n[1/3] Seeding Locations (34 Batangas cities & municipalities)...")
        loc_inserted, loc_updated = seed_locations()
        print(f"      ✅ Locations - Inserted: {loc_inserted}, Updated: {loc_updated}")

        # Seed Categories
        print("\n[2/3] Seeding Report Categories (5 types)...")
        cat_inserted, cat_updated = seed_categories()
        print(f"      ✅ Categories - Inserted: {cat_inserted}, Updated: {cat_updated}")

        # Seed Severity
        print("\n[3/3] Seeding Report Severity Levels (4 levels)...")
        sev_inserted, sev_updated = seed_severity()
        print(f"      ✅ Severity Levels - Inserted: {sev_inserted}, Updated: {sev_updated}")

        print("\n" + "=" * 70)
        print("✅ SEEDING COMPLETE!")
        print("=" * 70)
        print(f"\nTotal Summary:")
        print(f"  - Locations:  {loc_inserted} inserted, {loc_updated} updated")
        print(f"  - Categories: {cat_inserted} inserted, {cat_updated} updated")
        print(f"  - Severity:   {sev_inserted} inserted, {sev_updated} updated")
        print("\n")


if __name__ == '__main__':
    main()
