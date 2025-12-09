from flask import Blueprint, request, jsonify
from model import Sighting
from database import db
from datetime import datetime

api_sightings = Blueprint('api_sightings', __name__, url_prefix='/api/sightings')


@api_sightings.route('', methods=['GET'])
def get_sightings():
    """Get sightings with optional filtering"""
    species_id = request.args.get('species_id')
    location_id = request.args.get('location_id')
    status = request.args.get('status')
    limit = request.args.get('limit', 100, type=int)
    
    query = Sighting.query
    
    if species_id:
        query = query.filter_by(species_id=species_id)
    if location_id:
        query = query.filter_by(location_id=location_id)
    if status:
        query = query.filter_by(verification_status=status)
    
    sightings = query.order_by(Sighting.sighting_date.desc(), Sighting.created_at.desc()).limit(limit).all()
    
    return jsonify({
        'success': True,
        'count': len(sightings),
        'data': [s.to_dict() for s in sightings]
    })


@api_sightings.route('/<int:sighting_id>', methods=['GET'])
def get_sighting_by_id(sighting_id):
    """Get single sighting by ID"""
    sighting = Sighting.query.get_or_404(sighting_id)
    return jsonify({
        'success': True,
        'data': sighting.to_dict()
    })


@api_sightings.route('', methods=['POST'])
def create_sighting():
    """Submit new wildlife sighting"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['species_id', 'location_id', 'observer_name', 'observer_contact']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'message': f'Missing required field: {field}'
                }), 400
        
        # Create new sighting
        sighting_date = None
        if data.get('sighting_date'):
            try:
                sighting_date = datetime.strptime(data['sighting_date'], '%Y-%m-%d').date()
            except (ValueError, TypeError):
                sighting_date = None
        
        new_sighting = Sighting(
            species_id=data['species_id'],
            location_id=data['location_id'],
            number_observed=data.get('number_observed', 1),
            observer_name=data['observer_name'],
            observer_contact=data['observer_contact'],
            notes=data.get('notes'),
            sighting_date=sighting_date
        )
        
        db.session.add(new_sighting)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Sighting submitted successfully',
            'data': new_sighting.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error creating sighting: {str(e)}'
        }), 500

@api_sightings.route('/<int:sighting_id>', methods=['PUT'])
def update_sighting_status(sighting_id):
    """Update sighting verification status"""
    try:
        sighting = Sighting.query.get_or_404(sighting_id)
        data = request.get_json()
        
        if 'verification_status' in data:
            if data['verification_status'] not in ['pending', 'verified', 'rejected']:
                return jsonify({
                    'success': False,
                    'message': 'Invalid verification status'
                }), 400
            
            sighting.verification_status = data['verification_status']
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Sighting status updated',
                'data': sighting.to_dict()
            })
        
        return jsonify({
            'success': False,
            'message': 'No status provided'
        }), 400
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error updating sighting: {str(e)}'
        }), 500
