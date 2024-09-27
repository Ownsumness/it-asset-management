# assets.py

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from database import get_db
import datetime

assets_bp = Blueprint('assets', __name__)

@assets_bp.route('/')
def home():
    """
    Redirect to the login page.
    """
    return redirect(url_for('auth.login'))

@assets_bp.route('/dashboard')
def dashboard():
    """
    Display the asset dashboard.
    """
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    db = get_db()
    assets = db.execute(
        'SELECT * FROM assets'
    ).fetchall()

    return render_template('dashboard.html', assets=assets, role=session.get('role'))

@assets_bp.route('/add_asset', methods=['GET', 'POST'])
def add_asset():
    """
    Allow users to add a new asset.
    - GET: Render the add asset form.
    - POST: Validate input and add the asset to the database.
    """
    if 'user_id' not in session:
        flash('Permission denied.', 'danger')
        return redirect(url_for('assets.dashboard'))

    if request.method == 'POST':
        name = request.form['name']
        category = request.form['category']
        purchase_date = request.form['purchase_date']
        status = request.form['status']
        location = request.form['location']
        user_id = session['user_id']

        # Basic validation
        error = None
        if not name or not category or not purchase_date or not status or not location:
            error = 'All fields are required.'
        else:
            # Validate date
            try:
                purchase_date_obj = datetime.datetime.strptime(purchase_date, '%Y-%m-%d').date()
                if purchase_date_obj > datetime.date.today():
                    error = 'Purchase date cannot be in the future.'
            except ValueError:
                error = 'Invalid date format. Use YYYY-MM-DD.'

        if error:
            flash(error, 'danger')
            return render_template('add_asset.html', error=error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO assets (name, category, purchase_date, status, location, user_id) VALUES (?, ?, ?, ?, ?, ?)',
                (name, category, purchase_date, status, location, user_id)
            )
            db.commit()
            flash('Asset added successfully!', 'success')
            return redirect(url_for('assets.dashboard'))

    return render_template('add_asset.html')

@assets_bp.route('/edit_asset/<int:asset_id>', methods=['GET', 'POST'])
def edit_asset(asset_id):
    """
    Allow users to edit an existing asset.
    - GET: Render the edit asset form with current asset data.
    - POST: Validate input and update the asset in the database.
    """
    if 'user_id' not in session:
        flash('Please log in to continue.', 'danger')
        return redirect(url_for('auth.login'))

    db = get_db()
    asset = db.execute('SELECT * FROM assets WHERE asset_id = ?', (asset_id,)).fetchone()

    if asset is None:
        flash('Asset not found.', 'danger')
        return redirect(url_for('assets.dashboard'))

    if request.method == 'POST':
        name = request.form['name']
        category = request.form['category']
        purchase_date = request.form['purchase_date']
        status = request.form['status']
        location = request.form['location']

        # Basic validation
        error = None
        if not name or not category or not purchase_date or not status or not location:
            error = 'All fields are required.'
        else:
            # Validate date
            try:
                purchase_date_obj = datetime.datetime.strptime(purchase_date, '%Y-%m-%d').date()
                if purchase_date_obj > datetime.date.today():
                    error = 'Purchase date cannot be in the future.'
            except ValueError:
                error = 'Invalid date format. Use YYYY-MM-DD.'

        if error:
            flash(error, 'danger')
            return render_template('edit_asset.html', asset=asset, error=error)
        else:
            db.execute(
                'UPDATE assets SET name = ?, category = ?, purchase_date = ?, status = ?, location = ? WHERE asset_id = ?',
                (name, category, purchase_date, status, location, asset_id)
            )
            db.commit()
            flash('Asset updated successfully!', 'success')
            return redirect(url_for('assets.dashboard'))

    return render_template('edit_asset.html', asset=asset)

@assets_bp.route('/delete_asset/<int:asset_id>', methods=['POST'])
def delete_asset(asset_id):
    """
    Allow admin users to delete an asset.
    """
    if 'user_id' not in session or session.get('role') != 'admin':
        flash('Permission denied.', 'danger')
        return redirect(url_for('assets.dashboard'))

    db = get_db()
    db.execute('DELETE FROM assets WHERE asset_id = ?', (asset_id,))
    db.commit()
    flash('Asset deleted successfully!', 'success')
    return redirect(url_for('assets.dashboard'))
