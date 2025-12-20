#!/bin/bash

# RSS Architect Docker Startup Script

echo "🚀 Starting RSS Architect Docker Container..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    echo "Visit: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is available
if command -v docker-compose &> /dev/null; then
    COMPOSE_CMD="docker-compose"
elif docker compose version &> /dev/null; then
    COMPOSE_CMD="docker compose"
else
    echo "❌ Docker Compose is not available. Please install Docker Compose."
    exit 1
fi

# Create data directory if it doesn't exist
mkdir -p ./data

# Build and start the container
echo "🔨 Building RSS Architect container..."
$COMPOSE_CMD build

echo "🚀 Starting RSS Architect..."
$COMPOSE_CMD up -d

# Wait a moment for the container to start
sleep 3

# Check if container is running
if $COMPOSE_CMD ps | grep -q "rss-architect.*Up"; then
    echo "✅ RSS Architect is running!"
    echo ""
    echo "🌐 Access the application at: http://localhost:8501"
    echo ""
    echo "📋 Useful commands:"
    echo "  • View logs: $COMPOSE_CMD logs -f"
    echo "  • Stop: $COMPOSE_CMD down"
    echo "  • Restart: $COMPOSE_CMD restart"
    echo "  • Rebuild: $COMPOSE_CMD build --no-cache"
else
    echo "❌ Failed to start RSS Architect container"
    echo "📋 Check logs with: $COMPOSE_CMD logs"
    exit 1
fi