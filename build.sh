#!/bin/bash

# RSS Architect Docker Build Script

echo "🔨 Building RSS Architect Docker Image..."

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

# Build the image with no cache to ensure fresh build
echo "🔨 Building with no cache for fresh build..."
$COMPOSE_CMD build --no-cache

if [ $? -eq 0 ]; then
    echo "✅ RSS Architect Docker image built successfully!"
    echo ""
    echo "🚀 To start the application, run: ./start.sh"
else
    echo "❌ Failed to build RSS Architect Docker image"
    exit 1
fi