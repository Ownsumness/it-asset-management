# app.py

from flask import Flask, render_template
import os
from config import get_config
from database import init_db, close_db
from auth import auth_bp
from assets import assets_bp
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def create_app(config_class=None):
    """
    Application factory function.
    Creates and configures the Flask application.
    """
    app = Flask(__name__)
    
    # Load configuration
    if config_class is None:
        config_class = get_config()
    
    app.config.from_object(config_class)
    
    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(assets_bp)
    
    # Database teardown
    app.teardown_appcontext(close_db)
    
    # Error handlers
    @app.errorhandler(404)
    def page_not_found(e):
        """Render custom 404 error page."""
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_error(e):
        """Render custom 500 error page."""
        logger.error(f"Internal server error: {e}")
        return render_template('500.html'), 500
    
    # Health check endpoint
    @app.route('/health')
    def health_check():
        """Health check endpoint for monitoring and load balancers."""
        return {'status': 'healthy', 'app': 'it-asset-management'}, 200
    
    logger.info(f"Application created with config: {config_class.__class__.__name__}")
    
    return app


# Create the application instance
app = create_app()


if __name__ == '__main__':
    # Check if the database exists; if not, initialize it
    db_path = app.config.get('DATABASE_PATH', 'assets.db')
    if not os.path.exists(db_path):
        with app.app_context():
            init_db()
            logger.info("Database initialized")
    
    # Run in development mode
    app.run(debug=app.config.get('DEBUG', False))
