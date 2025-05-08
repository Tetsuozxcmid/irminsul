from appwrite.services.databases import Databases
from typing import Optional, Dict, List
import secrets



class PostCRUD:
    def __init__(self, db: Databases, db_id: str, collection_id: str):
        self.db = db
        self.db_id = db_id
        self.collection_id = collection_id

    def create_post(self, content, user_id) -> Dict:
        data = {
            "content": content,
            'user_id': user_id
        }
        return self.db.create_document(database_id=self.db_id, collection_id=self.collection_id, document_id=secrets.token_hex(8), data=data)

    def get_post(self, post_id: str) -> Dict:
        return self.db.get_document(database_id=self.db_id, collection_id=self.collection_id, document_id=post_id)

    def update_post(self,post_id: str,data):
        return self.db.update_document(database_id=self.db_id,collection_id=self.collection_id,document_id=post_id,data=data)
    
    def delete_post(self,post_id: str):
        return self.db.delete_document(database_id=self.db_id,collection_id=self.collection_id,document_id=post_id)
    
    
    def list_posts(self) -> Dict:

        return self.db.list_documents(
            database_id=self.db_id,
            collection_id=self.collection_id
        )