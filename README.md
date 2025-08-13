# Attachment Management System - Flask Backend

A complete Flask backend for managing student attachments, slots, bookings, and attendance tracking.

## Features

- **User Management**: Registration and authentication for different user roles
- **Slot Management**: Create and manage available attachment slots
- **Booking System**: Students can book available slots
- **Attendance Tracking**: Supervisors can mark student attendance
- **Reporting**: Comprehensive reports and analytics
- **Admin Panel**: HTML view for administrators to monitor all data

## User Roles

1. **Student** → Register, login, view available slots, book a slot
2. **Industry Supervisor** → Login, view assigned students, mark attendance
3. **School Supervisor** → Login, view reports
4. **Admin (Attachment Coordinator)** → Login, manage slots, view all data

## API Endpoints

| Endpoint | Method | Description | Access |
|----------|--------|-------------|---------|
| `/` | GET | Home page | Public |
| `/register` | POST | User registration | Public |
| `/login` | POST | User authentication | Public |
| `/slots` | GET | Get available slots | Public |
| `/book` | POST | Book a slot | Students only |
| `/attendance` | POST | Mark attendance | Supervisors only |
| `/reports` | GET | Get system reports | Public |
| `/admin-view` | GET | Admin HTML panel | Admin only |

## Database Schema

### Users Table
- `id` - Primary key
- `name` - User's full name
- `email` - Unique email address
- `password` - Hashed password (SHA-256)
- `role` - User role (student, industry_supervisor, school_supervisor, admin)
- `created_at` - Timestamp

### Slots Table
- `id` - Primary key
- `date` - Slot date (YYYY-MM-DD)
- `capacity` - Maximum number of students
- `booked_count` - Current number of bookings
- `created_at` - Timestamp

### Bookings Table
- `id` - Primary key
- `user_id` - Foreign key to users table
- `slot_id` - Foreign key to slots table
- `created_at` - Timestamp

### Attendance Table
- `id` - Primary key
- `booking_id` - Foreign key to bookings table
- `date` - Attendance date (YYYY-MM-DD)
- `status` - Present or absent
- `created_at` - Timestamp

## Installation & Setup

### Prerequisites
- Python 3.7+
- pip

### 1. Clone the repository
```bash
git clone <repository-url>
cd attachment-management-system
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the application
```bash
python app.py
```

The server will start on `http://localhost:5000`

### 4. Test the API
```bash
python test_api.py
```

## Deployment to Render

### 1. Create a new Web Service on Render
- Connect your GitHub repository
- Choose Python as the runtime
- Set build command: `pip install -r requirements.txt`
- Set start command: `gunicorn app:app`

### 2. Environment Variables (Optional)
- `FLASK_ENV`: Set to `production` for production deployment

### 3. Deploy
- Render will automatically build and deploy your application
- The app will be available at your Render URL

## API Usage Examples

### Register a New User
```bash
curl -X POST http://localhost:5000/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "password123",
    "role": "student"
  }'
```

### Login
```bash
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "password123"
  }'
```

### Get Available Slots
```bash
curl http://localhost:5000/slots
```

### Book a Slot
```bash
curl -X POST http://localhost:5000/book \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "slot_id": 1
  }'
```

### Mark Attendance
```bash
curl -X POST http://localhost:5000/attendance \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": 1,
    "date": "2024-01-15"
  }'
```

### Get Reports
```bash
curl http://localhost:5000/reports
```

### Admin View
```
http://localhost:5000/admin-view?email=admin@example.com
```

## Sample Data

The system comes with pre-loaded sample data:

- **Users**: 3 students, 1 industry supervisor, 1 school supervisor, 1 admin
- **Slots**: 5 slots with different capacities
- **Bookings**: 3 sample bookings
- **Attendance**: 3 sample attendance records

### Default Admin Credentials
- Email: `admin@example.com`
- Password: `password123`

## Security Features

- Password hashing using SHA-256
- Role-based access control
- Input validation and sanitization
- SQL injection prevention through parameterized queries
- CORS enabled for frontend integration

## Error Handling

All API endpoints return appropriate HTTP status codes:

- `200` - Success
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `409` - Conflict
- `500` - Internal Server Error

## Testing

Run the comprehensive test suite:

```bash
python test_api.py
```

This will test all endpoints and provide detailed output.

## File Structure

```
attachment-management-system/
├── app.py              # Main Flask application
├── database.py         # Database operations and models
├── requirements.txt    # Python dependencies
├── test_api.py        # API testing script
├── README.md          # This file
└── database.db        # SQLite database (created automatically)
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For questions or issues, please open an issue on GitHub or contact the development team. 