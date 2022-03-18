#!/bin/bash
docker build -f Dockerfile . -t swordphish3:1.0.0
docker-compose up -d
