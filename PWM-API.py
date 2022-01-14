from fastapi import FastAPI, Path
from cryptography.fernet import Fernet
import cryptocode
import json
import time

app = FastAPI()
key = ""
oldepoch = 0


@app.get("/")
def home():
    return {"connected": True}


@app.get("/getKey")
def getKey():
    global key, oldepoch

    if key == "":
        key = Fernet.generate_key()
        oldepoch = time.time()
    elif key != "":
        timeVar = time.time() - oldepoch
        if timeVar >= 8:
            key = Fernet.generate_key()
            oldepoch = time.time()
        elif timeVar > 3 and timeVar < 8:
            oldepoch = time.time()
    return {"key": key}


@app.get("/testKey")
def testKey():
    global key
    return key


@app.get("/login")
def login(email: str, password: str):
    global key

    emailDecrypted = cryptocode.decrypt(email, key)
    passwordDecrypted = cryptocode.decrypt(password, key)

    return
