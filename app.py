

from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_cors import CORS
from datetime import date, datetime

# Import database configuration
from database import init_db, create_tables, db

# Import models
from model import (
    Species, Location, Sighting, EnvironmentalReport, 
    User, ActivityLog, DashboardStats
)

# Import forms
from forms import SightingForm, EnvironmentalReportForm


app = Flask(__name__)

# Secret key for sessions and CSRF protection
app.config['SECRET_KEY'] = 'your-secret-key-change-this-in-production'

# Initialize CORS
CORS(app)

# Initialize database
init_db(app)


@app.route('/')
def index():
    """Homepage"""
    return render_template('FP.html')

@app.route('/api/species', methods=['GET'])
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


@app.route('/api/species/<int:species_id>', methods=['GET'])
def get_species_by_id(species_id):
    """Get single species by ID"""
    species = Species.query.get_or_404(species_id)
    return jsonify({
        'success': True,
        'data': species.to_dict()
    })


@app.route('/api/species/search', methods=['GET'])
def search_species():

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


@app.route('/api/locations', methods=['GET'])
def get_locations():

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


@app.route('/api/locations/<int:location_id>', methods=['GET'])
def get_location_by_id(location_id):
    """Get single location by ID"""
    location = Location.query.get_or_404(location_id)
    return jsonify({
        'success': True,
        'data': location.to_dict()
    })


@app.route('/api/sightings', methods=['GET'])
def get_sightings():

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
    
    sightings = query.order_by(Sighting.sighting_date.desc()).limit(limit).all()
    
    return jsonify({
        'success': True,
        'count': len(sightings),
        'data': [s.to_dict() for s in sightings]
    })


@app.route('/api/sightings/<int:sighting_id>', methods=['GET'])
def get_sighting_by_id(sighting_id):
    """Get single sighting by ID"""
    sighting = Sighting.query.get_or_404(sighting_id)
    return jsonify({
        'success': True,
        'data': sighting.to_dict()
    })


@app.route('/api/sightings', methods=['POST'])
def create_sighting():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['species_id', 'location_id', 'sighting_date', 'observer_name', 'observer_contact']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'message': f'Missing required field: {field}'
                }), 400
        
        # Create new sighting
        new_sighting = Sighting(
            species_id=data['species_id'],
            location_id=data['location_id'],
            sighting_date=datetime.strptime(data['sighting_date'], '%Y-%m-%d').date(),
            sighting_time=datetime.strptime(data['sighting_time'], '%H:%M:%S').time() if data.get('sighting_time') else None,
            number_observed=data.get('number_observed', 1),
            observer_name=data['observer_name'],
            observer_contact=data['observer_contact'],
            notes=data.get('notes'),
            photo_url=data.get('photo_url')
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


@app.route('/api/sightings/<int:sighting_id>', methods=['PUT'])
def update_sighting_status(sighting_id):
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

@app.route('/api/reports', methods=['GET'])
def get_reports():
    """
    Get all environmental reports with optional filtering
    Query params: location_id, type, status, severity
    """
    location_id = request.args.get('location_id')
    report_type = request.args.get('type')
    status = request.args.get('status')
    severity = request.args.get('severity')
    limit = request.args.get('limit', 100, type=int)
    
    query = EnvironmentalReport.query
    
    if location_id:
        query = query.filter_by(location_id=location_id)
    if report_type:
        query = query.filter_by(report_type=report_type)
    if status:
        query = query.filter_by(status=status)
    if severity:
        query = query.filter_by(severity=severity)
    
    reports = query.order_by(EnvironmentalReport.report_date.desc()).limit(limit).all()
    
    return jsonify({
        'success': True,
        'count': len(reports),
        'data': [r.to_dict() for r in reports]
    })


@app.route('/api/reports/<int:report_id>', methods=['GET'])
def get_report_by_id(report_id):
    """Get single report by ID"""
    report = EnvironmentalReport.query.get_or_404(report_id)
    return jsonify({
        'success': True,
        'data': report.to_dict()
    })


@app.route('/api/reports', methods=['POST'])
def create_report():
    """Submit new environmental report"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['location_id', 'report_type', 'severity', 'title', 'description', 'reporter_name', 'reporter_contact', 'report_date']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'message': f'Missing required field: {field}'
                }), 400
        
        # Create new report
        new_report = EnvironmentalReport(
            location_id=data['location_id'],
            report_type=data['report_type'],
            severity=data['severity'],
            title=data['title'],
            description=data['description'],
            reporter_name=data['reporter_name'],
            reporter_contact=data['reporter_contact'],
            report_date=datetime.strptime(data['report_date'], '%Y-%m-%d').date(),
            photo_url=data.get('photo_url')
        )
        
        db.session.add(new_report)
        
        # Update location total_reports count
        location = Location.query.get(data['location_id'])
        if location:
            location.total_reports += 1
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Report submitted successfully',
            'data': new_report.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error creating report: {str(e)}'
        }), 500


@app.route('/api/reports/<int:report_id>', methods=['PUT'])
def update_report_status(report_id):
    try:
        report = EnvironmentalReport.query.get_or_404(report_id)
        data = request.get_json()
        
        if 'status' in data:
            if data['status'] not in ['pending', 'in_progress', 'completed', 'closed']:
                return jsonify({
                    'success': False,
                    'message': 'Invalid status'
                }), 400
            
            report.status = data['status']
            
            # Set resolution date if completed
            if data['status'] == 'completed' and not report.resolution_date:
                report.resolution_date = date.today()
            
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Report status updated',
                'data': report.to_dict()
            })
        
        return jsonify({
            'success': False,
            'message': 'No status provided'
        }), 400
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error updating report: {str(e)}'
        }), 500

@app.route('/api/dashboard/stats', methods=['GET'])
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


@app.route('/api/dashboard/sightings-by-location', methods=['GET'])
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


@app.route('/api/dashboard/reports-by-type', methods=['GET'])
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

@app.route('/map')
def map_view():
    return render_template('Interactive Map.html')


@app.route('/species')
def species_view():
    return render_template('Life on Land and Water.html')


@app.route('/dashboard')
def dashboard_view():
    """Environmental dashboard page"""
    return render_template('Environmental Dashboard.html')


@app.route('/about')
def about_view():
    """About page"""
    return render_template('About Button.html')


@app.route('/resources')
def resources_view():
    """Resources and credits page"""
    return render_template('Resources and Credits.html')


@app.route('/submission-report')
def submission_report_view():
    """Submission report page (static template)"""
    return render_template('Submission Report.html')

# ERROR HANDLERS

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'message': 'Resource not found'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({
        'success': False,
        'message': 'Internal server error'
    }), 500

# RUN APPLICATION

if __name__ == '__main__':
    # Create tables if they don't exist
    with app.app_context():
        create_tables(app)
    
    # Run the application
    app.run(debug=True, host='0.0.0.0', port=5000)