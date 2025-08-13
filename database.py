import sqlite3
import datetime
from typing import List, Dict, Optional

class Database:
    def __init__(self, db_path: str = 'database.db'):
        self.db_path = db_path
        # Don't automatically create tables here - let Flask app control this
    
    def initialize_database(self):
        """Initialize database with tables and sample data - call this once"""
        self.create_tables()
        self.add_sample_data()
    
    def get_connection(self):
        """Get database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # This allows accessing columns by name
        return conn
    
    def create_tables(self):
        """Create all required tables if they don't exist"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL CHECK (role IN ('student', 'industry_supervisor', 'school_supervisor', 'admin')),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Slots table - updated to match Flask app expectations
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS slots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL DEFAULT 'Attachment Slot',
                date TEXT NOT NULL,
                time TEXT NOT NULL DEFAULT '09:00-17:00',
                max_capacity INTEGER NOT NULL DEFAULT 10,
                booked_count INTEGER NOT NULL DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
                FOREIGN KEY (slot_id) REFERENCES slots (id),
                UNIQUE(user_id)
            )
        ''')
        
        # Attendance table - updated to match Flask app expectations
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS attendance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                slot_id INTEGER NOT NULL,
                date TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'present' CHECK (status IN ('present', 'absent', 'late')),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (slot_id) REFERENCES slots (id),
                UNIQUE(user_id, slot_id, date)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_sample_data(self):
        """Add sample data for testing"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Check if data already exists
        cursor.execute("SELECT COUNT(*) FROM users")
        if cursor.fetchone()[0] > 0:
            conn.close()
            return
        
        # Add sample users
        sample_users = [
            ('John Doe', 'john@student.com', 'password123', 'student'),
            ('Jane Smith', 'jane@student.com', 'password123', 'student'),
            ('Bob Johnson', 'bob@student.com', 'password123', 'student'),
            ('Dr. Alice Brown', 'alice@supervisor.com', 'password123', 'industry_supervisor'),
            ('Prof. Charlie Wilson', 'charlie@school.com', 'password123', 'school_supervisor'),
            ('Admin User', 'admin@example.com', 'password123', 'admin')
        ]
        
        for user in sample_users:
            hashed_password = self._hash_password(user[2])
            cursor.execute('''
                INSERT INTO users (name, email, password, role)
                VALUES (?, ?, ?, ?)
            ''', (user[0], user[1], hashed_password, user[3]))
        
        # Add sample slots - updated to match new schema
        sample_slots = [
            ('Morning Slot', '2024-01-15', '09:00-12:00', 5),
            ('Afternoon Slot', '2024-01-16', '13:00-17:00', 5),
            ('Full Day Slot', '2024-01-17', '09:00-17:00', 5),
            ('Morning Slot', '2024-01-18', '09:00-12:00', 5),
            ('Afternoon Slot', '2024-01-19', '13:00-17:00', 5)
        ]
        
        for slot in sample_slots:
            cursor.execute('''
                INSERT INTO slots (name, date, time, max_capacity)
                VALUES (?, ?, ?, ?)
            ''', slot)
        
        # Add sample bookings
        sample_bookings = [
            (1, 1),  # John Doe -> Slot 1
            (2, 2),  # Jane Smith -> Slot 2
            (3, 3)   # Bob Johnson -> Slot 3
        ]
        
        for booking in sample_bookings:
            cursor.execute('''
                INSERT INTO bookings (user_id, slot_id, booked_at)
                VALUES (?, ?, ?)
            ''', (booking[0], booking[1], datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            
            # Update slot booked count
            cursor.execute('''
                UPDATE slots SET booked_count = booked_count + 1
                WHERE id = ?
            ''', (booking[1],))
        
        # Add sample attendance - updated to match new schema
        sample_attendance = [
            (1, 1, '2024-01-15', 'present'),  # John Doe present on Jan 15
            (2, 2, '2024-01-16', 'present'),  # Jane Smith present on Jan 16
            (3, 3, '2024-01-17', 'present')   # Bob Johnson present on Jan 17
        ]
        
        for attendance in sample_attendance:
            cursor.execute('''
                INSERT INTO attendance (user_id, slot_id, date, status)
                VALUES (?, ?, ?, ?)
            ''', attendance)
        
        conn.commit()
        conn.close()
    
    def _hash_password(self, password: str) -> str:
        """Hash password using SHA-256"""
        import hashlib
        return hashlib.sha256(password.encode()).hexdigest()
    
    # User operations
    def create_user(self, name: str, email: str, password: str, role: str) -> int:
        """Create a new user and return user ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO users (name, email, password, role)
                VALUES (?, ?, ?, ?)
            ''', (name, email, password, role))
            
            user_id = cursor.lastrowid
            conn.commit()
            return user_id
        except sqlite3.IntegrityError:
            raise Exception("User with this email already exists")
        finally:
            conn.close()
    
    def get_user_by_email(self, email: str) -> Optional[Dict]:
        """Get user by email"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        user = cursor.fetchone()
        
        conn.close()
        return dict(user) if user else None
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict]:
        """Get user by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        user = cursor.fetchone()
        
        conn.close()
        return dict(user) if user else None
    
    def get_users_by_role(self, role: str) -> int:
        """Get count of users by role"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM users WHERE role = ?', (role,))
        count = cursor.fetchone()[0]
        
        conn.close()
        return count
    
    def get_all_users(self) -> List[Dict]:
        """Get all users"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT id, name, email, role, created_at FROM users ORDER BY id')
        users = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        return users
    
    def get_total_users(self) -> int:
        """Get total number of users"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM users')
        count = cursor.fetchone()[0]
        
        conn.close()
        return count
    
    # Slot operations
    def get_available_slots(self) -> List[Dict]:
        """Get all available slots"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM slots 
            WHERE booked_count < max_capacity
            ORDER BY date
        ''')
        slots = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        return slots
    
    def get_slot_by_id(self, slot_id: int) -> Optional[Dict]:
        """Get slot by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM slots WHERE id = ?', (slot_id,))
        slot = cursor.fetchone()
        
        conn.close()
        return dict(slot) if slot else None
    
    def get_next_available_slot(self) -> Optional[Dict]:
        """Get next available slot"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM slots 
            WHERE booked_count < max_capacity
            ORDER BY date
            LIMIT 1
        ''')
        slot = cursor.fetchone()
        
        conn.close()
        return dict(slot) if slot else None
    
    def update_slot_booked_count(self, slot_id: int):
        """Update slot booked count"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE slots SET booked_count = booked_count + 1
            WHERE id = ?
        ''', (slot_id,))
        
        conn.commit()
        conn.close()
    
    def get_all_slots(self) -> List[Dict]:
        """Get all slots"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM slots ORDER BY date')
        slots = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        return slots
    
    def get_total_slots(self) -> int:
        """Get total number of slots"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM slots')
        count = cursor.fetchone()[0]
        
        conn.close()
        return count
    
    # Booking operations
    def create_booking(self, user_id: int, slot_id: int) -> int:
        """Create a new booking and return booking ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO bookings (user_id, slot_id, booked_at)
                VALUES (?, ?, ?)
            ''', (user_id, slot_id, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            
            booking_id = cursor.lastrowid
            conn.commit()
            return booking_id
        except sqlite3.IntegrityError:
            raise Exception("User already has a booking")
        finally:
            conn.close()
    
    def get_booking_by_user(self, user_id: int) -> Optional[Dict]:
        """Get booking by user ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT b.*, s.date as slot_date, s.name as slot_name
            FROM bookings b
            JOIN slots s ON b.slot_id = s.id
            WHERE b.user_id = ?
        ''', (user_id,))
        booking = cursor.fetchone()
        
        conn.close()
        return dict(booking) if booking else None
    
    def get_all_bookings(self) -> List[Dict]:
        """Get all bookings with user and slot info"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT b.*, u.name as user_name, s.date as slot_date, s.name as slot_name
            FROM bookings b
            JOIN users u ON b.user_id = u.id
            JOIN slots s ON b.slot_id = s.id
            ORDER BY b.booked_at DESC
        ''')
        bookings = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        return bookings
    
    def get_total_bookings(self) -> int:
        """Get total number of bookings"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM bookings')
        count = cursor.fetchone()[0]
        
        conn.close()
        return count
    
    def get_recent_bookings(self, limit: int = 5) -> List[Dict]:
        """Get recent bookings"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT b.*, u.name as user_name, s.date as slot_date
            FROM bookings b
            JOIN users u ON b.user_id = u.id
            JOIN slots s ON b.slot_id = s.id
            ORDER BY b.booked_at DESC
            LIMIT ?
        ''', (limit,))
        bookings = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        return bookings
    
    # Attendance operations
    def create_attendance(self, user_id: int, slot_id: int, date: str, status: str) -> int:
        """Create attendance record and return attendance ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO attendance (user_id, slot_id, date, status)
                VALUES (?, ?, ?, ?)
            ''', (user_id, slot_id, date, status))
            
            attendance_id = cursor.lastrowid
            conn.commit()
            return attendance_id
        except sqlite3.IntegrityError:
            raise Exception("Attendance already marked for this user, slot, and date")
        finally:
            conn.close()
    
    def get_attendance_by_booking_date(self, booking_id: int, date: str) -> Optional[Dict]:
        """Get attendance by booking ID and date"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT a.*, u.name as student_name
            FROM attendance a
            JOIN users u ON a.user_id = u.id
            WHERE a.slot_id = ? AND a.date = ?
        ''', (booking_id, date))
        attendance = cursor.fetchone()
        
        conn.close()
        return dict(attendance) if attendance else None
    
    def get_all_attendance(self) -> List[Dict]:
        """Get all attendance records"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT a.*, u.name as user_name, s.name as slot_name
            FROM attendance a
            JOIN users u ON a.user_id = u.id
            JOIN slots s ON a.slot_id = s.id
            ORDER BY a.date DESC
        ''')
        attendance = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        return attendance
    
    def get_total_attendance(self) -> int:
        """Get total number of attendance records"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM attendance')
        count = cursor.fetchone()[0]
        
        conn.close()
        return count
    
    def get_recent_attendance(self, limit: int = 5) -> List[Dict]:
        """Get recent attendance records"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT a.*, u.name as user_name, s.name as slot_name
            FROM attendance a
            JOIN users u ON a.user_id = u.id
            JOIN slots s ON a.slot_id = s.id
            ORDER BY a.date DESC
            LIMIT ?
        ''', (limit,))
        attendance = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        return attendance
