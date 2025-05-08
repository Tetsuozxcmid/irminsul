from config import DB_ID, USERS_COLLECTION_ID,POSTS_COLLECTION_ID
from main import client
from models.schemas.post import PostCreateModel
from models.schemas.user import UserCreateModel
from database.crud.user import UserCRUD
from database.crud.post import PostCRUD
from appwrite.services.databases import Databases
from fastapi import FastAPI
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))


app = FastAPI(
    title="mark API",
    description="API user <-> post interaction",
    docs_url="/"
)


db = Databases(client)
DB_ID = DB_ID
USERS_COLLECTION_ID = USERS_COLLECTION_ID


user_crud = UserCRUD(
    db=db,
    db_id=DB_ID,
    collection_id=USERS_COLLECTION_ID
)

post_crud = PostCRUD(
    db=db,
    db_id=DB_ID,
    collection_id=POSTS_COLLECTION_ID
)


@app.get('/users')
async def get_all_users():

    result = user_crud.list_users()
    return result


@app.post('/users', status_code=201)
async def create_user(user_data: UserCreateModel):
    result = user_crud.create_user(
        balance=user_data.balance,
        rank=user_data.rank,
        post_id=user_data.post_id
    )
    return result

@app.patch('/users/{user_id}')
async def Update_user(user_id:str,update_data:UserCreateModel):
    result = user_crud.update_user(user_id=user_id,data={'balance':update_data.balance,'rank':update_data.rank,'post_id': update_data.post_id})
    return result

@app.delete('/users/{user_id}',status_code=204)
async def get_user(user_id: str):
    result = user_crud.delete_user(user_id=user_id)
    return result

@app.get('/posts')
async def get_all_posts():
    result = post_crud.list_posts()
    return result

@app.post('/posts',status_code=201)
async def create_post(post_data: PostCreateModel):
    result = post_crud.create_post(content=post_data.content,user_id=post_data.user_id)
    return result

@app.patch('/posts/{post_id}')
async def Update_post(post_id:str,update_data:PostCreateModel):
    result = post_crud.update_post(post_id=post_id,data={'content':update_data.content,'user_id':update_data.user_id})
    return result

@app.delete('/posts/{post_id}',status_code=204)
async def get_post(post_id: str):
    result = post_crud.delete_user(post_id=post_id)
    return result


