# tests/test_app.py
"""
Basic tests for IT Asset Management application.
"""

import pytest


class TestHealthCheck:
    """Test health check endpoint."""
    
    def test_health_endpoint_returns_200(self, client):
        """Health check should return 200 OK."""
        response = client.get('/health')
        assert response.status_code == 200
    
    def test_health_endpoint_returns_json(self, client):
        """Health check should return JSON with status."""
        response = client.get('/health')
        data = response.get_json()
        assert data['status'] == 'healthy'
        assert 'app' in data


class TestRoutes:
    """Test basic route accessibility."""
    
    def test_home_redirects_to_login(self, client):
        """Home route should redirect to login."""
        response = client.get('/')
        assert response.status_code == 302
        assert '/login' in response.location
    
    def test_login_page_accessible(self, client):
        """Login page should be accessible."""
        response = client.get('/login')
        assert response.status_code == 200
    
    def test_register_page_accessible(self, client):
        """Register page should be accessible."""
        response = client.get('/register')
        assert response.status_code == 200


class TestErrorHandlers:
    """Test error handlers."""
    
    def test_404_handler(self, client):
        """Non-existent route should return 404."""
        response = client.get('/nonexistent-page')
        assert response.status_code == 404
