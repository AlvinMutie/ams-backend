from flask import Flask, request, jsonify, render_template, session, redirect, url_for
from flask_cors import CORS
from database import Database
import hashlib
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-super-secret-key-change-this-in-production'

# Enable CORS
CORS(app)

# Initialize database
db = Database()

# Frontend Routes
@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/login')
def login_page_alt():
    return render_template('login.html')

@app.route('/register')
def register_page():
    return render_template('register.html')

@app.route('/student')
def student_dashboard():
    return render_template('dashboard.html')

@app.route('/supervisor')
def university_supervisor_dashboard():
    return render_template('dashboard.html')

@app.route('/industry')
def industrial_supervisor_dashboard():
    return render_template('dashboard.html')

@app.route('/admin')
def coordinator_dashboard():
    return render_template('dashboard.html')

# API Routes
@app.route('/api/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        role = data.get('role')
        
        if not all([name, email, password, role]):
            return jsonify({'error': 'All fields are required'}), 400
        
        # Hash the password
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        # Create user
        user_id = db.create_user(name, email, hashed_password, role)
        
        return jsonify({
            'message': 'User registered successfully',
            'user_id': user_id
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if not all([email, password]):
            return jsonify({'error': 'Email and password are required'}), 400
        
        # Hash the password
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        # Get user
        user = db.get_user_by_email(email)
        
        if not user:
            return jsonify({'error': 'Invalid credentials'}), 401
        
        # Check password
        if user['password'] != hashed_password:
            return jsonify({'error': 'Invalid credentials'}), 401
        
        # Set session
        session['user_id'] = user['id']
        session['user_email'] = user['email']
        session['user_role'] = user['role']
        
        return jsonify({
            'message': 'Login successful',
            'user': {
                'id': user['id'],
                'name': user['name'],
                'email': user['email'],
                'role': user['role']
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/slots', methods=['GET'])
def get_slots():
    try:
        slots = db.get_available_slots()
        return jsonify(slots), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/book', methods=['POST'])
def book_slot():
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        slot_id = data.get('slot_id')
        
        if not all([user_id, slot_id]):
            return jsonify({'error': 'User ID and slot ID are required'}), 400
        
        # Check if slot is available
        slot = db.get_slot_by_id(slot_id)
        if not slot:
            return jsonify({'error': 'Slot not found'}), 404
        
        if slot['booked_count'] >= slot['max_capacity']:
            return jsonify({'error': 'Slot is full'}), 400
        
        # Book the slot
        booking_id = db.create_booking(user_id, slot_id)
        
        return jsonify({
            'message': 'Slot booked successfully',
            'booking_id': booking_id
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/attendance', methods=['POST'])
def mark_attendance():
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        slot_id = data.get('slot_id')
        date = data.get('date')
        status = data.get('status', 'present')
        
        if not all([user_id, slot_id, date]):
            return jsonify({'error': 'User ID, slot ID, and date are required'}), 400
        
        # Mark attendance
        attendance_id = db.mark_attendance(user_id, slot_id, date, status)
        
        return jsonify({
            'message': 'Attendance marked successfully',
            'attendance_id': attendance_id
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/reports', methods=['GET'])
def get_reports():
    try:
        reports = db.get_reports()
        return jsonify(reports), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/test-db')
def test_database():
    try:
        users = db.get_all_users()
        return jsonify({
            'message': 'Database test successful',
            'total_users': len(users),
            'users': users
        }), 200
    except Exception as e:
        return jsonify({'error': f'Database test failed: {str(e)}'}), 500

@app.route('/admin-view')
def admin_view():
    email = request.args.get('email')
    if email != 'admin@example.com':
        return "Access denied", 403
    
    try:
        users = db.get_all_users()
        slots = db.get_all_slots()
        bookings = db.get_all_bookings()
        attendance = db.get_all_attendance()
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Database Admin View</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                table {{ border-collapse: collapse; width: 100%; margin-bottom: 30px; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
                h2 {{ color: #333; }}
            </style>
        </head>
        <body>
            <h1>Database Admin View</h1>
            
            <h2>Users ({len(users)} total)</h2>
            <table>
                <tr><th>ID</th><th>Name</th><th>Email</th><th>Role</th><th>Created</th></tr>
                {''.join([f'<tr><td>{u["id"]}</td><td>{u["name"]}</td><td>{u["email"]}</td><td>{u["role"]}</td><td>{u["created_at"]}</td></tr>' for u in users])}
            </table>
            
            <h2>Slots ({len(slots)} total)</h2>
            <table>
                <tr><th>ID</th><th>Name</th><th>Date</th><th>Time</th><th>Max Capacity</th><th>Booked Count</th></tr>
                {''.join([f'<tr><td>{s["id"]}</td><td>{s["name"]}</td><td>{s["date"]}</td><td>{s["time"]}</td><td>{s["max_capacity"]}</td><td>{s["booked_count"]}</td></tr>' for s in slots])}
            </table>
            
            <h2>Bookings ({len(bookings)} total)</h2>
            <table>
                <tr><th>ID</th><th>User ID</th><th>Slot ID</th><th>Booked At</th></tr>
                {''.join([f'<tr><td>{b["id"]}</td><td>{b["user_id"]}</td><td>{b["slot_id"]}</td><td>{b["booked_at"]}</td></tr>' for b in bookings])}
            </table>
            
            <h2>Attendance ({len(attendance)} total)</h2>
            <table>
                <tr><th>ID</th><th>User ID</th><th>Slot ID</th><th>Date</th><th>Status</th></tr>
                {''.join([f'<tr><td>{a["id"]}</td><td>{a["user_id"]}</td><td>{a["slot_id"]}</td><td>{a["date"]}</td><td>{a["status"]}</td></tr>' for a in attendance])}
            </table>
        </body>
        </html>
        """
        
        return html
        
    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == '__main__':
    db.initialize_database()
    app.run(debug=True, host='0.0.0.0')
