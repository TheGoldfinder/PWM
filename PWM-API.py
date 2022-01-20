from urllib import request
from fastapi import FastAPI
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
oldepoch = 0
callsPerMinute = 0
maxCallsPerMin = 120


@app.get("/")
def home():
    return {"connected": True}


@app.get("/login")
def login(email: str, password: str):
    return str(email) + " " + str(password)


@app.get("/register")
def register(email: str, password: str):
    return


def callLimiter():
    global callsPerMinute

    lastClient = request.client

    if callsPerMinute >= maxCallsPerMin:
        return False
    callsPerMinute += 1
