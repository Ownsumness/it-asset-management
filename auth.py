# auth.py

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from database import get_db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handle user registration.
    - GET: Render the registration template.
    - POST: Validate input and register the user.
    """
    if request.method == 'POST':
        # Get form data
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        role = request.form['role']

        # Basic validation
        error = None
        if not username or not password or not confirm_password or not role:
            error = 'All fields are required.'
        elif len(username) < 4 or len(username) > 25:
            error = 'Username must be between 4 and 25 characters.'
        elif password != confirm_password:
            error = 'Passwords do not match.'
        elif len(password) < 6:
            error = 'Password must be at least 6 characters long.'

        if error:
            flash(error, 'danger')
        else:
            # Hash the password
            hashed_password = generate_password_hash(password)
            # Interact with the database
            db = get_db()
            try:
                db.execute('INSERT INTO users (username, password, role) VALUES (?, ?, ?)',
                           (username, hashed_password, role))
                db.commit()
                flash('Registration successful! Please log in.', 'success')
                return redirect(url_for('auth.login'))
            except db.IntegrityError:
                flash('Username already exists.', 'danger')
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle user login.
    - GET: Render the login template.
    - POST: Validate credentials and log the user in.
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db = get_db()
        user = db.execute(
            'SELECT * FROM users WHERE username = ?',
            (username,)
        ).fetchone()

        if user and check_password_hash(user['password'], password):
            session.clear()
            session['user_id'] = user['id']
            session['role'] = user['role']
            session['username'] = user['username']
            flash('Login successful!', 'success')
            return redirect(url_for('assets.dashboard'))
        else:
            flash('Invalid username or password.', 'danger')
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    """
    Log the user out by clearing the session.
    """
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))
