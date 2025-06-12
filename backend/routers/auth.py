from fastapi import APIRouter,Request,Depends,HTTPException,status
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse
from oauth2 import create_access_token
import utils
from bson.objectid import ObjectId
from schemas import res_schema
from database import get_mongo_db,create_user

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)



@router.post("/login", response_model=res_schema.Token_send)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db = Depends(get_mongo_db)):
    # Fetch user from MongoDB
    user = db.users.find_one({"username": user_credentials.username})
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User not found"
        )

    # Check password (assuming you used hash() to store the password during signup)
    if not utils.verify(user_credentials.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Password is incorrect"
        )

    # Generate JWT (use MongoDB _id or username/email as identifier)
    token = create_access_token({"id": str(user["_id"]), "email": user["username"]})

    return {
        "access_token": token,
        "token_type": "Bearer"
    }


@router.post("/signup", response_model=res_schema.Token_send)
def signup_user(user_credentials: OAuth2PasswordRequestForm = Depends(), db = Depends(get_mongo_db)):
    # Check if user already exists
    if db.users.find_one({"username": user_credentials.username}):
        raise HTTPException(status_code=400, detail="User already exists")


    if create_user(user_credentials.username,user_credentials.password,db):    
        # Create JWT token

        token = create_access_token({"id": str(new_user["_id"]), "email": new_user["username"]})

        return {
            "access_token": token,
            "token_type": "Bearer"
        }
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="unable to create user")