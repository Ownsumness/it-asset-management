# app.py

from flask import Flask, render_template
import os
from database import init_db, close_db
from auth import auth_bp
from assets import assets_bp

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

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
    return render_template('500.html'), 500

if __name__ == '__main__':
    # Check if the database exists; if not, initialize it
    if not os.path.exists('assets.db'):
        with app.app_context():
            init_db()
    # app.run(debug=False)
    pass
