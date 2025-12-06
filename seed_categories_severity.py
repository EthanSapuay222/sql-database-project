#!/usr/bin/env python
"""
Seed script for report categories and severity levels.
Usage: python seed_categories_severity.py
"""
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from model import ReportCategory, ReportSeverity


SAMPLE_CATEGORIES = [
    {'name': 'Pollution', 'description': 'Air, water, soil, or noise pollution'},
    {'name': 'Deforestation', 'description': 'Illegal or unauthorized forest clearing'},
    {'name': 'Waste Dumping', 'description': 'Illegal waste disposal'},
    {'name': 'Wildlife Incident', 'description': 'Wildlife injury, trafficking, or habitat issues'},
    {'name': 'Other', 'description': 'Other environmental concerns'},
]

SAMPLE_SEVERITY = [
    {'level': 'Low', 'description': 'Minor environmental impact, non-urgent'},
    {'level': 'Medium', 'description': 'Moderate impact, should be addressed soon'},
    {'level': 'High', 'description': 'Significant impact, requires prompt action'},
    {'level': 'Critical', 'description': 'Severe impact, immediate action required'},
]


def seed_categories_and_severity():
    """Insert categories and severity levels into database using upsert pattern"""
    with app.app_context():
        # Seed categories
        inserted_categories = 0
        updated_categories = 0
        
        for cat_data in SAMPLE_CATEGORIES:
            existing = ReportCategory.query.filter_by(name=cat_data['name']).first()
            if existing:
                # Update description if changed
                if existing.description != cat_data.get('description'):
                    existing.description = cat_data.get('description')
                    db.session.commit()
                    updated_categories += 1
            else:
                # Insert new category
                new_cat = ReportCategory(
                    name=cat_data['name'],
                    description=cat_data.get('description')
                )
                db.session.add(new_cat)
                db.session.commit()
                inserted_categories += 1
        
        print(f"✅ Categories - Inserted: {inserted_categories}, Updated: {updated_categories}")
        
        # Seed severity levels
        inserted_severity = 0
        updated_severity = 0
        
        for sev_data in SAMPLE_SEVERITY:
            existing = ReportSeverity.query.filter_by(level=sev_data['level']).first()
            if existing:
                # Update description if changed
                if existing.description != sev_data.get('description'):
                    existing.description = sev_data.get('description')
                    db.session.commit()
                    updated_severity += 1
            else:
                # Insert new severity level
                new_sev = ReportSeverity(
                    level=sev_data['level'],
                    description=sev_data.get('description')
                )
                db.session.add(new_sev)
                db.session.commit()
                inserted_severity += 1
        
        print(f"✅ Severity Levels - Inserted: {inserted_severity}, Updated: {updated_severity}")
        print("✅ Categories and Severity seeding complete!")


if __name__ == '__main__':
    seed_categories_and_severity()
