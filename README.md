## Установка
1. ```Bash git clone <url>```
2. ```python -m venv venv```
3. ```venv/scripts/activate```
4. ```pip install  -r requirements.txt```
5. ```python -m app.database.db_manage.py``` - инициализация бд, создание коллекций, атрибутов через кастомный db manager
6. Получить ключи с сайта appwrite
7. создать  `.env` файл корне директории проекта и добавить следующие поля:
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






