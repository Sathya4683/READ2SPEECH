from pymongo import MongoClient
from utils import hash,verify
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = MongoClient(MONGO_URI)

#create db and links/users collections
db = client["readtospeech"]
links=db.links
users=db.users


#first time user creation.. signup probably can be used
def create_user(username:str,password:str):
    user={
        "username":username,
        "password":hash(password),
        "send_mail": False 
    }
    users.insert_one(user)
    return True


#delete user entirely from the collection... have to also delete links related to the deleted user (smth like cascade delete)
def delete_user(username: str, password: str) -> bool:
    user = users.find_one({"username": username})
    if not user:
        return False  
    if not verify(password, user["password"]):  
        return False 
    
    result = users.delete_one({"_id": user["_id"]})  
    return result.deleted_count == 1

#add the links along with username, user_id embedded in the JWT and store in links collection
def insert_links(id:int,username:str,link:str):
    payload={
        "user_id":id,
        "username":username,
        "link":link
    }
    links.insert_one(payload)
    return True

#from the UI... ask the user to toggle whether they want notifications (have to create a button or smth ig in frontend ig)
def settings_toggle(username: str, toggle: bool) -> bool:
    result = users.update_one(
        {"username": username},
        {"$set": {"send_mail": toggle}}
    )
    
    return result.modified_count == 1



if __name__=="__main__":

    print("tests?")
    # post={"name":'chiiga',"age":123}
    # posts=db.posts  #posts is the collection
    # post_id=posts.insert_one(post).inserted_id

    # print(post_id)

    # if create_user("nig@gmail.com","hello123"):
    #     print("user has been created lol")
    
    # if delete_user("nig@gmail.com","hello123"):
    #     print("user has been deleted lmao")