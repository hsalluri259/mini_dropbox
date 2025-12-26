from fastapi import FastAPI, UploadFile
from app.s3 import s3, ensure_bucket
from app.config import settings
import uuid
import logging

app = FastAPI()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger(__name__)

# To be replaced by lifespan
@app.on_event("startup")
def startup():
    ensure_bucket(settings.BUCKET_NAME)
    logger.info(f"Open browser to play with API: http://localhost:8000/docs")

@app.post("/upload")
async def upload_file(file: UploadFile):
    file_id = str(uuid.uuid4())
    s3.upload_fileobj(
        file.file,
        settings.BUCKET_NAME,
        file_id,
        ExtraArgs={"ContentType": file.content_type},
    )
    logger.info(f"file_id is {file_id}, filename is {file.filename}")
    return {
        "file_id": file_id,
        "filename": file.filename
    }

@app.get("/download-url/{file_id}")
def get_download_url(file_id: str):
    url = s3.generate_presigned_url(
        "get_object",
        Params={
            "Bucket": settings.BUCKET_NAME,
            "Key": file_id,
        },
        ExpiresIn=3600,
    )
    logger.info(f"Issued download URL for file {file_id}")
    return {"url": url}
