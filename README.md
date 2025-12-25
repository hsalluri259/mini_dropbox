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

### Step 1️⃣ Object Storage (S3 replacement)
Use MinIO (S3-compatible).
```bash
docker run -p 9000:9000 -p 9001:9001 \
  minio/minio server /data --console-address ":9001"
```
We now have:

Buckets

Multipart uploads

Pre-signed URLs

Range GETs

👉 This alone gives you real Dropbox upload/download semantics.

### Step 2️⃣ Metadata DB

Use PostgreSQL.

Schema (simple):

files(
  file_id,
  user_id,
  path,
  size,
  version,
  s3_key,
  created_at
)

### Step 3️⃣ API Server (Core logic)

Language: Python (FastAPI) or Node.js (Express)

Endpoints:

POST   /upload/initiate
POST   /upload/chunk
POST   /upload/complete
GET    /files
GET    /download-url


Responsibilities:

Generate upload_id

Decide chunk size

Issue pre-signed URLs

Emit events after upload

### Step 4️⃣ Client (CLI or Web)

CLI is easiest.

Client logic:

Split file into chunks

Upload chunks in parallel

Retry failed chunks

Resume from last chunk

This is where client-side chunking happens.

### Step 5️⃣ Redis Cache

Cache:

Folder listings

File metadata

Invalidate on:

Upload

Rename

Delete

### Step 6️⃣ Kafka (Async events)

For local dev:

Redpanda (Kafka-compatible, single binary)

Emit:
FileUploaded {
  file_id,
  user_id,
  s3_key,
  size
}
Consumers:

Metadata writer

Search indexer (optional)

Background workers

### Step 7️⃣ Background Workers

Examples:

Fake virus scan

Thumbnail generator

Search index builder

These consume Kafka events.

### Step 8️⃣ CDN Simulation (Optional but powerful)

You won’t run a real CDN, but you can simulate behavior:

Serve downloads via:

Pre-signed URLs

HTTP Range requests

Use browser / curl to test resume:

```bash
curl -H "Range: bytes=0-1048575" <url>
```

This demonstrates server-side chunking.