import sqlite3
import hashlib
from datetime import datetime

class Database:
    def __init__(self, db_path='database.db'):
        self.db_path = db_path
        self.initialize_database()
    
    def get_connection(self):
        return sqlite3.connect(self.db_path)
    
    def create_tables(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Slots table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS slots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                date TEXT NOT NULL,
                time TEXT NOT NULL,
                max_capacity INTEGER NOT NULL,
                booked_count INTEGER DEFAULT 0
            )
        ''')
        
        # Bookings table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bookings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                slot_id INTEGER NOT NULL,
                booked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (slot_id) REFERENCES slots (id)
            )
        ''')
        
        # Attendance table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS attendance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                slot_id INTEGER NOT NULL,
                date TEXT NOT NULL,
                status TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (slot_id) REFERENCES slots (id),
                UNIQUE(user_id, slot_id, date)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_sample_data(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Add sample users if they don't exist
        sample_users = [
            ('John Doe', 'john@student.com', hashlib.sha256('password123'.encode()).hexdigest(), 'student'),
            ('Jane Smith', 'jane@supervisor.com', hashlib.sha256('password123'.encode()).hexdigest(), 'school_supervisor'),
            ('Bob Johnson', 'bob@industry.com', hashlib.sha256('password123'.encode()).hexdigest(), 'industry_supervisor'),
            ('Admin User', 'admin@example.com', hashlib.sha256('admin123'.encode()).hexdigest(), 'admin')
        ]
        
        for user in sample_users:
            cursor.execute('''
                INSERT OR IGNORE INTO users (name, email, password, role)
                VALUES (?, ?, ?, ?)
            ''', user)
        
        # Add sample slots if they don't exist
        sample_slots = [
            ('Morning Session', '2025-08-15', '09:00-12:00', 20),
            ('Afternoon Session', '2025-08-15', '14:00-17:00', 15),
            ('Evening Session', '2025-08-16', '18:00-21:00', 10)
        ]
        
        for slot in sample_slots:
            cursor.execute('''
                INSERT OR IGNORE INTO slots (name, date, time, max_capacity)
                VALUES (?, ?, ?, ?)
            ''', slot)
        
        conn.commit()
        conn.close()
    
    def initialize_database(self):
        """Initialize database with tables and sample data"""
        self.create_tables()
        self.add_sample_data()
    
    # User methods
    def create_user(self, name, email, password, role):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO users (name, email, password, role)
            VALUES (?, ?, ?, ?)
        ''', (name, email, password, role))
        
        user_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return user_id
    
    def get_user_by_email(self, email):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        user = cursor.fetchone()
        
        conn.close()
        
        if user:
            return {
                'id': user[0],
                'name': user[1],
                'email': user[2],
                'password': user[3],
                'role': user[4],
                'created_at': user[5]
            }
        return None
    
    def get_all_users(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM users ORDER BY created_at DESC')
        users = cursor.fetchall()
        
        conn.close()
        
        return [
            {
                'id': user[0],
                'name': user[1],
                'email': user[2],
                'password': user[3],
                'role': user[4],
                'created_at': user[5]
            }
            for user in users
        ]
    
    # Slot methods
    def get_available_slots(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM slots 
            WHERE booked_count < max_capacity
            ORDER BY date, time
        ''')
        slots = cursor.fetchall()
        
        conn.close()
        
        return [
            {
                'id': slot[0],
                'name': slot[1],
                'date': slot[2],
                'time': slot[3],
                'max_capacity': slot[4],
                'booked_count': slot[5]
            }
            for slot in slots
        ]
    
    def get_slot_by_id(self, slot_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM slots WHERE id = ?', (slot_id,))
        slot = cursor.fetchone()
        
        conn.close()
        
        if slot:
            return {
                'id': slot[0],
                'name': slot[1],
                'date': slot[2],
                'time': slot[3],
                'max_capacity': slot[4],
                'booked_count': slot[5]
            }
        return None
    
    def get_all_slots(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM slots ORDER BY date, time')
        slots = cursor.fetchall()
        
        conn.close()
        
        return [
            {
                'id': slot[0],
                'name': slot[1],
                'date': slot[2],
                'time': slot[3],
                'max_capacity': slot[4],
                'booked_count': slot[5]
            }
            for slot in slots
        ]
    
    # Booking methods
    def create_booking(self, user_id, slot_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO bookings (user_id, slot_id)
            VALUES (?, ?)
        ''', (user_id, slot_id))
        
        booking_id = cursor.lastrowid
        
        # Update slot booked count
        cursor.execute('''
            UPDATE slots 
            SET booked_count = booked_count + 1
            WHERE id = ?
        ''', (slot_id,))
        
        conn.commit()
        conn.close()
        return booking_id
    
    def get_all_bookings(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM bookings ORDER BY booked_at DESC')
        bookings = cursor.fetchall()
        
        conn.close()
        
        return [
            {
                'id': booking[0],
                'user_id': booking[1],
                'slot_id': booking[2],
                'booked_at': booking[3]
            }
            for booking in bookings
        ]
    
    # Attendance methods
    def mark_attendance(self, user_id, slot_id, date, status):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO attendance (user_id, slot_id, date, status)
            VALUES (?, ?, ?, ?)
        ''', (user_id, slot_id, date, status))
        
        attendance_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return attendance_id
    
    def get_all_attendance(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM attendance ORDER BY date DESC')
        attendance = cursor.fetchall()
        
        conn.close()
        
        return [
            {
                'id': record[0],
                'user_id': record[1],
                'slot_id': record[2],
                'date': record[3],
                'status': record[4]
            }
            for record in attendance
        ]
    
    # Report methods
    def get_reports(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Get counts
        cursor.execute('SELECT COUNT(*) FROM users')
        total_users = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM slots')
        total_slots = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM bookings')
        total_bookings = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM attendance')
        total_attendance = cursor.fetchone()[0]
        
        # Get recent data
        cursor.execute('SELECT * FROM bookings ORDER BY booked_at DESC LIMIT 5')
        recent_bookings = cursor.fetchall()
        
        cursor.execute('SELECT * FROM attendance ORDER BY date DESC LIMIT 5')
        recent_attendance = cursor.fetchall()
        
        conn.close()
        
        return {
            'summary': {
                'total_users': total_users,
                'total_slots': total_slots,
                'total_bookings': total_bookings,
                'total_attendance': total_attendance
            },
            'recent_bookings': [
                {
                    'id': booking[0],
                    'user_id': booking[1],
                    'slot_id': booking[2],
                    'booked_at': booking[3]
                }
                for booking in recent_bookings
            ],
            'recent_attendance': [
                {
                    'id': record[0],
                    'user_id': record[1],
                    'slot_id': record[2],
                    'date': record[3],
                    'status': record[4]
                }
                for record in recent_attendance
            ]
        }
