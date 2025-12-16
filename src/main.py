from fastapi import FastAPI
from routes.base import router
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()
app.include_router(router)