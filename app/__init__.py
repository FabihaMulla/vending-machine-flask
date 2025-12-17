"""
Flask Application Initialization
Creates and configures the Flask app with Blueprints
"""

import os
from flask import Flask, render_template
from flask_cors import CORS


def create_app():
    """
    Application factory for Flask app
    Returns configured Flask application instance
    """
    # Get the base directory (parent of app folder)
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    
    # Create Flask app with custom template and static folders
    app = Flask(__name__,
                template_folder=os.path.join(base_dir, 'templates'),
                static_folder=os.path.join(base_dir, 'static'))
    
    # Configuration
    app.config['SECRET_KEY'] = 'vending-machine-secret-key-2025'
    app.config['JSON_SORT_KEYS'] = False
    
    # Enable CORS for API endpoints
    CORS(app)
    
    # Register Blueprints
    from app.routes.vending_routes import vending_bp
    app.register_blueprint(vending_bp)
    
    # Root route - serve the main page
    @app.route('/')
    def index():
        """Serve the main vending machine interface"""
        return render_template('index.html')
    
    # Health check endpoint
    @app.route('/health')
    def health():
        """Health check endpoint"""
        return {'status': 'healthy', 'message': 'Vending Machine API is running'}, 200
    
    return app
