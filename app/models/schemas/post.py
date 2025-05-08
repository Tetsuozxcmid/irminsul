from pydantic import BaseModel


class PostCreateModel(BaseModel):
    content: str
    user_id: str
