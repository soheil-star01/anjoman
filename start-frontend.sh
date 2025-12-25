#!/bin/bash

# Start Anjoman Frontend
echo "🚀 Starting Anjoman Frontend..."

cd frontend

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "❌ node_modules not found. Please run setup first:"
    echo "   npm install"
    exit 1
fi

# Start the dev server
echo "✅ Starting Next.js dev server on http://localhost:3000"
npm run dev

