from fastapi import APIRouter, Depends, UploadFile, status
from fastapi.responses import JSONResponse
import os
from src.helpers.config import get_settings, Settings
from src.controllers import DataController, ProjectController,ProcessController
import aiofiles
from src.models import ResponseSignal
import logging
from .schemes.data import ProcessRequset

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
    # Step 1: Validate file type and size to ensure it's allowed
    data_controller = DataController()
    data_controller.validate_upload_file(file)
    
    # Step 2: Generate a unique name for the file and get its storage path
    file_path, file_id = data_controller.generate_unique_filepath(file.filename, project_id)
    
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
        content={"signal": ResponseSignal.FILE_UPLOADED_SUCCESSFULLY.value, "file_id": file_id}
    )
    
@router.post("/process/{project_id}")
async def process_endpoint(
    project_id: str,
    request: ProcessRequset,
    app_settings: Settings = Depends(get_settings)
):
    # Step 1: Get processing parameters from the request
    file_id = request.file_id
    chunk_size = request.chunk_size
    overlap_size = request.overlap_size
    
    # Step 2: Load the file content based on project and file ID
    process_controller = ProcessController(project_id)
    file_content = process_controller.get_file_content(file_id)
    
    # Step 3: Split content into chunks for RAG processing
    file_chunks = process_controller.process_file_content(file_content, file_id, chunk_size, overlap_size)
    # If no chunks were produced, return an error
    if file_chunks is None or len(file_chunks) == 0:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"signal": ResponseSignal.FILE_PROCESSED_FAILED.value}
        )
    
    # Return the successfully processed chunks
    return file_chunks
