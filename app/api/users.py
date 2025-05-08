from fastapi import APIRouter, HTTPException
from database.crud.user import UserCRUD
from models.schemas.user import UserCreateModel
from config import settings
from appwrite.services.databases import Databases
from main import client

router = APIRouter(prefix='/users', tags=['Users'])

db = Databases(client)
user_crud = UserCRUD(db=db, db_id=settings.DB_ID,
                     collection_id=settings.USERS_COLLECTION_ID)


@router.get('/')
async def get_all_users():
    return user_crud.list_users()


@router.post('/', status_code=201)
async def create_user(user_data: UserCreateModel):
    return user_crud.create_user(
        balance=user_data.balance,
        rank=user_data.rank,
        post_id=user_data.post_id
    )


@router.patch('/{user_id}')
async def update_user(user_id: str, update_data: UserCreateModel):
    return user_crud.update_user(
        user_id=user_id,
        data={
            'balance': update_data.balance,
            'rank': update_data.rank,
            'post_id': update_data.post_id
        }
    )


@router.delete('/{user_id}', status_code=204)
async def delete_user(user_id: str):
    return user_crud.delete_user(user_id=user_id)
