import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from appwrite.services.databases import Databases
import secrets
from app.main import client


class DatabaseInitializer:
    def __init__(self, client):
        self.db = Databases(client)
        self.db_id = None
        self.collections = {}  

    def delete_db(self, db_id):
        try:
            result = self.db.delete(database_id=db_id)
            if self.db_id == db_id:
                self.db_id = None
                self.collections = {}
            return result
        except Exception as e:
            print(f"Ошибка при удалении базы данных {db_id}: {str(e)}")
            

    def create_database(self, name):
        self.db_id = secrets.token_hex(8)
        result = self.db.create(  
            database_id=self.db_id,
            name=name
        )
        return result
    
    def create_collection(self, name):
        collection_id = secrets.token_hex(8)
        result = self.db.create_collection(
            database_id=self.db_id,
            collection_id=collection_id, 
            name=name
        )
        self.collections[name] = collection_id  
        return result
    
    def create_attribute(self, collection_name, name, attr_type, **params):
        
        getattr(self.db, f'create_{attr_type}_attribute')(
            database_id=self.db_id,
            collection_id=self.collections[collection_name],
            key=name,
            **params
        )
    
    def setup_user_collection(self):
        self.create_collection('users')
        for name, attr_type, params in [
            ('balance', 'integer', {'required': True}),
            ('rank', 'integer', {'required': True}),
            ('post_id', 'string', {'size': 255, 'required': True})
        ]:
            self.create_attribute('users', name, attr_type, **params)
    
    def setup_post_collection(self):
        self.create_collection('posts')
        for name, attr_type, params in [
            ('content', 'string', {'size': 255, 'required': True}),
            ('user_id', 'string', {'size': 255, 'required': True}),
            ('file_id', 'string', {'size': 255, 'required': True}),
            ('file_name', 'string', {'size': 255, 'required': True})
            

        ]:
            self.create_attribute('posts', name, attr_type, **params)
    
    def initialize_all(self):
        self.create_database('test_db')
        self.setup_user_collection()
        self.setup_post_collection()
        return {
            'db_id': self.db_id,
            'collections': self.collections
        }
        
try:
    initializer = DatabaseInitializer(client)
    result = initializer.initialize_all()
    print("Успешно создано:", result)
except Exception as e:
    print("Ошибка:", str(e))