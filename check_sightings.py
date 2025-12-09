from app import app
from model import Sighting

with app.app_context():
    sightings = Sighting.query.order_by(Sighting.sighting_date.desc()).limit(10).all()
    print(f'Total sightings in database: {len(sightings)}')
    print('\nSightings ordered by sighting_date (DESC):')
    for s in sightings:
        species_name = s.species.common_name if s.species else "Unknown"
        location_name = s.location.city_name if s.location else "Unknown"
        print(f'  - ID {s.sighting_id}: {s.observer_name} | {species_name} | {location_name} | Sighting Date: {s.sighting_date}')

