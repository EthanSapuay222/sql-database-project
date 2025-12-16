from flask import Blueprint, request, jsonify
from model import Species

api_species = Blueprint('api_species', __name__, url_prefix='/api/species')


@api_species.route('', methods=['GET'])
def get_species():
    """
    Get all species with optional filtering
    Query params: category (land/water), type (bird/mammal/reptile/fish)
    """
    category = request.args.get('category')
    species_type = request.args.get('type')
    
    query = Species.query
    
    if category:
        query = query.filter_by(category=category)
    if species_type:
        query = query.filter_by(species_type=species_type)
    
    species_list = query.all()
    return jsonify({
        'success': True,
        'count': len(species_list),
        'data': [s.to_dict() for s in species_list]
    })


@api_species.route('/<int:species_id>', methods=['GET'])
def get_species_by_id(species_id):
    """Get single species by ID"""
    species = Species.query.get_or_404(species_id)
    return jsonify({
        'success': True,
        'data': species.to_dict()
    })


@api_species.route('/search', methods=['GET'])
def search_species():
    """Search species by common or scientific name"""
    query = request.args.get('q', '')
    
    if not query:
        return jsonify({
            'success': False,
            'message': 'Search query is required'
        }), 400
    
    species_list = Species.query.filter(
        (Species.common_name.ilike(f'%{query}%')) | 
        (Species.scientific_name.ilike(f'%{query}%'))
    ).all()
    
    return jsonify({
        'success': True,
        'count': len(species_list),
        'data': [s.to_dict() for s in species_list]
    })
