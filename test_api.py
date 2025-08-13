#!/usr/bin/env python3
"""
Test script for the Attachment Management System API
Run this after starting the Flask server to test all endpoints
"""

import requests
import json

# Base URL for the API
BASE_URL = "http://localhost:5000"

def test_home():
    """Test the home endpoint"""
    print("Testing / endpoint...")
    response = requests.get(BASE_URL)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
    print("-" * 50)

def test_register():
    """Test user registration"""
    print("Testing /register endpoint...")
    
    # Test student registration
    student_data = {
        "name": "Test Student",
        "email": "teststudent@example.com",
        "password": "password123",
        "role": "student"
    }
    
    response = requests.post(f"{BASE_URL}/register", json=student_data)
    print(f"Student Registration - Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # Test supervisor registration
    supervisor_data = {
        "name": "Test Supervisor",
        "email": "testsupervisor@example.com",
        "password": "password123",
        "role": "industry_supervisor"
    }
    
    response = requests.post(f"{BASE_URL}/register", json=supervisor_data)
    print(f"Supervisor Registration - Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print("-" * 50)

def test_login():
    """Test user login"""
    print("Testing /login endpoint...")
    
    # Test student login
    student_login = {
        "email": "john@student.com",
        "password": "password123"
    }
    
    response = requests.post(f"{BASE_URL}/login", json=student_login)
    print(f"Student Login - Status: {response.status_code}")
    if response.status_code == 200:
        student_data = response.json()
        print(f"Student ID: {student_data['user_id']}")
        print(f"Student Role: {student_data['role']}")
        print(f"Session Token: {student_data['session_token'][:20]}...")
    
    # Test admin login
    admin_login = {
        "email": "admin@example.com",
        "password": "password123"
    }
    
    response = requests.post(f"{BASE_URL}/login", json=admin_login)
    print(f"Admin Login - Status: {response.status_code}")
    if response.status_code == 200:
        admin_data = response.json()
        print(f"Admin ID: {admin_data['user_id']}")
        print(f"Admin Role: {admin_data['role']}")
        print(f"Session Token: {admin_data['session_token'][:20]}...")
    
    print("-" * 50)

def test_slots():
    """Test getting available slots"""
    print("Testing /slots endpoint...")
    response = requests.get(f"{BASE_URL}/slots")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        slots_data = response.json()
        print(f"Total Available Slots: {slots_data['total']}")
        for slot in slots_data['slots']:
            print(f"  Slot {slot['id']}: {slot['date']} (Capacity: {slot['capacity']}, Booked: {slot['booked_count']})")
    print("-" * 50)

def test_book_slot():
    """Test booking a slot"""
    print("Testing /book endpoint...")
    
    # First, get a student user ID
    login_response = requests.post(f"{BASE_URL}/login", json={
        "email": "jane@student.com",
        "password": "password123"
    })
    
    if login_response.status_code == 200:
        student_id = login_response.json()['user_id']
        
        # Book slot 4
        booking_data = {
            "user_id": student_id,
            "slot_id": 4
        }
        
        response = requests.post(f"{BASE_URL}/book", json=booking_data)
        print(f"Booking Status: {response.status_code}")
        if response.status_code == 201:
            booking_info = response.json()
            print(f"Booking ID: {booking_info['booking_id']}")
            print(f"Slot ID: {booking_info['slot_id']}")
            print(f"Date: {booking_info['date']}")
        else:
            print(f"Error: {response.json()}")
    else:
        print("Could not login to test booking")
    
    print("-" * 50)

def test_attendance():
    """Test marking attendance"""
    print("Testing /attendance endpoint...")
    
    # Mark attendance for John Doe (student ID 1)
    attendance_data = {
        "student_id": 1,
        "date": "2024-01-20"
    }
    
    response = requests.post(f"{BASE_URL}/attendance", json=attendance_data)
    print(f"Attendance Status: {response.status_code}")
    if response.status_code == 201:
        attendance_info = response.json()
        print(f"Attendance ID: {attendance_info['attendance_id']}")
        print(f"Student: {attendance_info['student_name']}")
        print(f"Date: {attendance_info['date']}")
        print(f"Status: {attendance_info['status']}")
    else:
        print(f"Error: {response.json()}")
    
    print("-" * 50)

def test_reports():
    """Test getting reports"""
    print("Testing /reports endpoint...")
    response = requests.get(f"{BASE_URL}/reports")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        reports_data = response.json()
        summary = reports_data['summary']
        print(f"Summary:")
        print(f"  Total Users: {summary['total_users']}")
        print(f"  Total Slots: {summary['total_slots']}")
        print(f"  Total Bookings: {summary['total_bookings']}")
        print(f"  Total Attendance: {summary['total_attendance']}")
        print(f"  Students: {summary['students']}")
        print(f"  Supervisors: {summary['supervisors']}")
        
        print(f"\nRecent Bookings:")
        for booking in reports_data['recent_bookings']:
            print(f"  {booking['user_name']} -> Slot {booking['slot_id']} ({booking['slot_date']})")
        
        print(f"\nRecent Attendance:")
        for attendance in reports_data['recent_attendance']:
            print(f"  {attendance['student_name']} - {attendance['date']} ({attendance['status']})")
    
    print("-" * 50)

def test_admin_view():
    """Test admin view access"""
    print("Testing /admin-view endpoint...")
    
    # Test without email parameter (should fail)
    response = requests.get(f"{BASE_URL}/admin-view")
    print(f"Without email - Status: {response.status_code}")
    print(f"Response: {response.text[:100]}...")
    
    # Test with wrong email (should fail)
    response = requests.get(f"{BASE_URL}/admin-view?email=wrong@email.com")
    print(f"Wrong email - Status: {response.status_code}")
    print(f"Response: {response.text[:100]}...")
    
    # Test with correct email (should succeed)
    response = requests.get(f"{BASE_URL}/admin-view?email=admin@example.com")
    print(f"Correct email - Status: {response.status_code}")
    if response.status_code == 200:
        print("Admin view loaded successfully!")
        print(f"Response length: {len(response.text)} characters")
    else:
        print(f"Error: {response.text}")
    
    print("-" * 50)

def main():
    """Run all tests"""
    print("=" * 60)
    print("ATTACHMENT MANAGEMENT SYSTEM - API TESTING")
    print("=" * 60)
    
    try:
        test_home()
        test_register()
        test_login()
        test_slots()
        test_book_slot()
        test_attendance()
        test_reports()
        test_admin_view()
        
        print("\n" + "=" * 60)
        print("ALL TESTS COMPLETED!")
        print("=" * 60)
        
    except requests.exceptions.ConnectionError:
        print("ERROR: Could not connect to the server!")
        print("Make sure the Flask server is running on http://localhost:5000")
        print("Run: python app.py")
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    main()
