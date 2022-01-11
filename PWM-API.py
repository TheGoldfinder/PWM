from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def home():
    return {"connected": True}


@app.get("/login")
def login():
    return {"loggingIn": False}
