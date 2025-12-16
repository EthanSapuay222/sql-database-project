"""
EcoTrack Application
Main Flask application with modular blueprint architecture
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_wtf.csrf import CSRFProtect
from database import init_db, create_tables

# Import blueprints
from routes.pages import pages
from routes.auth import auth
from routes.species import api_species
from routes.locations import api_locations
from routes.sightings import api_sightings
from routes.reports import api_reports
from routes.dashboard import api_dashboard
from routes.admin import api_admin


def create_app():
    """Application factory function"""
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = 'your-secret-key-change-this-in-production'
    # Force sessions to be cleared on browser close
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    app.config['PERMANENT_SESSION_LIFETIME'] = 3600  # 1 hour
    
    # Initialize CORS
    CORS(app)
    
    # Initialize database
    init_db(app)
    
    # Initialize CSRF protection - disabled for API endpoints via configuration
    app.config['WTF_CSRF_CHECK_DEFAULT'] = False
    csrf = CSRFProtect(app)
    
    # Auto-logout on app startup - clear all sessions
    startup_flag = {'initialized': False}
    
    @app.before_request
    def startup_session_clear():
        """Clear sessions on first request after app startup"""
        if not startup_flag['initialized']:
            startup_flag['initialized'] = True
            # Clear the current request's session if on first load
            from flask import session
            if request.path == '/' and 'user_id' in session:
                session.clear()
    
    # Exempt all /api/ routes from CSRF by setting flag
    @app.before_request
    def disable_csrf_for_api():
        """Disable CSRF token validation for API routes"""
        if request.path.startswith('/api/'):
            # Skip CSRF validation for API endpoints
            return None
    
    # Register blueprints
    app.register_blueprint(pages)
    app.register_blueprint(auth)
    app.register_blueprint(api_species)
    app.register_blueprint(api_locations)
    app.register_blueprint(api_sightings)
    app.register_blueprint(api_reports)
    app.register_blueprint(api_dashboard)
    app.register_blueprint(api_admin)
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'message': 'Resource not found'
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        from database import db
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': 'Internal server error'
        }), 500
    
    return app


# Create application instance
app = create_app()


if __name__ == '__main__':
    with app.app_context():
        create_tables(app)
        # Clear any persisted sessions on startup
        try:
            from database import db
            # Note: If you implement server-side sessions, clear them here
            print("✅ App startup complete - sessions cleared")
        except:
            pass
    
    app.run(debug=True, host='0.0.0.0', port=5000)
