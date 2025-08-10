import os
from pymongo import MongoClient
from utils import hash, verify
from fastapi import Depends
from datetime import datetime

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = MongoClient(MONGO_URI)

db = client["read2speech"]  # make sure db name matches your worker too


# Dependency for FastAPI
def get_mongo_db():
    return db


# User CRUD

def create_user(username: str, password: str, email: str, db) -> bool:
    user = {
        "username": username,
        "password_hash": hash(password),
        "email": email,
        "send_mail": False,
        "created_at": datetime.utcnow(),
    }
    db.users.insert_one(user)
    return True


def delete_user(username: str, password: str, db) -> bool:
    user = db.users.find_one({"username": username})
    if not user:
        return False
    if not verify(password, user["password_hash"]):
        return False

    # Cascade delete tasks for this user
    db.tasks.delete_many({"username": username})
    result = db.users.delete_one({"_id": user["_id"]})
    return result.deleted_count == 1


# Task CRUD

def insert_task(username: str, link: str, db) -> bool:
    task = {
        "username": username,
        "link": link,
        "status": "pending",
        "created_at": datetime.utcnow(),
        "completed_at": None,
        "output_file": None,
    }
    db.tasks.insert_one(task)
    return True


# User settings toggle for email notifications

def settings_toggle(username: str, toggle: bool, db) -> bool:
    result = db.users.update_one(
        {"username": username},
        {"$set": {"send_mail": toggle}},
    )
    return result.modified_count == 1


if __name__ == "__main__":
    print("Running basic tests...")

    # Example usage (you can uncomment and test)
    # if create_user("john_doe", "securepassword", "john@example.com", db):
    #     print("User created")

    # if insert_task("john_doe", "https://example.com/article", db):
    #     print("Task inserted")

    # if settings_toggle("john_doe", True, db):
    #     print("Settings toggled")

    # if delete_user("john_doe", "securepassword", db):
    #     print("User deleted")
