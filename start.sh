#!/bin/bash

echo "🚀 Starting Attachment Management System..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.7+ first."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip first."
    exit 1
fi

echo "✅ Python and pip found"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate


# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Create database and add sample data
echo "🗄️  Setting up database..."
python3 -c "from database import Database; db = Database(); db.create_tables(); db.add_sample_data(); print('Database setup complete!')"

echo "🎉 Setup complete! Starting the server..."
echo "🌐 Server will be available at: http://localhost:5000"
echo "📊 Admin view: http://localhost:5000/admin-view?email=admin@example.com"
echo "🔄 Press Ctrl+C to stop the server"
echo ""

# Start the Flask application
python3 app.py
