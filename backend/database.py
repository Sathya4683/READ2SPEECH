from pymongo import MongoClient
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = MongoClient(MONGO_URI)

db = client["readtospeech"]
links=db.links


def create_user(username:str,password:str)
def insert_links(id:int,username:str,link:str):
    payload={
        "id":id,
        "username":username,
        "link":link
    }
    return links.insert_one(payload).inserted_id

    

if __name__=="__main__":

    # post={"name":'chiiga',"age":123}
    # posts=db.posts  #posts is the collection
    # post_id=posts.insert_one(post).inserted_id

    # print(post_id)

    print(insert_links(69,"niggesh123@gmail.com","https://www.google.com"))
