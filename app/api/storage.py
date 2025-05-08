from fastapi import APIRouter, UploadFile, File, HTTPException
from main import client
from database.crud.post import FileStorage
from pathlib import Path

router = APIRouter(prefix="/storage", tags=["Storage"])

file_storage = FileStorage(client)

@router.post('/upload')
async def upload_file(file: UploadFile = File(...)):
    try:
        file_path = f"{file.filename}"
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())
        result = file_storage.upload_file(file_path)
        Path(file_path).unlink(missing_ok=True)
        return result
    except Exception as e:
        raise HTTPException(500, detail=str(e))
    
@router.delete('/bucket/{bucket_id}', status_code=204)
async def delete_bucket(bucket_id: str):
    try:
        return file_storage.delete_bucket(bucket_id=bucket_id)
    except Exception as e:
        raise HTTPException(500, detail=str(e))