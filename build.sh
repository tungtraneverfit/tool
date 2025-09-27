#!/bin/bash

echo "🐳 Building SSH Remote Command Tool Docker Image..."

# Build Docker image
docker build -t ssh-remote-tool .

if [ $? -eq 0 ]; then
    echo "✅ Docker image built successfully!"
    echo ""
    echo "🚀 To run the container:"
    echo "   docker-compose up -d"
    echo ""
    echo "🌐 Access the tool at:"
    echo "   http://localhost:8080"
    echo ""
    echo "📂 SSH keys will be mounted from:"
    echo "   ~/.ssh -> /app/keys (read-only)"
    echo "   ~/Downloads -> /app/downloads (read-only)"
    echo ""
    echo "🔑 In the web interface, use paths like:"
    echo "   /app/keys/id_rsa"
    echo "   /app/downloads/test.pem"
else
    echo "❌ Docker build failed!"
    exit 1
fi
