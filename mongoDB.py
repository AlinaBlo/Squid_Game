###############################################################
# Imports
###############################################################
import pymongo
from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://ruppinea:ea2022EA@cluster0.yu53bb5.mongodb.net/?retryWrites=true&w=majority")
db = cluster["users"]
collision = db["users"]

# Search for user
def Search_User(username,email):
    print("Search User")
    results = collision.find({"username": username,"email": email})
    for result in results:
        return result["username"],result["email"]
    return "",""

def Search_username(username):
    results = collision.find({"username": username})
    for result in results:
        return result["username"]
    return ""

def Add_Score(username,Score):
    collision.update_one({"username": username},{"$push":{"scores":Score}})

def Get_Score(username):
    results = collision.find({"username": username})
    for result in results:
        return result["scores"]
    return "username not found"

def Search_email(email):
    results = collision.find({"email": email})
    for result in results:
        return result["email"]
    return ""

# New user
def New_User(username,email,password,age):
    print("new user")
    Fusername=Search_username(username)
    Femail=Search_email(email)
    scores=[]
    if Femail == "":
        print()
        if  Fusername == "":
            post = {"username": username, "email": email, "password": password, "age": age, "scores":scores}
            collision.insert_one(post)
            return 0
        else:
            print("username in use")
            return 1
    else:
        print("email in use")
        return 2

# user name and password
def login_User(username,password):
    results = collision.find({"username": username,"password": password})
    for result in results:
        return result["username"],result["password"]
    return "",""