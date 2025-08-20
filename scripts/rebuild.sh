#!/bin/bash

echo "Rebuilding Team Manager..."

# Stop and remove existing container
docker stop team_manager
docker rm team_manager

# Rebuild image
docker build -t team_manager .

# Run new container
docker run -d \
  --name team_manager \
  -p 5000:5000 \
  -v $(pwd)/data:/app/data \
  team_manager

echo "Rebuild complete! Application available at http://localhost:5000"