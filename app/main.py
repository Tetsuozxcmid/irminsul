from appwrite.client import Client
from config import settings

client = Client()

client = (client
          .set_endpoint(settings.APPWRITE_ENDPOINT)
          .set_project(settings.APPWRITE_ID_KEY)
          .set_key(settings.APPWRITE_API_KEY)
          )


