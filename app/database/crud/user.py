from appwrite.services.databases import Databases
from typing import Optional, Dict, List
import secrets


class UserCRUD:
    def __init__(self, db: Databases, db_id: str, collection_id: str):
        self.db = db
        self.db_id = db_id
        self.collection_id = collection_id

    def add_post_to_user(self, user_id: str, post_id: str) -> Dict:
        return self.db.update_document(database_id=self.db_id,
                                       collection_id=self.collection_id,
                                       document_id=user_id,
                                       data={'post_id': post_id})

    def user_exists(self, user_id: str) -> bool:
        try:
            self.get_user(user_id)
            return True
        except:
            return False

    def create_user(self, balance: int, rank: int, post_id: str) -> Dict:
        data = {
            "balance": balance,
            "rank": rank,
            'post_id': post_id
        }
        return self.db.create_document(database_id=self.db_id, collection_id=self.collection_id, document_id=secrets.token_hex(8), data=data)

    def get_user(self, user_id: str) -> Dict:
        return self.db.get_document(database_id=self.db_id, collection_id=self.collection_id, document_id=user_id)

    def update_user(self, user_id: str, data):
        return self.db.update_document(database_id=self.db_id, collection_id=self.collection_id, document_id=user_id, data=data)

    def delete_user(self, user_id: str):
        return self.db.delete_document(database_id=self.db_id, collection_id=self.collection_id, document_id=user_id)

    def list_users(self) -> Dict:

        return self.db.list_documents(
            database_id=self.db_id,
            collection_id=self.collection_id
        )
