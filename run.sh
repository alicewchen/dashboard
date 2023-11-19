#!/bin/bash

docker build -t btc-dashboard -f ./services/btc-dashboard/Dockerfile ./services/btc-dashboard

docker-compose down
docker-compose up