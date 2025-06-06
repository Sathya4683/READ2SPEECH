from fastapi import FastAPI, Body, Request,Form, Depends,HTTPException, status
import uvicorn
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt,JWTError
from datetime import datetime, timedelta

app =FastAPI()

# Secret key to encode the JWT
SECRET_KEY = "your-secret-key"  # this is the secret key used to validate if the token is actually provided by you and not hampered 
ALGORITHM = "HS256"              # algorithm used to sign the JWT
# ACCESS_TOKEN_EXPIRE_MINUTES = 30 # token expiry time
ACCESS_TOKEN_EXPIRE_SECONDS = 30  # to test out in real time how the token expires after 30 seconds

oauth_scheme=OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(data:dict, expires_delta):
    to_encode=data.copy()
    expire= datetime.utcnow() + (expires_delta)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    print(encoded_jwt)
    return encoded_jwt

#verify if the token is still valid... to use the funfact route
def verify_token(token:str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # If expired, this line will raise JWTError
        username = payload.get("sub")
        if username is None:
                raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return username
    except JWTError:
        # Token invalid or expired
        raise HTTPException(status_code=401, detail="Could not validate credentials")

#go to the token route and receive a token... username is the token used in this case... 
@app.post("/token")
async def token_generate(form_data: OAuth2PasswordRequestForm = Depends()):
    # Here you would normally validate username/password
    username = form_data.username

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_SECONDS)
    access_token = create_access_token(
        data={"sub": username},  # "sub" is the subject (user identifier)
        expires_delta=access_token_expires
    )
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

#doesnt matter if i comment this /token or not... coz fastapi always goes top to bottom scan
@app.post("/token")
async def token_generate(form_data:OAuth2PasswordRequestForm=Depends()):
    print(form_data)
    print(form_data.username)
    print(form_data.password)

    return {
        "access_token":form_data.username, # the actual token 
        "token_type":"bearer" #only those who bear the token in the header while sending HTTP requests are allowed
    }

#to access this method , you need to have a token (depends(oauth_scheme))....
@app.get("/funfact")
async def get_funfact(token:str =Depends(oauth_scheme)):
    username = verify_token(token)
    return {
        "welcome":username,
        "ig":"you got authenticated??",
        "funfact":"1+1 is 2 ig"
    }

if __name__ == "__main__":
    uvicorn.run("test:app", host="127.0.0.1", port=8000, reload=True)

