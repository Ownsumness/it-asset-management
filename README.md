# IT Asset Management System

A web-based IT asset management application built with Flask, enabling organizations to track, manage, and audit their IT assets efficiently.

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Flask](https://img.shields.io/badge/Flask-3.0.3-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## Features

- **User Authentication** - Secure login/registration with role-based access (admin/regular)
- **Asset Management** - Full CRUD operations for IT assets
- **Dashboard** - Overview of all assets with filtering capabilities
- **Role-Based Access** - Admins can delete assets; regular users can add/edit

## Tech Stack

- **Backend**: Flask 3.0.3
- **Database**: SQLite
- **Authentication**: Werkzeug password hashing
- **Deployment**: Render (with Gunicorn)
- **CI/CD**: GitHub Actions

## Quick Start

### Prerequisites
- Python 3.12+
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/Ownsumness/it-asset-management.git
cd it-asset-management

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Running Locally

```bash
# Set environment variables (optional for development)
set FLASK_ENV=development    # Windows
export FLASK_ENV=development # Linux/Mac

# Run the application
python app.py
```

Visit `http://127.0.0.1:5000` in your browser.

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=. --cov-report=html
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `FLASK_ENV` | Environment mode (`development`, `production`, `testing`) | `development` |
| `SECRET_KEY` | Flask secret key for sessions | Random (dev only) |
| `DATABASE_PATH` | Path to SQLite database file | `assets.db` |

> **⚠️ Important**: In production, always set `SECRET_KEY` as an environment variable!

## API Routes

| Route | Method | Description | Auth Required |
|-------|--------|-------------|---------------|
| `/` | GET | Redirect to login | No |
| `/login` | GET, POST | User login | No |
| `/register` | GET, POST | User registration | No |
| `/logout` | GET | User logout | Yes |
| `/dashboard` | GET | Asset dashboard | Yes |
| `/add_asset` | GET, POST | Add new asset | Yes |
| `/edit_asset/<id>` | GET, POST | Edit existing asset | Yes |
| `/delete_asset/<id>` | POST | Delete asset | Admin only |
| `/health` | GET | Health check endpoint | No |

## Project Structure

```
it-asset-management/
├── .github/
│   └── workflows/
│       └── ci.yml          # CI/CD pipeline
├── static/
│   └── styles.css          # Stylesheets
├── templates/
│   ├── base.html           # Base template
│   ├── login.html          # Login page
│   ├── register.html       # Registration page
│   ├── dashboard.html      # Asset dashboard
│   ├── add_asset.html      # Add asset form
│   ├── edit_asset.html     # Edit asset form
│   ├── 404.html            # 404 error page
│   └── 500.html            # 500 error page
├── tests/
│   ├── conftest.py         # Test fixtures
│   └── test_app.py         # Application tests
├── app.py                  # Application entry point
├── config.py               # Configuration module
├── database.py             # Database operations
├── auth.py                 # Authentication blueprint
├── assets.py               # Assets blueprint
├── schema.sql              # Database schema
├── requirements.txt        # Python dependencies
├── Procfile                # Render deployment
└── README.md               # This file
```

## Deployment

### Render

The application is configured for Render deployment:

1. Connect your GitHub repository to Render
2. Set environment variables in Render dashboard:
   - `SECRET_KEY`: A secure random string
   - `FLASK_ENV`: `production`
3. Deploy!

### Environment Setup for Production

```bash
# Generate a secure secret key
python -c "import secrets; print(secrets.token_hex(32))"
```

## Development

### Code Quality

```bash
# Run linting
flake8 . --max-line-length=127 --exclude=venv

# Format code (optional - install black first)
black . --exclude venv
```

### Adding New Features

1. Create a feature branch
2. Write tests first (TDD encouraged)
3. Implement the feature
4. Run tests and linting
5. Create a pull request

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Flask documentation
- DevOps best practices following CALMS framework
