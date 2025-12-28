from fastapi import FastAPI, APIRouter, Depends
import os 
from src.helpers.config import get_settings,Settings
router = APIRouter(
    prefix="/api/v1",
    tags=["api v1"],
)
@router.get("/")
async def welcome_message(app_settings: Settings = Depends(get_settings)):
   app_name = app_settings.APP_NAME
   app_version = app_settings.APP_VERSION
   return {"message": f"Welcome fROM {app_name} {app_version}!"}