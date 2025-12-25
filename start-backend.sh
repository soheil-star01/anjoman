#!/bin/bash

# Start Anjoman Backend
echo "🚀 Starting Anjoman Backend..."

cd backend

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run setup first:"
    echo "   python -m venv venv"
    echo "   source venv/bin/activate"
    echo "   pip install -r requirements.txt"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found. Please create one with your API keys."
    echo "   cp .env.example .env"
    echo "   Then edit .env to add your API keys."
    exit 1
fi

# Start the server
echo "✅ Starting FastAPI server on http://localhost:8000"
uvicorn main:app --reload --port 8000

