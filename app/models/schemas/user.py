from pydantic import BaseModel


class UserCreateModel(BaseModel):
    balance: int
    rank: int
    post_id: str
