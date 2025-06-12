from fastapi import FastAPI, APIRouter,Depends


router = APIRouter(
    prefix="/api/feed",
    tags=["Frontend Feed"]
)



@router.get("/audiobooks")
def get_audiobook():
    return {}



#background task to send mail.. goes here?