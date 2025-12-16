from flask import Blueprint, request, jsonify, session
from datetime import datetime as datetime_module
from model import User, EnvironmentalReport, ActivityLog, Sighting, Species, update_species_stats
from database import db

api_admin = Blueprint('api_admin', __name__, url_prefix='/api/admin')


# Debug route
@api_admin.route('/debug', methods=['GET'])
def debug_admin():
    """Debug route to check session and authorization"""
    return jsonify({
        'session_data': {
            'user_id': session.get('user_id'),
            'username': session.get('username'),
            'user_role': session.get('user_role'),
            'is_admin': session.get('user_role') == 'admin'
        },
        'request_headers': dict(request.headers),
        'cookies': dict(request.cookies)
    })


def admin_required(f):
    """Decorator to check admin authorization"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or session.get('user_role') != 'admin':
            return jsonify({'success': False, 'message': 'Unauthorized'}), 403
        return f(*args, **kwargs)
    return decorated_function


@api_admin.route('/reports', methods=['GET'])
def get_admin_reports():
    """Get all environmental reports for admin dashboard"""
    # Check admin authorization
    if 'user_id' not in session or session.get('user_role') != 'admin':
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    try:
        reports = db.session.query(EnvironmentalReport).all()
        
        reports_data = []
        for report in reports:
            reports_data.append({
                'report_id': report.report_id,
                'title': report.title,
                'description': report.description,
                'report_type': report.report_type,
                'severity': report.severity,
                'reporter_name': report.reporter_name,
                'reporter_contact': report.reporter_contact,
                'status': report.status
            })
        
        return jsonify({
            'success': True,
            'reports': reports_data,
            'stats': {
                'total': len(reports_data)
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@api_admin.route('/reports/<int:report_id>', methods=['GET'])
def get_admin_report(report_id):
    """Get a specific report for editing"""
    # Check admin authorization
    if 'user_id' not in session or session.get('user_role') != 'admin':
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    try:
        report = db.session.query(EnvironmentalReport).filter_by(report_id=report_id).first()
        
        if not report:
            return jsonify({'success': False, 'message': 'Report not found'}), 404
        
        return jsonify({
            'success': True,
            'report': {
                'report_id': report.report_id,
                'report_type': report.report_type,
                'description': report.description,
                'severity': report.severity,
                'status': report.status,
                'reporter_name': report.reporter_name
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@api_admin.route('/reports/<int:report_id>', methods=['PUT'])
def update_admin_report(report_id):
    """Update a report"""
    # Check admin authorization
    if 'user_id' not in session or session.get('user_role') != 'admin':
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    try:
        # Debug: request details
        print(f"DEBUG: PUT request to /api/admin/reports/{report_id}")
        print(f"DEBUG: Content-Type: {request.content_type}")
        print(f"DEBUG: Raw data: {request.get_data(as_text=True)}")
        
        report = db.session.query(EnvironmentalReport).filter_by(report_id=report_id).first()
        
        if not report:
            return jsonify({'success': False, 'message': 'Report not found'}), 404
        
        data = request.get_json(force=True, silent=False)
        print(f"DEBUG: Parsed JSON data: {data}")
        
        if not data:
            print("DEBUG: No data received!")
            return jsonify({'success': False, 'message': 'No data provided'}), 400
        
        # Update the fields
        if 'title' in data:
            report.title = data['title']
        if 'description' in data:
            report.description = data['description']
        if 'report_type' in data:
            report.report_type = data['report_type']
        if 'severity' in data:
            report.severity = data['severity']
        if 'reporter_name' in data:
            report.reporter_name = data['reporter_name']
        if 'reporter_contact' in data:
            report.reporter_contact = data['reporter_contact']
        if 'status' in data:
            report.status = data['status']
        
        db.session.commit()
        
        # Log activity
        activity = ActivityLog(
            user_id=session.get('user_id'),
            action_type='edit_report',
            description=f'Edited report #{report_id}',
            created_at=datetime_module.now()
        )
        db.session.add(activity)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Report updated successfully'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500


@api_admin.route('/reports/<int:report_id>', methods=['DELETE'])
def delete_admin_report(report_id):
    """Delete a report"""
    # Check admin authorization
    if 'user_id' not in session or session.get('user_role') != 'admin':
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    print(f"DEBUG DELETE: /api/admin/reports/{report_id}")
    print(f"DEBUG DELETE: Session user_id: {session.get('user_id')}")
    print(f"DEBUG DELETE: Session user_role: {session.get('user_role')}")
    
    try:
        report = db.session.query(EnvironmentalReport).filter_by(report_id=report_id).first()
        
        if not report:
            return jsonify({'success': False, 'message': 'Report not found'}), 404
        
        db.session.delete(report)
        db.session.commit()
        
        # Log activity
        activity = ActivityLog(
            user_id=session.get('user_id'),
            action_type='delete_report',
            description=f'Deleted report #{report_id}',
            created_at=datetime_module.now()
        )
        db.session.add(activity)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Report deleted successfully'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500


@api_admin.route('/users', methods=['GET'])
def get_admin_users():
    """Get all users for admin dashboard"""
    # Check admin authorization
    if 'user_id' not in session or session.get('user_role') != 'admin':
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    try:
        users = db.session.query(User).all()
        users_data = [user.to_dict() for user in users]
        return jsonify({
            'success': True,
            'data': users_data
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@api_admin.route('/users/<int:user_id>', methods=['DELETE'])
def delete_admin_user(user_id):
    """Delete a user - admin only"""
    # Check admin authorization
    if 'user_id' not in session or session.get('user_role') != 'admin':
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    try:
        # Prevent admin from deleting themselves
        if user_id == session.get('user_id'):
            return jsonify({'success': False, 'message': 'Cannot delete your own account'}), 400
        
        user = db.session.query(User).filter_by(user_id=user_id).first()
        
        if not user:
            return jsonify({'success': False, 'message': 'User not found'}), 404
        
        # Prevent deleting other admin accounts
        if user.user_role == 'admin':
            return jsonify({'success': False, 'message': 'Cannot delete admin accounts'}), 400
        
        username = user.username
        db.session.delete(user)
        db.session.commit()
        
        # Log activity
        activity = ActivityLog(
            user_id=session.get('user_id'),
            action_type='delete_user',
            description=f'Deleted user: {username}',
            created_at=datetime_module.now()
        )
        db.session.add(activity)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'User {username} deleted successfully'
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@api_admin.route('/sightings', methods=['GET'])
def get_admin_sightings():
    """Get all animal sightings for admin dashboard"""
    # Check admin authorization
    if 'user_id' not in session or session.get('user_role') != 'admin':
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    try:
        sightings = db.session.query(Sighting).order_by(Sighting.created_at.desc()).all()
        sightings_data = [sighting.to_dict() for sighting in sightings]
        return jsonify({
            'success': True,
            'data': sightings_data
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@api_admin.route('/sightings/<int:sighting_id>', methods=['DELETE'])
def delete_admin_sighting(sighting_id):
    """Delete an animal sighting - admin only"""
    # Check admin authorization
    if 'user_id' not in session or session.get('user_role') != 'admin':
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    try:
        sighting = db.session.query(Sighting).filter_by(sighting_id=sighting_id).first()
        
        if not sighting:
            return jsonify({'success': False, 'message': 'Sighting not found'}), 404
        
        species_id = sighting.species_id  # Store species_id before deletion
        species_name = sighting.species.common_name if sighting.species else 'Unknown'
        
        db.session.delete(sighting)
        db.session.commit()
        
        # Update species statistics after deletion
        update_species_stats(species_id)
        
        # Log activity
        activity = ActivityLog(
            user_id=session.get('user_id'),
            action_type='delete_sighting',
            description=f'Deleted sighting: {species_name}',
            created_at=datetime_module.now()
        )
        db.session.add(activity)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Sighting deleted successfully'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500


@api_admin.route('/species/refresh-stats', methods=['POST'])
def refresh_all_species_stats():
    """Refresh statistics for all species - admin only"""
    # Check admin authorization
    if 'user_id' not in session or session.get('user_role') != 'admin':
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    try:
        species_list = Species.query.all()
        updated_count = 0
        
        for species in species_list:
            species.update_statistics()
            updated_count += 1
        
        db.session.commit()
        
        # Log activity
        activity = ActivityLog(
            user_id=session.get('user_id'),
            action_type='refresh_stats',
            description=f'Refreshed statistics for {updated_count} species',
            created_at=datetime_module.now()
        )
        db.session.add(activity)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Statistics refreshed for {updated_count} species'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500


@api_admin.route('/sightings/<int:sighting_id>/verify', methods=['PUT'])
def verify_sighting(sighting_id):
    """Verify or reject a sighting - admin only"""
    # Check admin authorization
    if 'user_id' not in session or session.get('user_role') != 'admin':
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    try:
        sighting = db.session.query(Sighting).filter_by(sighting_id=sighting_id).first()
        
        if not sighting:
            return jsonify({'success': False, 'message': 'Sighting not found'}), 404
        
        data = request.get_json()
        new_status = data.get('status')
        
        if new_status not in ['verified', 'rejected', 'pending']:
            return jsonify({'success': False, 'message': 'Invalid status'}), 400
        
        old_status = sighting.verification_status
        sighting.verification_status = new_status
        db.session.commit()
        
        # Update species statistics when verification status changes
        update_species_stats(sighting.species_id)
        
        # Log activity
        species_name = sighting.species.common_name if sighting.species else 'Unknown'
        activity = ActivityLog(
            user_id=session.get('user_id'),
            action_type='verify_sighting',
            description=f'Changed sighting #{sighting_id} ({species_name}) from {old_status} to {new_status}',
            created_at=datetime_module.now()
        )
        db.session.add(activity)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Sighting {new_status} successfully'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500
