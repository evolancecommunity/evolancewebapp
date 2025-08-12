#!/bin/bash

# Evolance Production Deployment Script
set -e

echo "🚀 Starting Evolance Production Deployment..."

# Check if Docker and Docker Compose are installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Load environment variables
if [ -f .env.production ]; then
    echo "📋 Loading production environment variables..."
    export $(cat .env.production | grep -v '^#' | xargs)
else
    echo "⚠️  .env.production not found. Using default values."
fi

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p ssl logs monitoring

# Generate SSL certificates (self-signed for testing)
if [ ! -f ssl/evolance.crt ]; then
    echo "🔐 Generating SSL certificates..."
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
        -keyout ssl/evolance.key -out ssl/evolance.crt \
        -subj "/C=US/ST=State/L=City/O=Evolance/CN=evolance.com"
fi

# Build and start services
echo "🔨 Building Docker images..."
docker-compose build

echo "🚀 Starting services..."
docker-compose up -d

# Wait for services to be healthy
echo "⏳ Waiting for services to be healthy..."
sleep 30

# Check service health
echo "🏥 Checking service health..."
docker-compose ps

# Test API endpoint
echo "🧪 Testing API endpoint..."
if curl -f http://localhost/health > /dev/null 2>&1; then
    echo "✅ API is responding"
else
    echo "❌ API is not responding"
fi

# Test frontend
echo "🧪 Testing frontend..."
if curl -f http://localhost > /dev/null 2>&1; then
    echo "✅ Frontend is responding"
else
    echo "❌ Frontend is not responding"
fi

echo "🎉 Deployment completed successfully!"
echo ""
echo "📊 Service URLs:"
echo "   Frontend: https://evolance.com"
echo "   API: https://evolance.com/api"
echo "   Grafana: http://localhost:3001"
echo "   Prometheus: http://localhost:9090"
echo ""
echo "📝 Useful commands:"
echo "   View logs: docker-compose logs -f"
echo "   Stop services: docker-compose down"
echo "   Restart services: docker-compose restart"
echo "   Update services: docker-compose pull && docker-compose up -d" 