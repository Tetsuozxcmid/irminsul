from pydantic_settings import BaseSettings, SettingsConfigDict


class AppwriteConfig(BaseSettings):
    APPWRITE_ENDPOINT: str = "https://cloud.appwrite.io/v1"
    APPWRITE_ID_KEY: str
    APPWRITE_API_KEY: str
    DB_ID: str
    USERS_COLLECTION_ID: str
    POSTS_COLLECTION_ID: str
    BUCKET_ID: str

    model_config = SettingsConfigDict(env_file='.env')


settings = AppwriteConfig()
