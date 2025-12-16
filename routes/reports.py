from flask import Blueprint, request, jsonify
from datetime import date
from model import EnvironmentalReport, Location, ReportCategory, ReportSeverity, Sighting, Species, DashboardStats
from database import db

api_reports = Blueprint('api_reports', __name__, url_prefix='/api/reports')


@api_reports.route('', methods=['GET'])
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


@api_reports.route('/<int:report_id>', methods=['GET'])
def get_report_by_id(report_id):
    """Get single report by ID"""
    report = EnvironmentalReport.query.get_or_404(report_id)
    return jsonify({
        'success': True,
        'data': report.to_dict()
    })


@api_reports.route('', methods=['POST'])
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
        from datetime import datetime
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

        # Update today's dashboard stats
        try:
            today = date.today()
            stats = DashboardStats.query.filter_by(stat_date=today).first()
            if stats:
                stats.total_reports = stats.total_reports + 1
                if new_report.status == 'pending':
                    stats.pending_reports = stats.pending_reports + 1
                if new_report.severity == 'Critical':
                    stats.critical_reports = stats.critical_reports + 1
                db.session.commit()
            else:
                # Create fresh stats for today
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
        except Exception:
            # Non-fatal: do not block report creation if dashboard update fails
            db.session.rollback()

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


@api_reports.route('/<int:report_id>', methods=['PUT'])
def update_report_status(report_id):
    """Update report status"""
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


@api_reports.route('/categories', methods=['GET'])
def get_categories():
    """Get all report categories"""
    categories = ReportCategory.query.all()
    return jsonify({
        'success': True,
        'count': len(categories),
        'data': [c.to_dict() for c in categories]
    })


@api_reports.route('/severity', methods=['GET'])
def get_severity():
    """Get all report severity levels"""
    severity_levels = ReportSeverity.query.all()
    return jsonify({
        'success': True,
        'count': len(severity_levels),
        'data': [s.to_dict() for s in severity_levels]
    })
