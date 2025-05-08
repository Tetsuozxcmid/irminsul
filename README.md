## About

  - Использование API `Appwrite` для создания коллекций user,post и атрибутов в которые входят
    
    - user
      - `id`
      -  balance`(валюта)`
      -  rank `(ранг в сервисе)`
        
    - post
      - `id` 
      -   content`(описание)` 
      -   user_id`(привязка к юзеру который загрузил пост(указывается в свагере в поле user_id нужно ввести айдишник юзера которого надо связать))`
      -   file_id `(айдишник файла)`
      -   file `(загружаемый с помощью InputUpload файл ( в пробной версии appwrite максимум 50мб(указано в сваггере)` 
      -   file_name`(название файла))`
        
    - file bucket `просто хранилище файлов загруженных` где есть `file_id` `file_name` `file`
      
    Пользователь может загружать посты с файлами , удалять, обновлять их
      -   user <=> post `по айдишнику`

## Установка
1. ```git clone <url>```
   
3. ```python -m venv venv```
   
5. ```venv/scripts/activate```
   
7. ```pip install  -r requirements.txt```
   
9. ```python -m app.database.db_manage.py``` - инициализация бд, создание коллекций, атрибутов через кастомный db manager
    
11. Получить ключи с сайта appwrite
    
13. создать  `.env` файл корне директории проекта и добавить следующие поля ( какие то показываются при ините бд, какие то с appwrite можно взять) :
```
APPWRITE_ID_KEY=your-appwrite-id-key
APPWRITE_API_KEY=your-appwrite-api-key
DB_ID=your-db-id
USERS_COLLECTION_ID=your-users-collection-id
POSTS_COLLECTION_ID=your-posts-collection-id
BUCKET_ID=your-bucket-id
```
8. ```cd app```
9. ```uvicorn run:app --port 8001```

## Crud операции

- ```Создание бакета( временного хранилища для дальнейшего использования), удаление, обновление```
  
```Python 
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

```

- ```CRUD постов ( создание, удаление, привязка user_id по круду юзера, обновление постов)```
  
```Python
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

```

- ```CRUD Юзеров (Создание, обновление, удаление, вывод всех или по айдишнику, проверка есть ли юзер для связи с постами)```
  
```Python

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

```

## API

API Эндпоинты находятся в следующих директориях:

- `api/users.py`: Эндпоинты для взаимодействия с юзерами.
- `api/posts.py`: Эндпоинты для взаимодействия с постами(документами, загруженными файлами) ```Связаны айдишником с юзером, в свагере указывается айдишник юзера и привязывается в коллекцию поста айдишник, айдишник файла, название файла```.
- `api/storage.py`: Эндпоинты для взаимодействия с бакетами, тоесть хранилищем загруженных файлов.
- `api/db.py`: Эндпоинты для взаимодействия с базой данных.

Все эндпоинты находятся по локалхост адресу  `http://localhost:8000/docs`.

| Эндпоинт              | Описание                                                                 | Что использует                     |
| ---------------------- | --------------------------------------------------------------------------- | ------------------------------------------------------------ |
| `DELETE` /db/{db_id}    | Полностью удаляет базу данных в Appwrite по указанному ID.                    | `Databases из Appwrite SDK, HTTPException для обработки ошибок `|
| `POST` /storage/upload          | Загружает файл в хранилище Appwrite.                               |   `FileStorage, UploadFile из FastAPI, временные файлы `                                                               |
| `DELETE` /storage/bucket/{bucket_id}     | Удаляет bucket (контейнер для файлов) в Appwrite.                   | `FileStorage.delete_bucket(), обработка ошибок `                           |
| `GET` /users/	|Получает список всех пользователей	                                                      | `UserCRUD.list_users(), Appwrite Databases `                             |
| `POST ` /users/|	Создает нового пользователя|	`UserCreateModel для валидации, UserCRUD.create_user()` |
|`PATCH ` /users/{user_id} |	Обновляет данные пользователя	 |   `UserCreateModel, UserCRUD.update_user()`  |
| `DELETE` /users/{user_id}	|Удаляет пользователя	|`UserCRUD.delete_user(), статус 204` |
|`GET` /posts/|	Получает список всех постов|	`PostCRUD.list_posts(), Appwrite Databases` |
|`POST` /posts/	|Создает новый пост (с возможностью прикрепления файла)	|`Form данные, UploadFile, PostCRUD.create_post(), FileStorage` |
|`PATCH ` /posts/{post_id}	|Обновляет существующий пост	|`Form данные, UploadFile, PostCRUD.update_post() `|
| `DELETE ` /posts/{post_id} |	Удаляет пост|	`PostCRUD.delete_post(), статус 204`|


## Логирование
 - C помощью Logging и middleware
     - Logging 
  ```Python
   import logging


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

```
  - Middleware
```Python
from fastapi import Request
from datetime import datetime

from core.logger import logger


async def log_requests(request: Request, call_next):
    start_time = datetime.now()
    
    response = await call_next(request)

    process_time = (datetime.now() - start_time).total_seconds() * 1000
    
    logger.info(
        f"Method={request.method} Path={request.url.path} "
        f"Status={response.status_code} "
        f"ProcessTime={process_time:.2f}ms"
    )
    
    return response
```






