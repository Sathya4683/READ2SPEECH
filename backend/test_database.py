from pymongo import MongoClient

client = MongoClient("mongodb+srv://meow:meow123@cluster0.5ssxoyj.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

db = client.test_database123

collection=db.test_collection

collection.insert_one({"name":"sdfsadf","age":0})

print("collection created")

