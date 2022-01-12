from fastapi import FastAPI, Path
import json

app = FastAPI()


@app.get("/")
def home():
    return {"connected": True}


@app.get("/login")
def login(userName: str, password: str):
    with open("users.txt", "r") as file:
        t = file.readlines()
    return userName + " " + password
