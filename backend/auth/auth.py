from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from schemas import schemas


SECRET_KEY="NIGGA123"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=1


oauth2_scheme=OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(data:dict):
    to_encode=data.copy() 
    expire=datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode["exp"]=expire
    encoded_jwt=jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token:str,credentials_exception):
    try:
        payload=jwt.decode(token,SECRET_KEY, algorithms=ALGORITHM)
        user_id=payload.get("id")
        user_email=payload.get("email")
        # user_expiry=payload.get("exp")

        if user_id is None:
            raise credentials_exception
        token_data=schemas.TokenData(user_id=user_id, email=user_email)
        
        return token_data
    
    except JWTError:
        raise credentials_exception
    
def get_current_user(token:str = Depends(oauth2_scheme)):

    credentials_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="could not verify", headers={"WWW.Authenticate":"Bearer"})
    return verify_access_token(token, credentials_exception)

