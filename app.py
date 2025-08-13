from flask import Flask, request, jsonify, render_template, render_template_string
from flask_cors import CORS
import sqlite3
import hashlib
import datetime
from database import Database

app = Flask(__name__)
CORS(app)

db = Database()

# Frontend Routes
@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        # Handle form submission (this will be handled by JavaScript)
        return render_template('login.html')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    if request.method == 'POST':
        # Handle form submission (this will be handled by JavaScript)
        return render_template('register.html')
    return render_template('register.html')

@app.route('/student')
def student_dashboard():
    return render_template('dashboard.html')

@app.route('/student/logbook')
def student_logbook():
    return render_template('logbook.html')

@app.route('/student/final-report')
def student_final_report():
    return render_template('final_report.html')

@app.route('/student/deferral-request')
def student_deferral_request():
    return render_template('deferral_request.html')

@app.route('/student/download-logbook')
def student_download_logbook():
    return render_template('download_logbook.html')

@app.route('/student/return-form')
def student_return_form():
    return render_template('return_form.html')

@app.route('/student/placement-details')
def student_placement_details():
    return render_template('placement_details.html')

@app.route('/student/analytics')
def student_analytics():
    return render_template('analytics.html')

@app.route('/student/analytics-dashboard')
def student_analytics_dashboard():
    return render_template('analytics-dashboard.html')

@app.route('/supervisor')
def university_supervisor_dashboard():
    return render_template('dashboard.html')

@app.route('/supervisor/assessment-forms')
def university_supervisor_assessment_forms():
    return render_template('assessment_forms.html')

@app.route('/supervisor/logbook-approval')
def university_supervisor_logbook_approval():
    return render_template('logbook_approval.html')

@app.route('/supervisor/approve-logbook')
def university_supervisor_approve_logbook():
    return render_template('approve_logbook.html')

@app.route('/industry')
def industrial_supervisor_dashboard():
    return render_template('dashboard.html')

@app.route('/industry/assessment-form')
def industrial_supervisor_assessment_form():
    return render_template('assessment_form.html')

@app.route('/industry/confirm-logbook')
def industrial_supervisor_confirm_logbook():
    return render_template('confirm_logbook.html')

@app.route('/industry/analytics-dashboard')
def industrial_supervisor_analytics_dashboard():
    return render_template('analytics-dashboard.html')

@app.route('/admin')
def coordinator_dashboard():
    return render_template('dashboard.html')

@app.route('/admin/student-progress')
def coordinator_student_progress():
    return render_template('student_progress.html')

@app.route('/admin/assessment-management')
def coordinator_assessment_management():
    return render_template('assessment_management.html')

@app.route('/admin/assign-clusters')
def coordinator_assign_clusters():
    return render_template('assign_clusters.html')

@app.route('/admin/assign-supervisors')
def coordinator_assign_supervisors():
    return render_template('assign_supervisors.html')

@app.route('/admin/approve-supervisors')
def coordinator_approve_supervisors():
    return render_template('approve_supervisors.html')

@app.route('/admin/communication')
def coordinator_communication():
    return render_template('communication.html')

@app.route('/admin/compile-report')
def coordinator_compile_report():
    return render_template('compile_report.html')

@app.route('/admin/reporting-system')
def coordinator_reporting_system():
    return render_template('reporting-system.html')

