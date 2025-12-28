from fastapi import APIRouter, Depends, UploadFile, status
from fastapi.responses import JSONResponse
import os
from src.helpers.config import get_settings, Settings
from src.controllers import DataController, ProjectController
import aiofiles
from src.models import ResponseSignal
import logging
logger =logging.getLogger("uvicorn.error")

router = APIRouter(
    prefix="/api/v1/data",
    tags=["api v1", "data"],
)


@router.post("/upload/{project_id}")
async def upload_data(
    project_id: str,
    file: UploadFile,
    app_settings: Settings = Depends(get_settings)
):
    # Validate file type and size
    data_controller = DataController()
    data_controller.validate_upload_file(file)
    
    # Generate unique file path
    file_path = data_controller.generate_unique_filename(file.filename, project_id)
    
    # Save file in chunks (handles large files efficiently)
    try:
        async with aiofiles.open(file_path, "wb") as out_file:
            # Walrus operator (:=) reads chunk and checks if not empty in one expression
            while chunk := await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
                await out_file.write(chunk)
    except Exception as e:
        logger.error(f"Failed to upload file: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"signal": ResponseSignal.FILE_UPLOADED_FAILED.value}
        )
    
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"signal": ResponseSignal.FILE_UPLOADED_SUCCESSFULLY.value}
    )