# database.py

import sqlite3
from flask import g, current_app
from werkzeug.security import generate_password_hash

def get_db():
    """
    Get a database connection for the current application context.
    If none exists, create a new connection.
    """
    if 'db' not in g:
        g.db = sqlite3.connect('assets.db')
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    """
    Close the database connection if it exists.
    Called automatically when the application context ends.
    """
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    """
    Initialize the database by executing the schema.sql script.
    Inserts sample data into the database.
    """
    db = get_db()
    with current_app.open_resource('schema.sql', mode='r') as f:
        db.executescript(f.read())

    # Insert sample users with hashed passwords
    users = [
        ('admin1', generate_password_hash('password1'), 'admin'),
        ('admin2', generate_password_hash('password2'), 'admin'),
        ('user1', generate_password_hash('password3'), 'regular'),
        ('user2', generate_password_hash('password4'), 'regular'),
        ('user3', generate_password_hash('password5'), 'regular'),
        ('user4', generate_password_hash('password6'), 'regular'),
        ('user5', generate_password_hash('password7'), 'regular'),
        ('user6', generate_password_hash('password8'), 'regular'),
        ('user7', generate_password_hash('password9'), 'regular'),
        ('user8', generate_password_hash('password10'), 'regular'),
    ]

    db.executemany('INSERT INTO users (username, password, role) VALUES (?, ?, ?)', users)

    # Insert sample assets
    assets = [
        ('Laptop A', 'Computers', '2024-01-15', 'In Use', 'UK Office', 1),
        ('Printer B', 'Peripherals', '2024-02-20', 'Under Maintenance', 'US Office', 2),
        ('Monitor C', 'Displays', '2024-03-05', 'In Stock', 'US Warehouse', 3),
        ('Keyboard D', 'Accessories', '2024-04-10', 'In Use', 'US Office', 4),
        ('Mouse E', 'Accessories', '2024-05-18', 'In Stock', 'UK Warehouse', 5),
        ('Router F', 'Networking', '2024-06-25', 'In Use', 'UK Office', 6),
        ('Switch G', 'Networking', '2024-07-30', 'In Stock', 'US Warehouse', 7),
        ('Tablet H', 'Mobile Devices', '2024-08-12', 'In Use', 'UK Office', 8),
        ('Smartphone I', 'Mobile Devices', '2023-09-22', 'Lost', 'Unknown', 9),
        ('Server J', 'Servers', '2023-10-01', 'In Use', 'US Data Center', 10),
    ]

    db.executemany('''
        INSERT INTO assets (name, category, purchase_date, status, location, user_id)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', assets)

    db.commit()
