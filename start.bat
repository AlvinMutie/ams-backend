@echo off
echo 🚀 Starting Attachment Management System...

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.7+ first.
    pause
    exit /b 1
)

echo ✅ Python found

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo 📚 Installing dependencies...
pip install -r requirements.txt

REM Create database and add sample data
echo 🗄️  Setting up database...
python -c "from database import Database; db = Database(); db.create_tables(); db.add_sample_data(); print('Database setup complete!')"

echo 🎉 Setup complete! Starting the server...
echo 🌐 Server will be available at: http://localhost:5000
echo 📊 Admin view: http://localhost:5000/admin-view?email=admin@example.com
echo 🔄 Press Ctrl+C to stop the server
echo.

REM Start the Flask application
python app.py

pause

