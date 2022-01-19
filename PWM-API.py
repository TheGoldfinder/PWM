from fastapi import FastAPI
from cryptography.fernet import Fernet
import cryptocode
import json
import time

uppercaseLetters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K",
                    "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "ß"]

lowercaseLetters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
                    'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', "ß"]

uppercaseUmlaut = ["Ä", "Ö", "Ü"]

lowercaseUmlaut = ["ä", "ö", "ü"]

numbers = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]

specialCharacter = ["!", "\"", "/", "\'", "#", "+", "*", "~", ",", ".", "-", "_", "´", "`",
                    "?", "=", "}", ")", "]", "(", "[", "{", "&", "%", "$", "§", "^", "°", "<", ">", "|", "@", "€"]

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
    return {"key": key, "timestamp": time.time()}


@app.get("/testKey")
def testKey():
    return {"key": key, "timestamp": time.time()}


@app.get("/login")
def login(email: str, password: str):
    emailDecrypted = cryptocode.decrypt(email, key)
    passwordDecrypted = cryptocode.decrypt(password, key)

    return


@app.get("/register")
def register(email: str, password: str):
    return


getKey()
