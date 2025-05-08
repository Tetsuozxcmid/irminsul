from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from pathlib import Path
from database.crud.post import PostCRUD
from config import settings
from appwrite.services.databases import Databases
from main import client
from api.storage import file_storage

router = APIRouter(prefix="/posts", tags=["Posts"])

db = Databases(client)
post_crud = PostCRUD(
    db=db,
    db_id=settings.DB_ID,
    collection_id=settings.POSTS_COLLECTION_ID,
    storage=file_storage  
)

@router.get('/')
async def get_all_posts():
    return post_crud.list_posts()

@router.post('/', status_code=201)
async def create_post(content: str = Form(...), user_id: str = Form(...)):
    return post_crud.create_post(content=content, user_id=user_id)

@router.patch('/{post_id}')
async def update_post(
    post_id: str,
    content: str = Form(...),
    user_id: str = Form(...),
    file: UploadFile = File(None)
):
    data = {'content': content, 'user_id': user_id}
    if file:
        try:
            file_path = f"{file.filename}"
            with open(file_path, "wb") as buffer:
                buffer.write(await file.read())
            file_info = file_storage.upload_file(file_path)
            data.update({
                'file_id': file_info['$id'],
                'file_name': file_info['name']
            })
            Path(file_path).unlink(missing_ok=True)
        except Exception as e:
            raise HTTPException(500, detail=f'File upload failed: {str(e)}')
    return post_crud.update_post(post_id=post_id, data=data)

@router.delete('/{post_id}', status_code=204)
async def delete_post(post_id: str):
    return post_crud.delete_post(post_id=post_id)