#! /bin/bash

# Run as scripts/setup.sh 
# Launch Minio Object storage
docker compose up -d

# Install python prerequisites for API
pip install -r requirements.txt

# Run FastAPI locally
uvicorn app.main:app --reload

