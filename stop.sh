#!/bin/bash

# RSS Architect Docker Stop Script

echo "🛑 Stopping RSS Architect Docker Container..."

# Check if Docker Compose is available
if command -v docker-compose &> /dev/null; then
    COMPOSE_CMD="docker-compose"
elif docker compose version &> /dev/null; then
    COMPOSE_CMD="docker compose"
else
    echo "❌ Docker Compose is not available."
    exit 1
fi

# Stop the container
$COMPOSE_CMD down

echo "✅ RSS Architect has been stopped."
echo ""
echo "📋 To start again, run: ./start.sh"