from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    secret_key:str
    algorithm:str
    access_token_expire_minutes:int
    google_client_id:str
    google_client_secret:str
    google_redirect_uri:str
    scopes:str
    google_auth_url:str
    google_token_url:str
    google_userinfo_url:str


    class Config:
        env_file = "../.env"

settings=Settings()

