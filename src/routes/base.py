from fastapi import FastAPI, APIRouter
import os 
router = APIRouter(
    prefix="/api/v1",
    tags=["api v1"],
)
@router.get("/")
async def welcome_message():
    app_name=os.getenv("APP_NAME")
    app_version=os.getenv("APP_version")
    return {"message": f"Welcome fROM {app_name} {app_version}!"}