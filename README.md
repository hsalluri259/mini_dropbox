## mini_dropbox
Building a mini dropbox to understand the concepts

## Architecture  
Client (CLI / Web)
   |
   v
API Server (Upload / Metadata)
   |
   +--> Object Storage (MinIO)
   |
   +--> Redis (metadata cache)
   |
   +--> Postgres (metadata DB)
   |
   +--> Kafka / Redpanda (events)
           |
           +--> Workers (indexing, thumbnails)

## Components involved
Here are some of the components that will be involved in building a local dropbox type system.

✅ Chunked uploads
✅ Resumable uploads
✅ Metadata service
✅ Redis cache
✅ Object storage (S3-like)
✅ Pre-signed URLs
✅ Kafka-style async events
✅ Background workers
✅ CDN-like behavior (simulated)

## Implementation plan
### 1️⃣ Setup local Virtual env 
```bash
python3 -m venv mini_dropbox_venv
source mini_dropbox_venv/bin/activate
```
### 2️⃣ Install prerequisites
Run the below script which will
a. Install dependencies
b. Run docker compose to setup minio object storage locally.
```bash
scripts/setup.sh
```

👉 This alone gives us real Dropbox upload/download semantics.
### 3️⃣ FastAPI app structure (clean & scalable)
```bash
dropbox-mini/
├── docker-compose.yml
├── requirements.txt
├── minio-data/
├── app/
│   ├── main.py
│   ├── s3.py
│   └── config.py
├──scripts/
   ├── setup.sh
└── venv/
```

### 4️⃣ Run FastAPI locally (no Docker)
We now have:

S3-compatible storage

FastAPI backend

Pre-signed downloads

Local persistence

To Test upload/download, open `http://localhost:8000/docs` 
This will give unique file_id after uploading. For downloading, the api returns a pre-signed url from which a user can download the file automatically without involving API.
This way uploads/downloads are faster. 