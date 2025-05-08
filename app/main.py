from appwrite.client import Client
from config import APPWRITE_ID_KEY, APPWRITE_API_KEY

client = Client()

client = (client
          .set_endpoint('https://cloud.appwrite.io/v1')
          .set_project(APPWRITE_ID_KEY)
          .set_key(APPWRITE_API_KEY)
          )

print(client)
