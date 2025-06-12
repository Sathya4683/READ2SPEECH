from jose import JWTError, jwt
from datetime import datetime, timedelta,timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from schemas import req_sch 
from config import settings

oauth2_scheme=OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(data:dict):
    to_encode=data.copy() 
    expire=datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode["exp"]=expire
    encoded_jwt=jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt

def verify_access_token(token:str,credentials_exception):
    try:
        payload=jwt.decode(token,settings.secret_key, algorithms=settings.algorithm)
        user_id=payload.get("id")
        user_email=payload.get("email")

        if user_id is None:
            raise credentials_exception
        token_data=req_sch.TokenData(user_id=user_id, email=user_email)
        return token_data
    except JWTError:
        raise credentials_exception
    
def get_current_user(token:str = Depends(oauth2_scheme)):
    credentials_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="could not verify", headers={"WWW.Authenticate":"Bearer"})
    return verify_access_token(token, credentials_exception)


