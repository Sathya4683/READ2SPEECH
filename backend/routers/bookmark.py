from fastapi import FastAPI, APIRouter,Depends
from schemas import req_schema,res_schema


router = APIRouter(
    prefix="/api/bookmark",
    tags=["Bookmark functionality"]
)


@router.post("/add",response_model=res_schema.LinkSaved)
def add_website(save_link:req_schema.Link):
    return {}

@router.delete("/delete")
def remove_website():
    return {}