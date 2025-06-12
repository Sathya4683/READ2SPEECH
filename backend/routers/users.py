from fastapi import FastAPI, APIRouter,Depends
from auth import auth


router = APIRouter(
    prefix="/api/users",
    tags=["Users"]
)



@router.post("/signup")
def user_signup():
    return token


@router.post("/login")
def user_login():
    return token


@router.post("/settings")
def user_settings():
    return {}