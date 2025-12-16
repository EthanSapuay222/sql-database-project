from flask import Blueprint, request, jsonify
from datetime import date
from model import DashboardStats, EnvironmentalReport, Sighting, Species, Location
from database import db

api_dashboard = Blueprint('api_dashboard', __name__, url_prefix='/api/dashboard')


@api_dashboard.route('/stats', methods=['GET'])
def get_dashboard_stats():
    """Get dashboard statistics for today"""
    today = date.today()
    stats = DashboardStats.query.filter_by(stat_date=today).first()
    
    if not stats:
        # Calculate stats if not exists
        stats = DashboardStats(
            stat_date=today,
            total_reports=EnvironmentalReport.query.count(),
            pending_reports=EnvironmentalReport.query.filter_by(status='pending').count(),
            completed_reports=EnvironmentalReport.query.filter_by(status='completed').count(),
            critical_reports=EnvironmentalReport.query.filter_by(severity='Critical').count(),
            total_sightings=Sighting.query.count(),
            verified_sightings=Sighting.query.filter_by(verification_status='verified').count(),
            land_species_count=Species.query.filter_by(category='land').count(),
            water_species_count=Species.query.filter_by(category='water').count()
        )
        db.session.add(stats)
        db.session.commit()
    
    return jsonify({
        'success': True,
        'data': stats.to_dict()
    })


@api_dashboard.route('/sightings-by-location', methods=['GET'])
def get_sightings_by_location():
    """Get species sightings count by location for charts"""
    category = request.args.get('category', 'land')  # 'land' or 'water'
    limit = request.args.get('limit', 10, type=int)
    
    # Query to get sightings count per location for specific category
    results = db.session.query(
        Location.city_name,
        db.func.count(Sighting.sighting_id).label('count')
    ).join(Sighting).join(Species).filter(
        Species.category == category
    ).group_by(Location.city_name).order_by(db.text('count DESC')).limit(limit).all()
    
    return jsonify({
        'success': True,
        'category': category,
        'data': [
            {'city': r.city_name, 'sightings': r.count}
            for r in results
        ]
    })


@api_dashboard.route('/reports-by-type', methods=['GET'])
def get_reports_by_type():
    """Get environmental reports count by type"""
    results = db.session.query(
        EnvironmentalReport.report_type,
        db.func.count(EnvironmentalReport.report_id).label('count')
    ).group_by(EnvironmentalReport.report_type).all()
    
    return jsonify({
        'success': True,
        'data': [
            {'type': r.report_type, 'count': r.count}
            for r in results
        ]
    })
