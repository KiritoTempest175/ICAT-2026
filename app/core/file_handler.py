import os
import shutil
from fastapi import UploadFile

def save_upload(upload_file: UploadFile, storage_path: str) -> str:
    """
    Task C: Save the uploaded file to the local storage.
    """
    if not os.path.exists(storage_path):
        os.makedirs(storage_path)
    
    file_path = os.path.join(storage_path, upload_file.filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)
        
    return file_path

def delete_file(file_path: str):
    """
    Task C: Delete the file for privacy logic.
    """
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
        except OSError as e:
            print(f"Error deleting file {file_path}: {e}")
