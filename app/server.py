import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))

from fastapi import FastAPI
from pydantic import BaseModel
from appwrite.services.databases import Databases
from database.crud.user import UserCRUD
from main import client  
from config import DB_ID,USERS_COLLECTION_ID
app = FastAPI(
    title="Simple Todo API",
    description="A simple API built using AppWrite's db",
    docs_url="/"
)


db = Databases(client)
DB_ID = DB_ID  
USERS_COLLECTION_ID = USERS_COLLECTION_ID 


crud = UserCRUD(
    db=db,
    db_id=DB_ID,
    collection_id=USERS_COLLECTION_ID
)

class UserCreateModel(BaseModel):
    balance: int
    rank: int
    post_id: str

@app.get('/users')
async def get_all_users():
    
    result = crud.list_users()  
    return result

@app.post('/users', status_code=201)
async def create_user(user_data: UserCreateModel):
    result = crud.create_user(
        balance=user_data.balance,
        rank=user_data.rank,
        post_id=user_data.post_id
    )
    return result