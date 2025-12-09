from flask import Blueprint, render_template, redirect, url_for, session, flash
from model import Location, ReportCategory, ReportSeverity, Species

pages = Blueprint('pages', __name__)


@pages.route('/')
def index():
    """Homepage - show FP if authenticated, otherwise redirect to login"""
    if 'user_id' in session:
        return render_template('FP.html')
    else:
        return redirect(url_for('auth.login'))


@pages.route('/map')
def map_view():
    """Interactive map page"""
    return render_template('Interactive Map.html')


@pages.route('/species')
def species_view():
    """Species page with all land and water animals from database"""
    land_species = Species.query.filter_by(category='land').all()
    water_species = Species.query.filter_by(category='water').all()
    return render_template('Life on Land and Water.html', land_species=land_species, water_species=water_species)


@pages.route('/dashboard')
def dashboard_view():
    """Environmental dashboard page"""
    return render_template('Environmental Dashboard.html')


@pages.route('/about')
def about_view():
    """About page"""
    return render_template('About Button.html')


@pages.route('/resources')
def resources_view():
    """Resources and credits page"""
    return render_template('Resources and Credits.html')


@pages.route('/submission-report')
def submission_report_view():
    """Submission report page with locations, categories, and severity from database"""
    locations = Location.query.all()
    categories = ReportCategory.query.all()
    severity = ReportSeverity.query.all()
    return render_template('Submission Report.html', locations=locations, categories=categories, severity=severity)


@pages.route('/admin')
def admin_dashboard():
    """Admin dashboard - only accessible by admin users"""
    # Check if user is logged in and is admin
    if 'user_id' not in session:
        flash('You must be logged in to access the admin panel', 'user_error')
        return redirect(url_for('pages.login'))
    
    if session.get('user_role') != 'admin':
        flash('You do not have permission to access the admin panel', 'user_error')
        return redirect(url_for('pages.index'))
    
    return render_template('Admin.html')


@pages.route('/admin/login', methods=['GET'])
def admin_login_view():
    """Admin login page"""
    return render_template('AdminLogin.html')


@pages.route('/login', methods=['GET'])
def login():
    """User login page"""
    return render_template('Login.html')


@pages.route('/login/admin')
def login_admin_redirect():
    """Redirect /login/admin to /admin/login for convenience"""
    return redirect(url_for('pages.admin_login_view'))
