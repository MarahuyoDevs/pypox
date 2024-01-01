from pydantic import BaseModel


class UserRegister(BaseModel):
    username: str
    password: str
    name: str
    email: str
    phone: str
