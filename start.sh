#!/bin/bash
# AaryaOnlineCompiler - Startup Script
# Created by Aarya Agarwal

echo "🚀 Starting AaryaOnlineCompiler..."
echo "Created by Aarya Agarwal"
echo ""

# Function to cleanup background processes
cleanup() {
    echo ""
    echo "🛑 Shutting down servers..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit 0
}

# Trap SIGINT (Ctrl+C) and call cleanup
trap cleanup SIGINT

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run setup first."
    exit 1
fi

# Start Django backend
echo "🔧 Starting Django backend on http://localhost:8000..."
cd AaryaCompiler
source ../venv/bin/activate
python manage.py runserver 8000 > ../backend.log 2>&1 &
BACKEND_PID=$!
cd ..

# Wait a moment for backend to start
sleep 3

# Start React frontend
echo "⚛️  Starting React frontend on http://localhost:5173..."
cd frontend
npm run dev > ../frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..

echo ""
echo "✅ Both servers are starting up!"
echo ""
echo "📱 Frontend: http://localhost:5173"
echo "🔌 Backend API: http://localhost:8000/api/"
echo "🔍 Django Admin: http://localhost:8000/admin/"
echo ""
echo "📝 Logs:"
echo "   Backend: backend.log"
echo "   Frontend: frontend.log"
echo ""
echo "⏹️  Press Ctrl+C to stop both servers"
echo ""

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID
