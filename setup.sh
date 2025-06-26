#!/bin/bash
# AaryaOnlineCompiler - Setup Script
# Created by Aarya Agarwal

echo "🔧 Setting up AaryaOnlineCompiler..."
echo "Created by Aarya Agarwal"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 16+ first."
    exit 1
fi

# Check if pip is installed
if ! command -v pip &> /dev/null && ! command -v pip3 &> /dev/null; then
    echo "❌ pip is not installed. Please install pip first."
    exit 1
fi

echo "✅ Prerequisites check passed!"
echo ""

# Create virtual environment
echo "🐍 Creating Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Setup Django
echo "🔧 Setting up Django..."
cd AaryaCompiler
python manage.py makemigrations
python manage.py migrate

# Create superuser (optional)
echo ""
read -p "Would you like to create a Django superuser? (y/n): " create_superuser
if [[ $create_superuser =~ ^[Yy]$ ]]; then
    python manage.py createsuperuser
fi

cd ..

# Setup Frontend
echo "⚛️  Setting up React frontend..."
cd frontend
npm install
# Install additional Tailwind CSS PostCSS plugin for v4 compatibility
npm install @tailwindcss/postcss
cd ..

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "🚀 To start the application, run:"
echo "   ./start.sh"
echo ""
echo "📚 Or start manually:"
echo "   Backend:  cd AaryaCompiler && source ../venv/bin/activate && python manage.py runserver"
echo "   Frontend: cd frontend && npm run dev"
echo ""
echo "🌐 The application will be available at:"
echo "   Frontend: http://localhost:5173"
echo "   Backend API: http://localhost:8000/api/"
echo "   Django Admin: http://localhost:8000/admin/"
