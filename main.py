from fastapi import FastAPI
app = FastAPI()
@app.get("/welcomes")
def welcome_message():
    return {"message": "Welcome to the FastAPI application!"}