from os import environ
from dotenv import load_dotenv

load_dotenv()

APPWRITE_ID_KEY= environ.get('APPWRITE_ID_KEY')
APPWRITE_API_KEY = environ.get('APPWRITE_API_KEY')
DB_ID=environ.get('DB_ID')
USERS_COLLECTION_ID=environ.get('USERS_COLLECTION_ID')
