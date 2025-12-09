from flask import Blueprint, request, jsonify, session
from datetime import datetime as datetime_module
from model import User, EnvironmentalReport, ActivityLog
from database import db

api_admin = Blueprint('api_admin', __name__, url_prefix='/api/admin')


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
@admin_required
def get_admin_reports():
    """Get all environmental reports for admin dashboard"""
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
@admin_required
def get_admin_report(report_id):
    """Get a specific report for editing"""
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
@admin_required
def update_admin_report(report_id):
    """Update a report"""
    try:
        report = db.session.query(EnvironmentalReport).filter_by(report_id=report_id).first()
        
        if not report:
            return jsonify({'success': False, 'message': 'Report not found'}), 404
        
        data = request.get_json()
        
        # Update fields
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
        return jsonify({'success': False, 'message': str(e)}), 500


@api_admin.route('/reports/<int:report_id>', methods=['DELETE'])
@admin_required
def delete_admin_report(report_id):
    """Delete a report"""
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
        return jsonify({'success': False, 'message': str(e)}), 500


@api_admin.route('/users', methods=['GET'])
@admin_required
def get_admin_users():
    """Get all users for admin dashboard"""
    try:
        users = db.session.query(User).all()
        users_data = [user.to_dict() for user in users]
        return jsonify({
            'success': True,
            'users': users_data
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@api_admin.route('/users/<int:user_id>', methods=['DELETE'])
@admin_required
def delete_admin_user(user_id):
    """Delete a user - admin only"""
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
