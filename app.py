"""
EcoTrack Application
Main Flask application with modular blueprint architecture
"""

from flask import Flask, jsonify
from flask_cors import CORS
from database import init_db, create_tables

# Import blueprints
from routes.pages import pages
from routes.auth import auth
from routes.api_species import api_species
from routes.api_locations import api_locations
from routes.api_sightings import api_sightings
from routes.api_reports import api_reports
from routes.api_dashboard import api_dashboard
from routes.api_admin import api_admin


def create_app():
    """Application factory function"""
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = 'your-secret-key-change-this-in-production'
    
    # Initialize CORS
    CORS(app)
    
    # Initialize database
    init_db(app)
    
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
    
    app.run(debug=True, host='0.0.0.0', port=5000)
