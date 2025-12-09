from flask import Blueprint, request, jsonify
from model import Location

api_locations = Blueprint('api_locations', __name__, url_prefix='/api/locations')


@api_locations.route('', methods=['GET'])
def get_locations():
    """Get all locations with optional filtering"""
    severity = request.args.get('severity')
    location_type = request.args.get('type')
    
    query = Location.query
    
    if severity:
        query = query.filter_by(severity_level=severity)
    if location_type:
        query = query.filter_by(location_type=location_type)
    
    locations = query.all()
    return jsonify({
        'success': True,
        'count': len(locations),
        'data': [loc.to_dict() for loc in locations]
    })


@api_locations.route('/<int:location_id>', methods=['GET'])
def get_location_by_id(location_id):
    """Get single location by ID"""
    location = Location.query.get_or_404(location_id)
    return jsonify({
        'success': True,
        'data': location.to_dict()
    })
