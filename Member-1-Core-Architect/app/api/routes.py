from fastapi import APIRouter, UploadFile, File, BackgroundTasks, HTTPException
from app.core.file_handler import save_upload, delete_file
from app.core.processor import clean_pdf_text
from app.models import ProcessResponse
import os

router = APIRouter()
UPLOAD_DIR = "storage/uploads"

@router.post("/upload")
async def upload(file: UploadFile = File(...)):
    # Task A + C: Uses new handler
    path = save_upload(file, UPLOAD_DIR)
    return {"filename": file.filename, "saved_at": path}

@router.post("/process", response_model=ProcessResponse)
async def process(filename: str, background_tasks: BackgroundTasks):
    file_path = os.path.join(UPLOAD_DIR, filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail=f"File {filename} not found in uploads")

    # Task B: Clean text
    content = clean_pdf_text(file_path)
    
    # Task C: Use delete_file logic in the background
    background_tasks.add_task(delete_file, file_path)
    
    return ProcessResponse(
        filename=filename,
        content=content,
        message="File processed and scheduled for deletion"
    )