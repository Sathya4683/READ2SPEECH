from pydantic import BaseModel,EmailStr,HttpUrl


class Link(BaseModel):
    url:HttpUrl

class SetPreferences(BaseModel):
    mails:bool

class Token(BaseModel):
    username:EmailStr 
    password:str

class TokenData(BaseModel):
    user_id: int
    email:EmailStr

class Signup(BaseModel):
    username:EmailStr
    password:str
    

