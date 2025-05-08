from fastapi import APIRouter, HTTPException
from appwrite.services.databases import Databases
from main import client

router = APIRouter(prefix="/db", tags=["Database Management"])

@router.delete('/{db_id}', status_code=204)
async def delete_database(db_id: str):
    try:
        db = Databases(client)
        db.delete(database_id=db_id)
        return None
    except Exception as e:
        raise HTTPException(500, detail=str(e))