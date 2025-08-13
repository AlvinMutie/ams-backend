#!/usr/bin/env python3
"""
Simple test script to verify Flask backend functionality
"""

import requests
import json

BASE_URL = "http://localhost:5000"

def test_frontend_routes():
    """Test all frontend routes"""
    print("Testing Frontend Routes...")
    
    routes = [
        "/",
        "/login", 
        "/register",
        "/student",
        "/supervisor",
        "/industry",
        "/admin"
    ]
    
    for route in routes:
        try:
            response = requests.get(f"{BASE_URL}{route}")
            print(f"✓ {route}: {response.status_code}")
        except requests.exceptions.ConnectionError:
            print(f"✗ {route}: Connection failed (Flask not running)")
        except Exception as e:
            print(f"✗ {route}: Error - {e}")

def test_api_routes():
    """Test API endpoints"""
    print("\nTesting API Routes...")
    
    # Test registration
    test_user = {
        "name": "Test User",
        "email": "test@example.com", 
        "password": "testpass123",
        "role": "student"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/register", json=test_user)
        print(f"✓ /api/register: {response.status_code}")
        if response.status_code == 201:
            print(f"  Response: {response.json()}")
    except Exception as e:
        print(f"✗ /api/register: Error - {e}")
    
    # Test login
    login_data = {
        "email": "john@student.com",
        "password": "password123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/login", json=login_data)
        print(f"✓ /api/login: {response.status_code}")
        if response.status_code == 200:
            print(f"  Response: {response.json()}")
    except Exception as e:
        print(f"✗ /api/login: Error - {e}")
    
    # Test other API endpoints
    api_routes = [
        "/api/slots",
        "/api/reports",
        "/api/admin-view"
    ]
    
    for route in api_routes:
        try:
            response = requests.get(f"{BASE_URL}{route}")
            print(f"✓ {route}: {response.status_code}")
        except Exception as e:
            print(f"✗ {route}: Error - {e}")

def test_static_files():
    """Test if static files are accessible"""
    print("\nTesting Static Files...")
    
    static_files = [
        "/static/css/theme-styles.css",
        "/static/css/dashboard-styles.css",
        "/static/css/login-styles.css",
        "/static/js/theme-utils.js"
    ]
    
    for file_path in static_files:
        try:
            response = requests.get(f"{BASE_URL}{file_path}")
            print(f"✓ {file_path}: {response.status_code}")
        except Exception as e:
            print(f"✗ {file_path}: Error - {e}")

if __name__ == "__main__":
    print("Flask Backend Test Suite")
    print("=" * 40)
    
    test_frontend_routes()
    test_api_routes()
    test_static_files()
    
    print("\nTest completed!")
    print("\nTo run the Flask app:")
    print("1. Activate virtual environment: venv\\Scripts\\activate")
    print("2. Run: python app.py")
    print("3. Open browser to: http://localhost:5000")
