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
    user = getSpecificUser(email)
    if user == False:
        return "Error 403 user not found"
    else:
        if user["email"] == email and user["password"] == password:
            return {"login": True}


@app.put("/register")
def register(email: str, password: str):
    return


def getUserName(email):
    addIsReached = False
    userName = ""
    for i in email:
        if i == "@":
            addIsReached = True
        if not addIsReached:
            userName += i
    return userName


def checkUserExists(email):
    users = getJsonUsers()
    userName = getUserName(email)

    if userName in users:
        return True
    return False


def getJsonUsers():
    with open("users.json", "r") as file:
        users = json.loads(file.read())
    return users


def writeJsonUsers(usersDict):
    with open("users.json", "w") as file:
        file.write(json.dumps(usersDict))
    return


def addJsonUser(email, password):
    users = getJsonUsers()
    userName = getUserName(email)
    userExists = checkUserExists(email)

    if not userExists:
        users[userName] = {"email": email, "password": password}
        writeJsonUsers(users)
        return True
    return False


def getSpecificUser(email):
    userName = getUserName(email)
    users = getJsonUsers()
    userExists = checkUserExists(email)

    if userExists:
        return users[userName]
    return False