# API Routes (keep all existing functionality)
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
        
        if role not in ['student', 'industry_supervisor', 'school_supervisor', 'admin']:
            return jsonify({'error': 'Invalid role'}), 400
        
        # Hash password
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
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
        
        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400
        
        # Hash password for comparison
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        user = db.get_user_by_email(email)
        
        if not user or user['password'] != hashed_password:
            return jsonify({'error': 'Invalid credentials'}), 401
        
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
        return jsonify({'slots': slots}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/book', methods=['POST'])
def book_slot():
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        slot_id = data.get('slot_id')
        
        if not user_id or not slot_id:
            return jsonify({'error': 'User ID and slot ID are required'}), 400
        
        # Check if slot is available
        slot = db.get_slot_by_id(slot_id)
        if not slot:
            return jsonify({'error': 'Slot not found'}), 404
        
        if slot['booked_count'] >= slot['max_capacity']:
            return jsonify({'error': 'Slot is full'}), 409
        
        # Create booking
        booking_id = db.create_booking(user_id, slot_id)
        
        # Update slot booked count
        db.update_slot_booked_count(slot_id)
        
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
        status = data.get('status')  # 'present', 'absent', 'late'
        
        if not all([user_id, slot_id, status]):
            return jsonify({'error': 'User ID, slot ID, and status are required'}), 400
        
        if status not in ['present', 'absent', 'late']:
            return jsonify({'error': 'Invalid status'}), 400
        
        # Get current date
        current_date = datetime.datetime.now().strftime('%Y-%m-%d')
        
        attendance_id = db.create_attendance(user_id, slot_id, current_date, status)
        
        return jsonify({
            'message': 'Attendance marked successfully',
            'attendance_id': attendance_id
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/reports', methods=['GET'])
def get_reports():
    try:
        # Get various statistics
        total_users = db.get_total_users()
        total_slots = db.get_total_slots()
        total_bookings = db.get_total_bookings()
        total_attendance = db.get_total_attendance()
        
        # Get recent data
        recent_bookings = db.get_recent_bookings(5)
        recent_attendance = db.get_recent_attendance(5)
        
        report = {
            'summary': {
                'total_users': total_users,
                'total_slots': total_slots,
                'total_bookings': total_bookings,
                'total_attendance': total_attendance
            },
            'recent_bookings': recent_bookings,
            'recent_attendance': recent_attendance
        }
        
        return jsonify(report), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin-view')
def admin_view():
    try:
        # Get all data for admin view
        users = db.get_all_users()
        slots = db.get_all_slots()
        bookings = db.get_all_bookings()
        attendance = db.get_all_attendance()
        
        # Create HTML table view
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>AMS Admin View</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                table {{ border-collapse: collapse; width: 100%; margin-bottom: 20px; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
                h1, h2 {{ color: #333; }}
            </style>
        </head>
        <body>
            <h1>Attachment Management System - Admin View</h1>
            
            <h2>Users ({len(users)})</h2>
            <table>
                <tr><th>ID</th><th>Name</th><th>Email</th><th>Role</th><th>Created</th></tr>
                {''.join([f'<tr><td>{u["id"]}</td><td>{u["name"]}</td><td>{u["email"]}</td><td>{u["role"]}</td><td>{u["created_at"]}</td></tr>' for u in users])}
            </table>
            
            <h2>Slots ({len(slots)})</h2>
            <table>
                <tr><th>ID</th><th>Name</th><th>Date</th><th>Time</th><th>Capacity</th><th>Booked</th></tr>
                {''.join([f'<tr><td>{s["id"]}</td><td>{s["name"]}</td><td>{s["date"]}</td><td>{s["time"]}</td><td>{s["max_capacity"]}</td><td>{s["booked_count"]}</td></tr>' for s in slots])}
            </table>
            
            <h2>Bookings ({len(bookings)})</h2>
            <table>
                <tr><th>ID</th><th>User ID</th><th>Slot ID</th><th>Booked At</th></tr>
                {''.join([f'<tr><td>{b["id"]}</td><td>{b["user_id"]}</td><td>{b["slot_id"]}</td><td>{b["booked_at"]}</td></tr>' for b in bookings])}
            </table>
            
            <h2>Attendance ({len(attendance)})</h2>
            <table>
                <tr><th>ID</th><th>User ID</th><th>Slot ID</th><th>Date</th><th>Status</th></tr>
                {''.join([f'<tr><td>{a["id"]}</td><td>{a["user_id"]}</td><td>{a["slot_id"]}</td><td>{a["date"]}</td><td>{a["status"]}</td></tr>' for a in attendance])}
            </table>
        </body>
        </html>
        """
        
        return html_content
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    db.create_tables()
    db.add_sample_data()
    app.run(debug=True, host='0.0.0.0', port=5000)
