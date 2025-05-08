from appwrite.services.databases import Databases
from appwrite.services.storage import Storage
from appwrite.input_file import InputFile
from database.crud.user import UserCRUD
from typing import  Dict
from config import settings
import secrets


class FileStorage:
    def __init__(self, client):
        self.storage = Storage(client)
        self.bucket_id = settings.BUCKET_ID

    def create_bucket(self, name: str):
        self.bucket_id = secrets.token_hex(8)
        return self.storage.create_bucket(bucket_id=self.bucket_id, name=name)

    def delete_bucket(self, bucket_id: str):
        return self.storage.delete_bucket(bucket_id=bucket_id)

    def upload_file(self, file_path: str):
        file = InputFile.from_path(file_path)
        return self.storage.create_file(bucket_id=self.bucket_id, file_id=secrets.token_hex(8), file=file)

    def delete_file(self, file_id: str):
        return self.storage.delete_file(bucket_id=self.bucket_id, file_id=file_id)

    def list_file(self):
        return self.storage.list_files(self.bucket_id)


class PostCRUD:
    def __init__(self, db: Databases, db_id: str, collection_id: str, storage: FileStorage, user_crud: UserCRUD):
        self.db = db
        self.storage = storage
        self.db_id = db_id
        self.collection_id = collection_id
        self.user_crud = user_crud

    def create_file_post(self, content, user_id, file_path):
        file_info = self.storage.upload_file(file_path)
        data = {
            "content": content,
            "user_id": user_id,
            "file_id": file_info['$id'],
            "file_name": file_info['name']
        }
        return self.db.create_document(database_id=self.db_id, collection_id=self.collection_id, document_id=secrets.token_hex(8), data=data)

    def create_post(self, data: dict) -> Dict:
        if not self.user_crud.user_exists(data['user_id']):
            raise ValueError(f"User {data['user_id']} does not exist")

        return self.db.create_document(
            database_id=self.db_id,
            collection_id=self.collection_id,
            document_id=secrets.token_hex(8),
            data=data
        )

    def get_post(self, post_id: str) -> Dict:
        return self.db.get_document(database_id=self.db_id, collection_id=self.collection_id, document_id=post_id)

    def update_post(self, post_id: str, data):
        return self.db.update_document(database_id=self.db_id, collection_id=self.collection_id, document_id=post_id, data=data)

    def delete_post(self, post_id: str):
        return self.db.delete_document(database_id=self.db_id, collection_id=self.collection_id, document_id=post_id)

    def list_posts(self) -> Dict:

        return self.db.list_documents(
            database_id=self.db_id,
            collection_id=self.collection_id
        )
