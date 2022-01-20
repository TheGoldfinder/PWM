import uvicorn

if __name__ == "__main__":
    uvicorn.run("PWM-API:app", host="127.0.0.1", port=8000, reload=True)
