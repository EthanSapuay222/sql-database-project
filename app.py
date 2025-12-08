

from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from flask_cors import CORS
from datetime import date, datetime, timedelta
import datetime as datetime_module

# Import database configuration
from database import init_db, create_tables, db

# Import models
from model import (
    Species, Location, Sighting, EnvironmentalReport, 
    User, ActivityLog, DashboardStats,
    ReportCategory, ReportSeverity
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
    """Homepage - show FP if authenticated, otherwise show login"""
    if 'user_id' in session:
        return render_template('FP.html')
    else:
        return render_template('Login.html')

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
        required_fields = ['species_id', 'location_id', 'observer_name', 'observer_contact']
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
            number_observed=data.get('number_observed', 1),
            observer_name=data['observer_name'],
            observer_contact=data['observer_contact'],
            notes=data.get('notes')
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


@app.route('/api/categories', methods=['GET'])
def get_categories():
    """Get all report categories"""
    categories = ReportCategory.query.all()
    return jsonify({
        'success': True,
        'count': len(categories),
        'data': [c.to_dict() for c in categories]
    })


@app.route('/api/severity', methods=['GET'])
def get_severity():
    """Get all report severity levels"""
    severity_levels = ReportSeverity.query.all()
    return jsonify({
        'success': True,
        'count': len(severity_levels),
        'data': [s.to_dict() for s in severity_levels]
    })


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

        # Update today's dashboard stats (incremental)
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
    """Species page with all land and water animals from database"""
    land_species = Species.query.filter_by(category='land').all()
    water_species = Species.query.filter_by(category='water').all()
    return render_template('Life on Land and Water.html', land_species=land_species, water_species=water_species)


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
    """Submission report page with locations, categories, and severity from database"""
    locations = Location.query.all()
    categories = ReportCategory.query.all()
    severity = ReportSeverity.query.all()
    return render_template('Submission Report.html', locations=locations, categories=categories, severity=severity)


# AUTHENTICATION ROUTES

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Display login page or handle login form submission"""
    if request.method == 'GET':
        return render_template('Login.html')
    
    # POST requests are handled by specific routes below
    return redirect(url_for('login'))


@app.route('/user_login', methods=['POST'])
def user_login():
    """Handle user login via username"""
    try:
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        # Validation
        if not username or not password:
            flash('Username and password are required', 'user_error')
            return render_template('Login.html')
        
        # Find user by username
        user = User.query.filter_by(username=username).first()
        
        if not user or user.password != password:
            flash('Invalid username or password', 'user_error')
            return render_template('Login.html')
        
        if not user.is_active:
            flash('Your account has been deactivated', 'user_error')
            return render_template('Login.html')
        
        # Create session
        session['user_id'] = user.user_id
        session['username'] = user.username
        session['user_role'] = user.user_role
        
        try:
            # Update last login
            user.last_login = datetime.now()
            db.session.commit()
            
            # Log activity
            activity = ActivityLog(
                user_id=user.user_id,
                action_type='User Login',
                description=f'User {user.username} logged in',
                created_at=datetime.now()
            )
            db.session.add(activity)
            db.session.commit()
        except Exception as log_error:
            app.logger.warning(f"Could not log activity: {str(log_error)}")
            # Continue anyway, don't block login
        
        flash(f'Welcome back, {user.full_name}!', 'register_success')
        return redirect(url_for('index'))
        
    except Exception as e:
        app.logger.error(f"Login error: {str(e)}", exc_info=True)
        flash('An error occurred during login', 'user_error')
        return render_template('Login.html')


@app.route('/user_register', methods=['POST'])
def user_register():
    """Handle user registration"""
    try:
        full_name = request.form.get('full_name', '').strip()
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        confirm_password = request.form.get('confirm_password', '').strip()
        
        # Validation
        errors = []
        
        if not all([full_name, username, password, confirm_password]):
            errors.append('All fields are required')
        
        if len(username) < 3:
            errors.append('Username must be at least 3 characters')
        
        if len(password) < 6:
            errors.append('Password must be at least 6 characters')
        
        if password != confirm_password:
            errors.append('Passwords do not match')
        
        # Check for existing user
        if User.query.filter_by(username=username).first():
            errors.append('Username already taken')
        
        if errors:
            return jsonify({
                'success': False,
                'errors': errors
            }), 400
        
        # Create new user
        new_user = User(
            username=username,
            password=password,
            full_name=full_name,
            user_role='public',  # Default role for new users
            is_active=True
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        # Log activity
        activity = ActivityLog(
            user_id=new_user.user_id,
            action_type='User Registration',
            description=f'New user {username} registered',
            created_at=datetime.now()
        )
        db.session.add(activity)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Account created successfully! You can now log in.'
        }), 201
        
    except Exception as e:
        app.logger.error(f"Registration error: {str(e)}")
        return jsonify({
            'success': False,
            'errors': ['An error occurred during registration']
        }), 500


@app.route('/admin_login', methods=['POST'])
def admin_login():
    """Handle admin login"""
    try:
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        remember = request.form.get('remember') == 'on'
        
        # Validation
        if not username or not password:
            flash('Username and password are required', 'admin_error')
            return render_template('Login.html')
        
        # Find user by username
        user = User.query.filter_by(username=username).first()
        
        if not user or user.password != password:
            flash('Invalid username or password', 'admin_error')
            return render_template('Login.html')
        
        # Check if user is admin
        if user.user_role != 'admin':
            flash('You do not have admin privileges', 'admin_error')
            
            # Log failed admin login attempt
            activity = ActivityLog(
                user_id=user.user_id,
                action_type='Failed Admin Login',
                description=f'Non-admin user {username} attempted admin login',
                created_at=datetime.now()
            )
            db.session.add(activity)
            db.session.commit()
            
            return render_template('Login.html')
        
        if not user.is_active:
            flash('Your account has been deactivated', 'admin_error')
            return render_template('Login.html')
        
        # Create admin session
        session['user_id'] = user.user_id
        session['username'] = user.username
        session['user_role'] = user.user_role
        session['is_admin'] = True
        
        if remember:
            session.permanent = True
            app.permanent_session_lifetime = timedelta(days=7)
        
        # Update last login
        user.last_login = datetime.now()
        db.session.commit()
        
        # Log admin login
        activity = ActivityLog(
            user_id=user.user_id,
            action_type='Admin Login',
            description=f'Admin {username} logged in',
            created_at=datetime.now()
        )
        db.session.add(activity)
        db.session.commit()
        
        flash(f'Welcome, Admin {user.full_name}!', 'register_success')
        return redirect(url_for('admin_dashboard'))
        
    except Exception as e:
        app.logger.error(f"Admin login error: {str(e)}")
        flash('An error occurred during admin login', 'admin_error')
        return render_template('Login.html')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    """Handle user logout"""
    try:
        if 'user_id' in session:
            user_id = session['user_id']
            username = session.get('username', 'Unknown')
            
            # Log logout activity
            activity = ActivityLog(
                user_id=user_id,
                action_type='User Logout',
                description=f'User {username} logged out',
                created_at=datetime.now()
            )
            db.session.add(activity)
            db.session.commit()
        
        session.clear()
        flash('You have been logged out', 'register_success')
    except Exception as e:
        app.logger.error(f"Logout error: {str(e)}")
    
    return redirect(url_for('index'))


@app.route('/admin')
def admin_dashboard():
    """Admin dashboard - only accessible by admin users"""
    # Check if user is logged in and is admin
    if 'user_id' not in session:
        flash('You must be logged in to access the admin panel', 'user_error')
        return redirect(url_for('login'))
    
    if session.get('user_role') != 'admin':
        flash('You do not have permission to access the admin panel', 'user_error')
        return redirect(url_for('index'))
    
    return render_template('Admin.html')


# API ROUTES FOR ADMIN DASHBOARD

@app.route('/api/admin/reports', methods=['GET'])
def get_admin_reports():
    """Get all environmental reports for admin dashboard"""
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
                'total': len(reports_data),
                'pending': 0,
                'approved': 0
            }
        })
    except Exception as e:
        app.logger.error(f"Error fetching reports: {str(e)}")
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/admin/reports/<int:report_id>', methods=['GET'])
def get_admin_report(report_id):
    """Get a specific report for editing"""
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
                'location': report.location,
                'description': report.description,
                'severity': report.severity,
                'submitted_date': report.submitted_date.isoformat() if report.submitted_date else None,
                'submitted_by': report.submitted_by or 'Anonymous'
            }
        })
    except Exception as e:
        app.logger.error(f"Error fetching report: {str(e)}")
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/admin/reports/<int:report_id>', methods=['PUT'])
def update_admin_report(report_id):
    """Update a report"""
    if 'user_id' not in session or session.get('user_role') != 'admin':
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    try:
        report = db.session.query(EnvironmentalReport).filter_by(report_id=report_id).first()
        
        if not report:
            return jsonify({'success': False, 'message': 'Report not found'}), 404
        
        data = request.get_json()
        
        # Update fields from seed.py attributes
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
            created_at=datetime_module.datetime.now()
        )
        db.session.add(activity)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Report updated successfully'
        })
    except Exception as e:
        app.logger.error(f"Error updating report: {str(e)}")
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/admin/reports/<int:report_id>', methods=['DELETE'])
def delete_admin_report(report_id):
    """Delete a report"""
    if 'user_id' not in session or session.get('user_role') != 'admin':
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
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
            created_at=datetime_module.datetime.now()
        )
        db.session.add(activity)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Report deleted successfully'
        })
    except Exception as e:
        app.logger.error(f"Error deleting report: {str(e)}")
        return jsonify({'success': False, 'message': str(e)}), 500



# USER MANAGEMENT API ROUTES

@app.route('/api/admin/users', methods=['GET'])
def get_admin_users():
    """Get all users for admin dashboard"""
    if 'user_id' not in session or session.get('user_role') != 'admin':
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    try:
        users = db.session.query(User).all()
        users_data = [user.to_dict() for user in users]
        return jsonify({
            'success': True,
            'users': users_data
        })
    except Exception as e:
        app.logger.error(f"Error fetching users: {str(e)}")
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/admin/users/<int:user_id>', methods=['DELETE'])
def delete_admin_user(user_id):
    """Delete a user - admin only"""
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
            created_at=datetime_module.datetime.now()
        )
        db.session.add(activity)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'User {username} deleted successfully'
        })
    except Exception as e:
        app.logger.error(f"Error deleting user: {str(e)}")
        return jsonify({'success': False, 'message': str(e)}), 500


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



if __name__ == '__main__':

    with app.app_context():
        create_tables(app)
    

    app.run(debug=True, host='0.0.0.0', port=5000)