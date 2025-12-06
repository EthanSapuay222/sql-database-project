#!/usr/bin/env python
"""
Seed Sample Environmental Reports
Creates sample reports for testing the dashboard
"""

from app import app
from model import EnvironmentalReport, Location
from database import db
from datetime import date, timedelta
import random

SAMPLE_REPORTS = [
    {
        'title': 'Illegal Waste Dumping at Batangas City Port',
        'description': 'Large amounts of industrial waste found dumped near the port area. Immediate cleanup required.',
        'report_type': 'pollution',
        'severity': 'Critical',
        'reporter_name': 'Juan Dela Cruz',
        'reporter_contact': 'juan@email.com',
        'status': 'pending'
    },
    {
        'title': 'Deforestation in Taal Watershed',
        'description': 'Unauthorized tree cutting observed in the protected watershed area.',
        'report_type': 'habitat_loss',
        'severity': 'High',
        'reporter_name': 'Maria Santos',
        'reporter_contact': 'maria@email.com',
        'status': 'in_progress'
    },
    {
        'title': 'Plastic Pollution at Nasugbu Beach',
        'description': 'Excessive plastic waste accumulating along the shoreline, affecting marine life.',
        'report_type': 'pollution',
        'severity': 'High',
        'reporter_name': 'Pedro Reyes',
        'reporter_contact': '09123456789',
        'status': 'pending'
    },
    {
        'title': 'Wildlife Trafficking Suspected',
        'description': 'Reports of illegal bird trading in the local market area.',
        'report_type': 'wildlife_incident',
        'severity': 'Critical',
        'reporter_name': 'Ana Garcia',
        'reporter_contact': 'ana.garcia@email.com',
        'status': 'in_progress'
    },
    {
        'title': 'Water Pollution in Tanauan River',
        'description': 'Factory discharge causing water discoloration and fish kill.',
        'report_type': 'pollution',
        'severity': 'High',
        'reporter_name': 'Carlos Manuel',
        'reporter_contact': '09187654321',
        'status': 'pending'
    },
    {
        'title': 'Illegal Fishing Activity',
        'description': 'Use of dynamite fishing reported in coastal areas of Mabini.',
        'report_type': 'illegal_activity',
        'severity': 'Critical',
        'reporter_name': 'Rosa Mendoza',
        'reporter_contact': 'rosa.m@email.com',
        'status': 'completed'
    },
    {
        'title': 'Air Quality Concerns in Lipa City',
        'description': 'Increased smoke emissions from industrial area affecting residents.',
        'report_type': 'pollution',
        'severity': 'Medium',
        'reporter_name': 'Jose Villanueva',
        'reporter_contact': 'jose.v@email.com',
        'status': 'in_progress'
    },
    {
        'title': 'Coral Reef Damage',
        'description': 'Boat anchors damaging coral formations in Tingloy marine sanctuary.',
        'report_type': 'habitat_loss',
        'severity': 'High',
        'reporter_name': 'Lisa Fernandez',
        'reporter_contact': '09162345678',
        'status': 'pending'
    },
    {
        'title': 'Noise Pollution from Construction',
        'description': 'Excessive noise during late hours affecting wildlife in Santo Tomas.',
        'report_type': 'other',
        'severity': 'Low',
        'reporter_name': 'Roberto Cruz',
        'reporter_contact': 'roberto@email.com',
        'status': 'completed'
    },
    {
        'title': 'Mangrove Clearing in Balayan',
        'description': 'Illegal clearing of mangrove forest for construction purposes.',
        'report_type': 'habitat_loss',
        'severity': 'Critical',
        'reporter_name': 'Elena Torres',
        'reporter_contact': 'elena.t@email.com',
        'status': 'in_progress'
    }
]

def seed_sample_reports():
    """Add sample reports to the database"""
    with app.app_context():
        print("=" * 70)
        print("🌱 Seeding Sample Environmental Reports")
        print("=" * 70)
        
        # Get all locations
        locations = Location.query.all()
        if not locations:
            print("❌ No locations found! Please run seed.py first.")
            return
        
        # Clear existing reports (optional)
        print("\n⚠️  Clearing existing reports...")
        EnvironmentalReport.query.delete()
        db.session.commit()
        
        # Add sample reports
        print("\n📝 Adding sample reports...\n")
        added = 0
        
        for i, report_data in enumerate(SAMPLE_REPORTS):
            # Randomly assign location
            location = random.choice(locations)
            
            # Create report with dates in the past few days
            days_ago = random.randint(0, 14)
            report_date = date.today() - timedelta(days=days_ago)
            
            new_report = EnvironmentalReport(
                location_id=location.location_id,
                title=report_data['title'],
                description=report_data['description'],
                report_type=report_data['report_type'],
                severity=report_data['severity'],
                status=report_data['status'],
                reporter_name=report_data['reporter_name'],
                reporter_contact=report_data['reporter_contact'],
                report_date=report_date
            )
            
            db.session.add(new_report)
            added += 1
            
            print(f"  ✓ {report_data['title']}")
            print(f"    Location: {location.city_name} | Severity: {report_data['severity']} | Status: {report_data['status']}")
        
        db.session.commit()
        
        print(f"\n✅ Successfully added {added} sample reports!")
        print("=" * 70)

if __name__ == '__main__':
    seed_sample_reports()
