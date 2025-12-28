from fastapi import FastAPI
from src.routes import base,data
from motor.motor_asyncio import AsyncIOMotorClient
from src.helpers.config import get_settings
app = FastAPI()

# Event that runs when the FastAPI application starts
@app.on_event("startup")
async def startup_db_client():
    settings = get_settings()
    # Initialize MongoDB client connection
    app.mongo_conn = AsyncIOMotorClient(settings.MONGODB_URL)
    # Connect to the specific database
    app.db_client = app.mongo_conn[settings.MONGODB_DATABASE]

# Event that runs when the FastAPI application stops
@app.on_event("shutdown")
async def shutdown_db_client():
    # Close MongoDB connection
    app.mongo_conn.close()

app.include_router(base.router)
app.include_router(data.router) 
