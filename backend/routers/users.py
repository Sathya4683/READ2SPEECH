from fastapi import APIRouter,Depends,status
from fastapi.responses import JSONResponse
from schemas import req_schema,res_schema
from oauth2 import get_current_user
from database import get_mongo_db, create_user, settings_toggle, delete_user, insert_links

router = APIRouter(
    prefix="/api/users",
    tags=["Users"]
)

#update the mail_settings field in users collection to update/turn on the mail(that is get notification after the video has been convererted to an audio book) 
@router.post("/settings")
def user_settings(
    pref: req_schema.SetPreferences,
    user_token: req_schema.TokenData = Depends(get_current_user),db=Depends(get_mongo_db)
):
    success = settings_toggle(user_token.email, pref.mails,db)

    if success:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "status": "success",
                "message": f"Email preference updated to {pref.mails}"
            }
        )
    else:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "status": "failure",
                "message": "User not found or update failed"
            }
        )


#post the link from the browser extension into the links collection
@router.post("/add", response_model=res_schema.LinkSaved)
def add_website(save_link: req_schema.Link, user_token: req_schema.TokenData = Depends(get_current_user),db=Depends(get_mongo_db)):
    
    if insert_links(id=user_token.user_id, username=user_token.email, link=save_link.url,db=db):
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "status": "link saved successfully",
                "link": save_link.url
            }
        )
    else:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "status": "unable to save link",
                "link": save_link.url
            }
        )
    


@router.delete("/delete")
def remove_website():
    return {}