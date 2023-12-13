#!/bin/bash

# Run tests for main service
docker build -t btc-dashboard -f ./services/btc-dashboard/Dockerfile ./services/btc-dashboard

docker-compose -f docker-compose.test.yml up -d
docker-compose logs --tail=1000 -f btc-dashboard
docker-compose down